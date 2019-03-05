# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:58:10 2019

@author: csvankhede
"""

import base64
import numpy as np
import io
from PIL import Image
import pandas as pd
from keras.models import load_model
from flask import request
from flask import jsonify
from flask import Flask
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import tensorflow as tf
import pymysql
import time


app = Flask(__name__)

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

server = pymysql.connect(host = "localhost", user = "root", passwd = "password",db = 'malaria_diagno')
cur = server.cursor()
@app.route("/login",methods=["GET","POST"])
def login():
    message = request.get_json(force=True)
    user_id = message["user_id"]
    password = message["password"]
    try:
        pswrd = cur.execute("SELECT password IN `login` WHERE User_ID==%s;",user_id)
        server.commit()
        if pswrd == password:
            jsonify({"login_response":"You have loged in successfuly"})
        else:
            jsonify({"login_response":"Wrong password"})
    except:
        jsonify({"login_response":"Invalid Username."})
        
@app.route("/signup",methods=["GET","POST"])
def signup():
    message = request.get_json(force=True)
    user_id = message["user_id"]
    name = message["name"]
    age = message["age"]
    gender= message["gender"]
    email= message["email"]
    password = message["password"]
    try:
        cur.execute("INSERT INTO `user`(User_ID,Name,Age,Gender,Email_ID,Password) VALUES (%s,%s,%s,%s,%s,%s);",(user_id,name,age,gender,email,password))
        server.commit()
        jsonify({"login_response":"Signed up sccessfully."})
    except:
        jsonify({"login_response":"User ID already exist."})
@app.route("/save_report",methods=["GET","POST"])
def save_report():
    message = request.get_json(force=True)
    report = message["report"]
    user_id=
    report_id=
    date=
    name=
    age=
    image_id=
    gender=
    try:
        cur.execute("INSERT INTO `report`(Report_ID,User_ID,Report,Date,Name,Age,Image_ID,Gender) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);",(report_id,user_id,report,date,name,age,image_id,gender))
        server.commit()
        jsonify({"save_report_response":"Report has been saved successfully!"})
    except:
        jsonify({"save_report_response":"Try again!"})
        
    
    
    
app.run()
