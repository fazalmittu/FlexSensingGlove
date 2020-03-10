import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.model_selection import train_test_split
from pynput.keyboard import Key, Listener
import logging
import serial
import time
import atexit
import sys

width_val = 200
n = 30 #number of data points

serial_port = '/dev/cu.usbmodem141101'
baud_rate = 9600  # In arduino, Serial.begin(baud_rate)

ser = serial.Serial(serial_port, baud_rate)
ser.close()
ser.open()

value_list = [-1 for i in range(width_val)]

index_counter = 0
key_data = np.zeros((n, width_val))
label_arr = np.zeros((n, 1))

test_data = np.zeros((1, width_val))

key_label_map = {'u': 1, 'm': 2, 'NO KEY': 3}
key_prediction = {0 : 'u', 1 : 'm', 2 : 'NO KEY'}

# GETTING DATA #########################################################################################################

print('TYPE THE KEYS "U" AND "M" 10 TIMES EACH')

def keypress(key):
    logging.info(str(key) + ' pressed')
    global index_counter

    if key.char in key_label_map:
        print('ENTERED IF')

        for k in range(2):
            ser.write(b'0\r\n')

        for i in range(width_val):
            line = ser.readline()
            line = line.decode("utf-8")
            value_list[i] = int(line)

        key_data[index_counter] = value_list

        label_arr[index_counter] = key_label_map[key.char]

        if index_counter == n-11:
            sys.exit()
        index_counter += 1

    print('READY', index_counter)

with Listener(on_press=keypress) as listener:
    listener.join()

print('NOW PLACE YOUR HAND FLAT FOR 10 SECONDS')
print('TRY TO KEEP AS STILL AS POSSIBLE')

time.sleep(5)

for i in range(10):
    ser.write(b'0\r\n')
    for j in range(width_val):
        line = ser.readline()
        line = line.decode("utf-8")
        value_list[j] = int(line)
    key_data[index_counter+i+1] = value_list
    label_arr[index_counter+i+1] = 3

time.sleep(2)

print('DATA COLLECTION COMPLETE')

for i in range(30):
    print(key_data[i])

for i in range(30):
    print(label_arr[i])

#JUST ADDED

# def save_numpy():
#     np.save('key_datafile', key_data)
#     np.save('key_labels', label_arr)
#
# atexit.register(save_numpy)

########################################################################################################################

# ML SECTION ###########################################################################################################

epochs = 10
classes = 3

label_data_ = label_arr.flatten()
label_arr = label_data_-1
label_arr = tf.keras.utils.to_categorical(label_arr)#,num_classes=classes)

layers = [keras.layers.Dense(width_val, input_dim=width_val, activation='relu'),
          keras.layers.Dense(width_val, activation='sigmoid'),
          keras.layers.Dense(classes, activation='softmax')]

model = keras.Sequential(layers)

model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])

model.fit(key_data, label_arr, epochs=epochs)

# sample every 0.66 seconds; get value from ser monitor and run model.predict on it (or 10 values)

while True:
    ser.write(b'0\r\n')
    for i in range(width_val):
        line = ser.readline()
        line = line.decode("utf-8")
        value_list[i] = int(line)
    test_data[0] = value_list

    predictions = model.predict(test_data)

    print(predictions, ' ', key_prediction[np.argmax(predictions)])

    time.sleep(0.66)
