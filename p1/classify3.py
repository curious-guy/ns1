#!/usr/bin/env python3

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import cv2
import numpy
import string
import random
import argparse
import tensorflow as tf
import tensorflow.keras as keras

def sort(lst):
    #print(lst[1][1])
    for i in range(len(lst)-1):
        #print(i[0])
        if lst[i][0].isdigit():
            #print(lst[i])
            temp_String = lst[i]
            lst.pop(i)
            #print(lst)
            lst.append(temp_String)
            #print(lst)
            return lst
            #print(lst) 

def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def main():
    output_list = []
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    print("Classifying captchas with symbol set {" + captcha_symbols + "}")

    with tf.device('/cpu:0'):
        with open(args.output, 'w') as output_file:
            json_file = open(args.model_name+'.json', 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            model = keras.models.model_from_json(loaded_model_json)
            model.load_weights(args.model_name+'.h5')
            model.compile(loss='categorical_crossentropy',
                          optimizer=keras.optimizers.Adam(1e-3, amsgrad=True),
                          metrics=['accuracy'])

            for x in os.listdir(args.captcha_dir):
                # load image and preprocess it
                raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
                rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
                image = numpy.array(rgb_data) / 255.0
                (c, h, w) = image.shape
                image = image.reshape([-1, c, h, w])
                prediction = model.predict(image)
                #output_file.write(x + ", " + decode(captcha_symbols, prediction) + "\n")
                temp = decode(captcha_symbols, prediction)
                output_list.append(temp)
                print(output_list)
                print('Classified ' + x)
            output_list.sort()
            print('abc', output_list)
            sorted_list = sort(output_list)
            print(sorted_list)
            for i in range(len(sorted_list)-1):
                output_file.write(sorted_list[i] + ","+ "\n")
            output_file.write(sorted_list[len(sorted_list)-1] + "\n")

if __name__ == '__main__':
    main()
