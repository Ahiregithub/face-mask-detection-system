#import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img to_array
from tensorflow.keras.models import load_model
from imutils.video import videostream
import numpy as np
import imutils
import time
import cv2 as cv
import os
def detect_and_predict_mask(frame, faceNet, maskNet):
# grab the dimensions of the frame and then construct a blob
# from it
(h, w) = frame.shape[:2]
blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
  (104.0, 177.0, 123.0))
# pass the blob through the network and obtain the face detections
faceNet.setInput (blob)
detections = facenet.forward()
print(detections.shape)
# initialize our list of faces, their corresponding locations,
# and the list of predictions from our face mask network
faces= []
locs = []
preds = []

 #loop over the detections
for i in range(0, detections.shape[2]):
#extract the confidence (i.e., probability) associated with
#the detection
confidence = detections[0, 0, i, 2]
#filter out weak detections by ensuring the confidence is
# greater than the minimum confidence
if confidence > 5:
#compute the (x, y)=coordinates of the bounding box for
#the object
box = detections[0, , i, 3:7] + np.array([w, h, w, h])
(startx, startY, endx, endy) = box.astype("int")
#ensure the bounding boxes fall within the dinensions of the frane
(startx, starty) = (max(0, startx), max(0, starty))
(endx, endy)=(min(w-1,endx),min(h-1,endy))
 #extract the face ROI, convert it fron BGR to RGB channel
#ordering, resize it to 224x224, and preprocess it
face = frame[starty:endy, startx:endx]
face = cv2.cvtcolor(face, cv2.COLOR_BGR2RGB)
face = cv2.resize(face, (224, 224))
face = img_to_array(face)
face=preprocess_input(face)
#add the face and bounding boxes to their respective
#lists
faces.append(face)
locs.append((startx, starty, endx, endy))
#only make a predictions 1f at least one face was detected
if len(faces) > 0:
#for faster inference we'11 make batch predictions on all
#faces at the sane time rather than one-by-one predictions
#in the above for loop
faces = np.array(faces, dtype="float32")
preds = maskNet.predict(faces, batch_size=32)

 #locations
return (locs, preds)
#load our serialized face detector model from disk
prototxtPath = r"C:\Users\Hp\Desktop\zip1\Face-Mask-Detection-master (1)\Face-Mask-Detection-master\face_detector"
weightsPath = r"C:\Users\Hp\Desktop\zip1\Face-Mask-Detection-master (1)\Face-Mask-Detection-master\face_detector"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
# load the face mask detector model from disk
masknet = load_model("mask_detector.model")
#initialize the video stream
print("[INFO] starting video stream...")
vs = videostream(src=0).start()
# loop over the frames from the video stream
while True:
#grab the frame from the threaded video stream and resize it
# to have a maximum width of 400 pixels
frame= vs.read()
frame = imutils.resize(frame, width=400)
# detect faces in the frame and determine if they are wearing a
# face mask or not
(locs, preds) =detect_and_predict_mask(frame, facelet, masklet)

 # locations
for (box, pred) in zip(locs, preds):
#unpack the bounding box and predictions
(startx, starty, endx, endy) = box
(mask, withoutMask) = pred
#a determine the class label and color we'11 use to dra
#the bounding box and text
label = "Mask" if mask > withoutMask else "No Mask"
color = (0, 25s, 0) if label == "Mask" else (0, 0, 255)
#include the probability in the label
label = "{}: {:.2f}X".format(label, max(mask, withoutMask) * 100)
#display the label and bounding box rectangle on the output
#eframe
cv2. putText (frame, label, (startx, starty - 10),
cv2. FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
cv2.rectangle(frame, (startx, starty), (endx, endy), color, 2)


# show the output frame
cv2.imshow("Frame", frame)
key = cv2.waitKey(1) & 0XFF
# if the q key was pressed, break from the loop
if key == ord("q"):
break
#do a bit of cleanup
cv2. destroyAllwindows ()
vs.stop()




