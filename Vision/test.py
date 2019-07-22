import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('test3.jpg')
kernel = np.ones((1000,1000),np.float32)/1000000
dst = cv2.filter2D(img,-1,kernel)
cv2.imwrite("dst.jpg",dst)
hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

## mask of green (36,25,25) ~ (86, 255,255)
# mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

## slice the green
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = (127,0,255)

kernel = np.ones((500,500),np.float32)/250000
dst = cv2.filter2D(green,-1,kernel)
mask = cv2.inRange(dst, (125,0,250),(130,0,255))
imask = mask>0
pink = np.zeros_like(green, np.uint8)
pink[imask] = (127,0,255)
cv2.imwrite("greendst.jpg",pink)
## save 
cv2.imwrite("green.jpg", green)