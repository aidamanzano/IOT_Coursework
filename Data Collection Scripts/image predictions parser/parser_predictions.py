#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 21:57:48 2021

@author: aida
"""

from predictions_with_pathfile import *
import PIL
from PIL import Image
import os
import pandas as pd 

rootdir='/home/aida/darknet/photosweek1/'

def get_date_taken(path):
    return Image.open(path).getexif()[36867]

for root, dirs, files in os.walk(rootdir):
    for file in files:
        file_name=str(file[:-4])
        date_list=[]
        time_list=[]
        predictions_list=[]
        confidence_list=[]
        date_image_was_taken=file[:8]
        
        #print(date_image_was_taken)
        date_list.append(date_image_was_taken)
        date_time = get_date_taken(rootdir+str(file))
        time=date_time[-8:]
        time_list.append(time)
        
        #print(time)
        #print(file)
        full_image_path= rootdir+str(file)
        #print(full_image_path)

        temp=main(full_image_path)
        if temp:  
            conf, pred = temp
            predictions_list.append(pred)
            confidence_list.append(conf)
            print('ALL LISTS:', date_list, time_list,predictions_list,confidence_list)
            #Create the dataframe    
            predictionsdf = pd.DataFrame({'Date':date_list,
                                 'Time':time_list,
                                 'Prediction':predictions_list, 'Confidence':confidence_list})
            
           #Save as a CSV file in my directory
            predictionsdf.to_csv('/home/aida/IOT/IOT_CW/python-fitbit/sensed-data/pics2/' + \
                           file_name+'.csv', \
                           columns = ['Date','Time','Prediction','Confidence'],header=True, 
                           index = False)