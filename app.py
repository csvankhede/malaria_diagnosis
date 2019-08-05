# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 17:18:30 2019

@author: csvankhede
"""

from flask import Flask
from flask import render_template,request,redirect,session,abort,flash,url_for
import os
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, IntegerField, RadioField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql 
#import pymysql.escape_string as esc
import gc
import base64
import numpy as np
import io
from PIL import Image
import pandas as pd
from keras.models import load_model
from flask import jsonify
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tensorflow as tf

app = Flask(__name__)
app.static_folder = 'static'

bootstrap = Bootstrap(app)



class LoginForm(FlaskForm):
    user_id = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=2, max=16)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=25)])
    age = IntegerField('age',validators=[InputRequired()])
    gender = RadioField('gender',choices = [('M', 'Male'),('F','Female')])
    user_id = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=2, max=50)])
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=50)])
    
@app.route('/logout')
def Logout():
    session['logged in'] = False
    return home()
@app.route('/')
def home():
    if not session.get("logged in"):
        form = RegisterForm()
        return render_template('welcome.html',form=form)
    else:
        return render_template('home.html')
@app.route('/signup',methods=['POST','GET'])
def register():
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            serv = pymysql.connect(host = "localhost", user = "root", passwd = "password",db = 'malaria_diagno')
            cur = serv.cursor()
            
            hash_password = generate_password_hash(form.password.data,method='sha256')
            user_id = form.user_id.data
            name = form.name.data
            age = form.age.data
            gender = form.gender.data
            email = form.email.data
            usr = cur.execute("SELECT * FROM `user` WHERE  User_ID= %s",(user_id,))
            
            if int(usr)>0:
                flash("Username already taken,try another username.")
                serv.commit()
                cur.close()
                serv.close()
                gc.collect()
                return render_template("welcome.html",form=form)
            else:
                cur.execute("""INSERT INTO `user` (User_ID,Name,Age,Gender,Email_ID,Password) VALUES(%s,%s,%s,%s,%s,%s)""",(user_id,name,age,gender,email,hash_password))
                serv.commit()
                flash("Thank you for registration")
                cur.close()
                serv.close()
                gc.collect()
                session['logged in'] = True
                return home()
        return render_template("welcome.html",form=form)
        
    except Exception as e:
        return (str(e))
@app.route('/login',methods=['POST','GET'])
def login():
    
    try:
        form = LoginForm()
        if form.validate_on_submit():
            serv= pymysql.connect(host = "localhost", user = "root", passwd = "password",db = 'malaria_diagno')
            cur = serv.cursor()
            cur.execute("SELECT password FROM user WHERE User_ID= %s",(form.user_id.data,))
            pswrd = cur.fetchone()[0]
            cur.close()
            serv.close()
            gc.collect()
            
            if check_password_hash(pswrd,form.password.data):
                session['logged in'] = True
                return home()
            else:
                pass
        return render_template("home.html",form=form)
            
    except Exception as e:
        return (str(e))
graph = tf.get_default_graph()
def get_model():
    global model
    model = load_model("CNN_model6_2_2019.h5")
    print("model loaded")
    
print("loading model")
get_model()
@app.route("/predict",methods=["get","post"])
def predict():
    global graph
    #get json from client
    message = request.get_json(force=True)
    encoded = message["image"]
    
    #decode base64 image and convert it to np.array
    decoded = base64.b64decode(encoded)
    img = np.array(Image.open(io.BytesIO(decoded)))
    
    #intialize parameter 
    size = 50
    cnt = 0
    thresh_pred = 0.85
    h,w,c = img.shape
    plt.imshow(img)
    max_y = 0 
    while max_y+size < h:
        max_x = 0 
        while max_x+size < w:
            left = max_x
            right = max_x+size
            top = max_y 
            bottom = max_y + size
            
            patch = img[top:bottom,left:right]
            df = pd.DataFrame(np.ndarray.flatten(patch)).values.reshape(-1,50,50,3)
            with graph.as_default():
                prediction = model.predict(df)
            if prediction > thresh_pred:
                cnt+=1
                plt.gca().add_patch(Rectangle((left,top),50,50,linewidth=1,edgecolor='r',facecolor='none'))
            max_x += size-10
        max_y += size-10
    imgBytesIOBytes = io.BytesIO()
    plt.savefig(imgBytesIOBytes,format = 'jpeg')
    imgBytesIOBytes.seek(0)
    encoded_imgBytesIOBytes = str(base64.b64encode(imgBytesIOBytes.read()))
    response = {"predicted_image":encoded_imgBytesIOBytes[2:-1],"count":cnt}
    return jsonify(response)

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    app.run()