# -*- coding: utf-8 -*-
"""lstm for audio trial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cy56NnoicwHvCzXouvpQSMSla2MgqW_p
"""

import pandas as pd #Importing the libraries
import numpy as np
import glob

#practical approach to  deep learning projects using cnn
from google.colab import drive
drive.mount('/content/drive')

Test_root = glob.glob('/content/drive/MyDrive/dog cat librosa/test')[0]    #In Python, the glob module is used to retrieve files/pathnames matching a specified pattern.
Train_root = glob.glob('/content/drive/MyDrive/dog cat librosa/train ')[0]
X_path = glob.glob(Test_root + "/dogs/*")
X_path = X_path + glob.glob(Test_root + "/cats/*")
X_path = X_path + glob.glob(Train_root + "/dog/*")
X_path = X_path + glob.glob(Train_root + "/cat/*")

import ntpath        #The ntpath module provides os. path functionality on Windows platforms. You can also use it to handle Windows paths on other platforms. 
                    #This module treats both forward slashes ( / ) and backward slashes ( \ ) as directory separators.
y = np.empty((0, 1, ))
for f in X_path:
    if 'cat' in ntpath.basename(f):
        resp = np.array([0])
        resp = resp.reshape(1, 1, )
        y = np.vstack((y, resp))
    elif 'dog' in ntpath.basename(f):
        resp = np.array([1])
        resp = resp.reshape(1, 1, )
        y = np.vstack((y, resp))
print (f)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_path, y, test_size=0.25, random_state=42)

import librosa
def librosa_read_wav_files(wav_files):
    if not isinstance(wav_files, list):
        wav_files = [wav_files]
    return [librosa.load(f)[0] for f in wav_files]

wav_rate = librosa.load(X_train[0])[1]
X_train = librosa_read_wav_files(X_train)
X_test  = librosa_read_wav_files(X_test)

import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 2, figsize=(16,7))
axs[0][0].plot(X_train[0])
axs[0][1].plot(X_train[1])
axs[1][0].plot(X_train[2])
axs[1][1].plot(X_train[3])
plt.show()

def extract_features(audio_samples, sample_rate):
    extracted_features = np.empty((0, 41, ))
    if not isinstance(audio_samples, list):
        audio_samples = [audio_samples]
        
    for sample in audio_samples:
        zero_cross_feat = librosa.feature.zero_crossing_rate(sample).mean()
        mfccs = librosa.feature.mfcc(y=sample, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T,axis=0)
        mfccsscaled = np.append(mfccsscaled, zero_cross_feat)
        mfccsscaled = mfccsscaled.reshape(1, 41, )
        extracted_features = np.vstack((extracted_features, mfccsscaled))
    return extracted_features

X_train_features = extract_features(X_train, wav_rate)
X_test_features  = extract_features(X_test, wav_rate)

X_train_features[0]

from keras import layers
from keras import models
from keras import optimizers
from keras import losses
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.utils import to_categorical

train_labels = to_categorical(y_train)
test_labels = to_categorical(y_test)

train_labels

test_labels

X_train_new = X_train_features.reshape(-1,1,X_train_features.shape[1])
print(X_train_new.shape)

X_test_new = X_test_features.reshape(-1,1,X_test_features.shape[1])
print(X_test_new.shape)

from keras.models import Sequential
from keras.layers import Dense,LSTM, Dropout
model = Sequential()
model.add(LSTM(units = 10, return_sequences= True, input_shape = (1,41 )))
model.add(Dropout(0.2))
#model = Sequential()
model.add(LSTM(units = 10, return_sequences= True))
model.add(Dropout(0.2))
#model = Sequential()
model.add(LSTM(units = 10, return_sequences= True))
model.add(Dropout(0.2))
#model = Sequential()
model.add(LSTM(units = 10))
model.add(Dropout(0.2))
model.add(Dense(units = 2, activation = 'sigmoid'))

X_train_features.shape

train_labels.shape

best_model_weights = './base.model'
checkpoint = ModelCheckpoint(
    best_model_weights,
    monitor='val_acc',
    verbose=1,
    save_best_only=True,
    mode='min',
    save_weights_only=False,
    period=1
)
callbacks = [checkpoint]
model.compile(optimizer='adam',
              loss=losses.categorical_crossentropy,
              metrics=['accuracy'])

history = model.fit(X_train_new,train_labels,validation_data=(X_test_new,test_labels),epochs = 200, verbose = 1,callbacks=callbacks)

print(history.history.keys())
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
epochs = range(1, len(acc)+1)
plt.plot(epochs, acc, 'b', label = "training accuracy")
plt.plot(epochs, val_acc, 'r', label = "validation accuracy")
plt.title('Training and validation accuracy')
plt.legend()
plt.show()

model.save_weights('model_wieghts.h9')
model.save('model_keras.h9')



from keras.models import Sequential
from keras.layers import Dense,LSTM, Dropout
model = Sequential()
model.add(LSTM(units = 10, return_sequences= True, input_shape = (X_train_features.shape[1], 1)))
model.add(Dropout(0.2))
model = Sequential()
model.add(LSTM(units = 10, return_sequences= True))
model.add(Dropout(0.2))
model = Sequential()
model.add(LSTM(units = 10, return_sequences= True))
model.add(Dropout(0.2))
model = Sequential()
model.add(LSTM(units = 10))
model.add(Dropout(0.2))
model.add(Dense(units = 1))

print(history.history.keys())
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
epochs = range(1, len(acc)+1)
plt.plot(epochs, acc, 'b', label = "training accuracy")
plt.plot(epochs, val_acc, 'r', label = "validation accuracy")
plt.title('Training and validation accuracy')
plt.legend()
plt.show()

model.save_weights('model_wieghts.h10')
model.save('model_keras.h10')