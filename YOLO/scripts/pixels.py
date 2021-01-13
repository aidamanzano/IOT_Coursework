#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 15:55:22 2020

@author: aida
This script reads the main csv file, uses the file name to search for it, opens it and returns the width and height pixel
values, and then saves them onto a csv file.
"""
import os
import json
import pandas as pd
from os import listdir, getcwd
from os.path import join
import PIL
from PIL import Image



with open('/media/aida/New Volume/validation.csv', newline='') as csvfile:
    data = pd.read_csv(csvfile)
    abs_width = []
    abs_height = []
    for i in range(len(data)):
        file = data['subDirectory_filePath'][i]
        #print(file)
        image_folder_path= '/media/aida/New Volume/rootdir/Manually_Annotated_Images/'+str(file)
        #print(image_folder_path)
        with Image.open(image_folder_path) as img:
            absolute_width_val, absolute_height_val = img.size
            abs_height.append(absolute_height_val)
            print(absolute_height_val)
            abs_width.append(absolute_width_val)
            print(absolute_width_val)
    #Create the dataframe    
    df = pd.DataFrame({'Absolute_width':abs_width,
                         'Absolute_height':abs_height})
    
   #Save as a CSV file in my directory
    df.to_csv('/home/aida/' + \
                   'abs_vals_validation'+'.csv', \
                   columns = ['Absolute_width','Absolute_height'],header=True, 
                   index = False)

