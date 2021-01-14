#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 21:05:41 2020

@author: aida
"""


from __future__ import print_function
import requests
import json
import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        img = cv2.imread(img_name)
        crop_img = img[0:720, 320:960]
        cv2.imshow("cropped.jpg", crop_img)
        cv2.imwrite("cropped.jpg", crop_img)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()


addr = 'http://localhost:5000'
test_url = addr + '/api/test'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('/home/aida/cropped.jpg')
img_path = '/home/aida/cropped.jpg'
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
# decode response
#print(json.loads(response.text))
print(response.text)
# expected output: {u'message': u'image received. size=124x124'}