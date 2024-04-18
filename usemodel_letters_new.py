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
import pandas as pd
from sklearn.model_selection import train_test_split
from PIL import ImageTk, Image, ImageDraw
import PIL


def vectorr(x):
    # Ανάγνωση εικόνας
    gray = cv2.imread(x, cv2.IMREAD_GRAYSCALE)

    # resizing εικόνας και μετατρόπη του backround σε μαύρο
    gray = cv2.resize(255-gray, (28, 28))
    #plt.subplot(121)
    #plt.imshow(gray, cmap=plt.get_cmap('gray'))
    (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #plt.subplot(122)
    #plt.imshow(gray, cmap=plt.get_cmap('gray'))
    flatten = gray.flatten() / 255.0
    #flatten = flatten.reshape((28, 28),order='F')
    #plt.subplot(122)
   # plt.imshow(flatten, cmap=plt.get_cmap('gray'))print()
    #plt.show()
    
    #flatten = flatten.reshape((1, 784),order='F')
   # flatten = flatten.flatten() / 255.0
    return flatten


def predict(dvector):
    global predictions
    # Φόρτωμα αρχείου json και δημιουργία μοντέλου
    json_file = open('model_letters.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model_letters.h5")
    print("Φόρτωση του μοντέλου από τον δίσκο")
    
    predictions = loaded_model.predict(np.array([dvector]))
    print(predictions.shape)
    print(predictions)

    maxp=0
    maxl=0
    letter=0
    isFirst=0
    print(predictions[0])
    for p in predictions[0]:
        if isFirst==1:
            letter=letter+1
            if p>maxp:
                maxp=p
                maxl=letter
        isFirst=1
    print(maxl)
    print("maxp" ,maxp)
    print("Το προβλεπόμενο γράμμα είναι το ", chr(maxl+64))
    return chr(maxl+64)

