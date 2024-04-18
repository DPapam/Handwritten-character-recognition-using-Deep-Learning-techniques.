from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.utils import np_utils
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import tensorflow as tf
import tensorflow.examples.tutorials.mnist.input_data as input_data
import math
import scipy
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from PIL import ImageTk, Image, ImageDraw
import PIL

print('hello\n')
global maxp,maxd
def vectorr(x):
    # Ανάγνωση εικόνας
    gray = cv2.imread(x, cv2.IMREAD_GRAYSCALE)

    # resizing εικόνας και μετατρόπη του backround σε μαύρο
    gray = cv2.resize(255-gray, (28, 28))
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    flatten = gray.flatten() / 255.0
    return flatten


def predict(dvector):
    global predictions
    predictions=[]
    # Φόρτωμα αρχείου json και δημιουργία μοντέλου
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    print("Φόρτωση του μοντέλου από τον δίσκο")
    
    predictions = loaded_model.predict(np.array([dvector]))
    maxp=0
    maxd=0
    digit=-1
    for p in predictions[0]:
        digit=digit+1
        if p>maxp:
            maxp=p
            maxd=digit
    print("Ο προβλεπόμενος αριθμός είναι το", maxd)
    return maxd

#file=open("information.txt",'r',encoding='utf-8')
#imgname = file.read()
#file.close()
#a,b= imgname.split("Desktop/")

#messagebox.showinfo("","ΣΤΗΝ ΕΙΚΟΝΑ ΑΠΕΙΚΟΝΙΖΕΤΑΙ Ο ΑΡΙΘΜΟΣ:"+str(predict(vectorr(b))))
#predict(vectorr(b))
