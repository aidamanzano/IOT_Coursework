#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 13:14:16 2020

@author: aida
"""

import os
import json
import pandas as pd
from os import listdir, getcwd
from os.path import join

# =============================================================================
# def function_to_get_class(file_name_func):
#    with open('/media/aida/New Volume/training2.csv', newline='') as csvfile:
#     data = pd.read_csv(csvfile)
#     stupid_str= 
#     object_class=data.loc[str(file_name_func), 'expression']
#     return object_class
# =============================================================================

    
# =============================================================================
# 
# rootdir ='/home/aida/IOT'
# counter = 0
# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         #ile_with_directory=
#         file_name_for_label= file[:file.find('.')]+ ".txt"
#         folder = subdir[subdir.rindex('/')+1:]
#         file_name_for_function = str(folder)+'/'+str(file)
#         class_id = function_to_get_class(file_name_for_function)
#         print(class_id)
#         x= 0.5
#         y = 0.5
#         width = 0.87
#         height = 0.87
# =============================================================================
        
# =============================================================================
#         #replace the string '/media/aida/New Volume/Manually_Annotated_Images/' with the location of your image folders

#         outfile = open('/home/aida/IOT'+str(file_name), 'a+')
#         outfile.write(str(object_class) + " " + str(x) + " " + str(y) + " " + str(width) + " " + str(height))
#         outfile.close()
# 
# =============================================================================
        
"""I think this is wrong, I need to c/media/aida/New Volume/Manually_Annotated_Images/numberof folder and then name the txt files as file_name
    iterate through number of folders"""

with open('/media/aida/New Volume/validation.csv', newline='') as csvfile:
    data = pd.read_csv(csvfile)
    for i in range(len(data)):
        file = data['subDirectory_filePath'][i]
        #stripping the folder number up to the character "/" and then removing the .jpg or .png extension to replace it with .txt
        label_file_name= file[file.find('/')+1:file.find('.')]+ ".txt"
        folder = file[:file.index("/")]
        image_folder_path= '/home/aida/darknet/data/obj/'+str(folder)+'/'
        object_class = data['expression'][i]
        x = data['x'][i]
        y = data['y'][i]
        width = data['width'][i]
        height = data['height'][i]
        os.chdir(image_folder_path)
        cwd = os.getcwd()
        #print(label_file_name)
        #print(object_class, x, y, width, height)
        outfile = open(str(image_folder_path)+str(label_file_name), 'w+')
        outfile.write(str(object_class) + " " + str(x) + " " + str(y) + " " + str(width) + " " + str(height))
        outfile.close()