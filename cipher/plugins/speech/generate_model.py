#!/usr/bin/python3
# coding: utf-8
import numpy as np
import json
from keras.models import Sequential
from keras.layers import Dense, LSTM
from librosa.core import load
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from os.path import join
from os import listdir
from recorder.features import N_SAMPLE_MFCCS, N_MFCC, SELECTED_FEATURE
from recorder.constants import SAMPLERATE, TRAINED_MODEL_PATH, DATASET_PATH
from recorder.processes import pre_process
from recorder.reader import get_labels

def get_dataset(feature, pre_process_func, split_ratio=0.8, random_state=44):
    """
    Create a dataset from all the samples and their annotation.
    """
    with open(join(DATASET_PATH, 'classes.json'), 'r') as filename:
        dataset_json = json.load(filename)

        X = None
        y = np.array([])

        labels = get_labels()

        for dir_name, class_name in dataset_json.items():
            class_path = join(DATASET_PATH, str(dir_name))
            for file in listdir(class_path):
                if file.endswith('.wav'):
                    data, _rate = load(join(class_path, file), sr=SAMPLERATE)
                    y = np.hstack((y, labels.index(class_name)))
                    if X is None:
                        X = np.array([feature(pre_process_func(data))])
                    else:
                        X = np.append(X, [feature(pre_process_func(data))], axis=0)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= (1 - split_ratio), random_state=random_state, shuffle=True)
        #X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], CHANNELS)
        #X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], CHANNELS)
        y_train_hot = to_categorical(y_train)
        y_test_hot = to_categorical(y_test)

        return X_train, X_test, y_train_hot, y_test_hot

def get_model():
    model = Sequential()
    model.add(LSTM(128, activation='tanh', input_shape=(N_SAMPLE_MFCCS, N_MFCC)))
    model.add(Dense(len(get_labels()), activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    return model

if __name__ == '__main__':
    print("Creating model ...")
    model = get_model()
    print("Extracting dataset ...")
    X_train, X_test, y_train, y_test = get_dataset(SELECTED_FEATURE, pre_process)
    print("Training model ...")

    epochs = 60
    batch_size = 40
    print(X_train.shape)

    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(X_test, y_test))
    model.save(TRAINED_MODEL_PATH)