#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 22:55:06 2021

@author: aida
"""
import PIL
from PIL import Image
import os


folder_path = '/home/aida/darknet/photosweek1/'
#image_name =

def get_date_taken(path):
    return Image.open(path).getexif()[36867]


rootdir='/home/aida/darknet/photosweek1/'

for root, dirs, files in os.walk(rootdir):
    for file in files:
        date_image_was_taken=file[:8]
        print(date_image_was_taken)
        date_time = get_date_taken(rootdir+str(file))
        time=date_time[-8:]
        print(time)
        
        