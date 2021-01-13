#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 22:25:45 2020

@author: aida
"""
import os
import json
import pandas as pd
from os import listdir, getcwd
from os.path import join

counter_list=[0,0,0,0,0,0,0,0,0,0,0]
def how_many_images_from_that_class(object_class,counters):
    counter_list[object_class]+=1
    print(counter_list)
    print(counter_list[object_class])
    return counter_list[object_class]

          
     
with open('/media/aida/New Volume/training.csv', newline='') as csvfile:
    data = pd.read_csv(csvfile)
    for i in range(len(data)):
        file = data['subDirectory_filePath'][i]
        #print(file)
        image_folder_path= 'data/obj/'+str(file)+'\n'
        object_class = data['expression'][i]
        number= how_many_images_from_that_class(object_class, counter_list)
        if number <= 5000:
            print('hello')
            #outfile = open('/media/aida/New Volume/val.txt', 'a+')
            #outfile.write(str(image_folder_path))
        else:
            pass
