# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 18:18:01 2019

@author: csvankhede
"""

# import all layers of keras
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten,Dropout,Activation
from keras.models import Sequential
from keras.optimizers import Adam
def CNN():
    model = Sequential()
	# Layer 1
	model.add(Conv2D(32,(2,2),padding = 'same', activation = 'relu', input_shape = (50,50,3),name= 'conv1'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool1'))
	# Layer 2
	model.add(Conv2D(32,(2,2),padding = 'same', activation = 'relu',name= 'conv2'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool2'))
	# Layer 3
	model.add(Conv2D(64,(2,2),padding = 'same', activation = 'relu',name= 'conv3'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool3'))
	# Layer 4
	model.add(Conv2D(64,(2,2),padding = 'same', activation = 'relu',name= 'conv4'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool4'))
	# Layer 5
	model.add(Conv2D(128,(2,2),padding = 'same', activation = 'relu',name= 'conv5'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool5'))
	# Layer 6
	model.add(Conv2D(128,(2,2),padding = 'same', activation = 'relu',name= 'conv6'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool6'))
	# Layer 7
	model.add(Conv2D(256,(2,2),padding = 'same', activation = 'relu',name= 'conv7'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool7'))
	# Layer 8
	model.add(Conv2D(256,(2,2),padding = 'same', activation = 'relu',name= 'conv8'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool8'))
	# Layer 9
	model.add(Conv2D(512,(2,2),padding = 'same', activation = 'relu',name= 'conv9'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool9'))
	# Layer 10
	model.add(Conv2D(512,(2,2),padding = 'same', activation = 'relu',name= 'conv10'))
	model.add(MaxPooling2D(pool_size=(2,2),padding= 'same',name='maxpool10'))

	model.add(Flatten())
	model.add(Dense(512,name = 'Dense1'))
	model.add(Dropout(0.2))
	model.add(Dense(units=1,activation='sigmoid',name = 'Dense2'))
	model.compile(optimizer=Adam(lr=0.00001),loss='binary_crossentropy', metrics=['accuracy'])
		
    return model