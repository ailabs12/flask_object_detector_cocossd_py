
#import numpy as np
import cv2
import os

ssdcocoModelPath = os.path.dirname(os.path.abspath(__file__))

prototxt = os.path.join(ssdcocoModelPath, 'deploy.prototxt')
modelFile = os.path.join(ssdcocoModelPath, 'VGG_coco_SSD_300x300_iter_400000.caffemodel')
prototxtFaces = os.path.join(ssdcocoModelPath, 'deploy_Faces.prototxt')
modelFileFaces = os.path.join(ssdcocoModelPath, 'res10_300x300_ssd_iter_140000_fp16_Faces.caffemodel')

if not os.path.exists(prototxt) or not os.path.exists(modelFile) or not os.path.exists(prototxtFaces) or not os.path.exists(modelFileFaces):
	if not os.path.isfile(prototxt) or not os.path.isfile(modelFile) or not os.path.isfile(prototxtFaces) or not os.path.isfile(modelFileFaces):
		print('exiting: could not find ssdcoco models')
		print('download the model from: https://drive.google.com/file/d/0BzKzrI_SkD1_dUY1Ml9GRTFpUWc/view')
		print('download the model from(for Faces): https://github.com/opencv/opencv_3rdparty/raw/19512576c112aa2c7b6328cb0e8d589a4a90a26d/res10_300x300_ssd_iter_140000_fp16.caffemodel')
		raise SystemExit(1)

#инициализировать ssdcoco модель из prototxt и modelFile для распознавания объектов по классам
net = cv2.dnn.readNetFromCaffe(prototxt, modelFile)

#инициализировать ssdcoco модель из prototxtFaces и modelFileFaces для распознавания лиц
netFaces = cv2.dnn.readNetFromCaffe(prototxtFaces, modelFileFaces)

