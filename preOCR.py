import cv2
import numpy as np
from OCR import tesseract
import os
import sys

# Opening image. 
img = cv2.imread(sys.argv[1])

#Resizing Image.
if int(img.shape[0]) > 1500 and int(img.shape[1]) > 1500:
	scale_percent = 30 # percent of original size
	width = int(img.shape[1] * scale_percent / 100)
	height = int(img.shape[0] * scale_percent / 100)
	dim = (width, height)
	resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
	imcopy = resized.copy()
else:
	imcopy = img.copy()

#Converting the Image in YUV spectrum.
imyuv = cv2.cvtColor(resized, cv2.COLOR_BGR2YUV)
imy = np.zeros(imyuv.shape[0:2], np.uint8)
imy[:,:] = imyuv[:,:,0]

#Blurring the text followed by edge detection and finding contours.
imblurred = cv2.GaussianBlur(imy,(3,3),0)
edges = cv2.Canny(imblurred, 100, 300, apertureSize = 3)
contours,hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Finding the contour with max area and creating a bounding rectangular bounding box that fits tightly to the contour.
areas = []
for cnt in contours:
    hull = cv2.convexHull(cnt)
    simplified_cnt = cv2.approxPolyDP(hull, 0.001*cv2.arcLength(hull,True),True)
    areas.append(cv2.contourArea(simplified_cnt))  
max_index = np.argmax(areas)
cnt=contours[max_index]
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(imcopy,(x,y),(x+w,y+h),(0,255,0),2)

#cropping the image according to the bounding box
imcropped = imy[y:y+h, x:x+w]
cv2.imwrite("cropped.jpg", imcropped)

#Calling tesseract
tesseract()

#Deleting the cropped file.
os.remove("cropped.jpg")



