from keras.datasets import fashion_mnist
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
from PIL import ImageTk, Image,ImageDraw
import PIL
import pandas as pd
from sklearn.model_selection import train_test_split


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
    # Φόρτωμα αρχείου json και δημιουργία μοντέλου
    json_file = open('model_fashion.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model_fashion.h5")
    print("Φόρτωση του μοντέλου από τον δίσκο")
    
    predictions = loaded_model.predict(np.array([dvector]))
    print(predictions.shape)
    print(predictions)

    maxp=0
    maxf=0
    fashion=-1
    print(predictions[0])
    Fashion={0:"T-shirt/top",1:"Trouser",2:"Pullover",3:"Dress",4:"Coat",5:"Sandal",
             6:"Shirt",7:"Sneaker",8:"Bag",9:"Ankle boot"}
    for p in predictions[0]:
        fashion=fashion+1
        if p>maxp:
            maxp=p
            maxf=fashion
    print(Fashion.get(maxf))
    print("Το προβλεπόμενο ρούχο είναι το ", Fashion.get(maxf))
    return Fashion.get(maxf)





