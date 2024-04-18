import pandas as pd
from sklearn.model_selection import train_test_split
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

raw_data1 = pd.read_csv("C:\Second_python\emnist-letters-train.csv",header=None)
raw_data2 = pd.read_csv("C:\Second_python\emnist-letters-test.csv",header=None)

#print(raw_data1.head())
#print(raw_data1.columns.values[:10])

#print(raw_data2.head())
#print(raw_data2.columns.values[:10])


raw_data = raw_data1.append(raw_data2,ignore_index=True)
#print(raw_data.head())





train, test =   train_test_split(raw_data, test_size=0.1) # change this split however you want


X_train = train.values[:,1:]
y_train = train.values[:,0]

X_test = test.values[:,1:]
y_test = test.values[:,0]
print(X_train.shape)
print(y_train.shape)
print(y_test)
# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]
print(y_test)

# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation='relu'))
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

# build the model
model = baseline_model()
# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

# serialize model to JSON
model_json = model.to_json()
with open("model_letters.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model_letters.h5")
print("Saved model to disk")
