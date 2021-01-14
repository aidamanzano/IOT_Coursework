#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 01:27:26 2021

@author: aida
"""


import numpy as np
import argparse
import time
import cv2
import os

from flask import Flask, request, Response, jsonify
import jsonpickle
import base64
import json
from PIL import Image

confthres=0.25
nmsthres=0.1
path="/home/aida/darknet/"

def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
    #labelsPath = os.path.sep.join([yolo_path, "yolo_v3/coco.names"])
    LABELS = open(labels_path).read().strip().split("\n")
    return LABELS

def get_colors(LABELS):
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
    return COLORS


def load_model(configpath,weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net

def get_predection(image,net,LABELS,COLORS):
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # draw a bounding box rectangle and label on the image
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            #print(boxes)
            #print(classIDs)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
            #print('HEREE', confidences[i], LABELS[classIDs[i]])
            
        return image, confidences[i], LABELS[classIDs[i]]
    else:
        return False
    
def main(image):
    # load our input image and grab its spatial dimensions
    #img = cv2.imread(image_path_file)
    labelsPath='/home/aida/darknet/data/obj.names'
    Lables=get_labels(labelsPath)
    CFG="/home/aida/darknet/cfg/yolo-obj.cfg"
    Weights="/home/aida/darknet/backup/yolo-obj_best.weights"
    nets=load_model(CFG,Weights)
    Colors=get_colors(Lables)
    temp=get_predection(image, nets, Lables, Colors)
    if temp:
        res, confidence, prediction = temp
        print('mainfile',prediction, confidence)
        # image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # show the output image
        cv2.imshow("Image", res)
        #cv2.waitKey()
        cv2.destroyAllWindows()
        return confidence, prediction, res
        
#preds, conf, img  = main('/home/aida/cropped.jpg')

app = Flask(__name__)


# route http posts to this method
@app.route('/api/test', methods=['POST'])


def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


    # do some fancy processing here....
    confidence, predictions, inference_image = main(img)
    cv2.imshow("Image", inference_image)
    cv2.waitKey()

    # build a response dict to send back to client
    response = {'message': 'yolo completed, prediction returned. PREDICTION IS {}, CONFIDENCE IS {}'.format(predictions, confidence)
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)


