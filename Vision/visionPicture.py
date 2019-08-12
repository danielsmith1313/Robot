# import the necessary packages
#from picamera.array import PiRGBArray
#import picamera
from itertools import repeat
import itertools
import random
from itertools import starmap
import matplotlib
import cv2
import numpy as np
import time
#from dual_g2_hpmd_rpi import motors, MAX_SPEED
import io
import matplotlib
import matplotlib.pyplot as plt

BLUR = 300
GREENMASK = (36, 25, 25), (75, 255,255)
#camera = picamera.PiCamera()

while True:
    #motors.enable()
    #Capture the image
    #stream = io.BytesIO()
    #time.sleep(2)
    #camera.capture(stream,format="jpeg")
    #Convert the stream from the capture to an array
    #data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #Convert to BGR order for cv2
    img=cv2.imread("test4.jpg")
    img = cv2.resize(img,(1280,840))
    ##Uncomment to test a specific image
    #img = cv2.imread("test3.jpg")
    #img = cv2.resize(img,(1280,840))
    # Camera warm-up time

    def cropImgSides(im, scale):
        centerX,centerY=im.shape[1] / 2, im.shape[0] /2
        widthScaled, heightScaled = im.shape[1] * scale, im.shape[0]
        leftX,rightX=centerX - widthScaled / 2, centerX + widthScaled /2
        topY,bottomY= centerY - heightScaled / 2, centerY + heightScaled / 2
        imgCropped = im[int(topY):int(bottomY),int(leftX):int(rightX)]
        return imgCropped
    hsvbrown = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    maskbrown = cv2.inRange(hsvbrown,(0,0,80),(40,90,255))
    imaskbrown = maskbrown>0
    brown = np.zeros_like(img,np.uint8)
    brown[imaskbrown] = (127,0,255)
    ratioBrown = (cv2.countNonZero(maskbrown)/(img.size/3))
    print("Ratiobrown ", np.round(ratioBrown*100,2))
    #pink = cropImgSides(img,0.6)
    hsvleaf = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #Get the green filter for output
    
    maskleaf = cv2.inRange(hsvleaf, (36, 25, 25), (75, 255,255))
    imask = maskleaf>0
    ## slice the green, replacing other colors with black
    imaskleaf = maskleaf>0
    greenleaf = np.zeros_like(img, np.uint8)
    #Replace all the locations where there are green pixels with pink
    greenleaf[imask] = (127,0,255)


    t1 = time.time()
    #Blur the initial image to get an estimate of the average shape of the green
    kernel = np.ones((BLUR,BLUR),np.float32)/(BLUR*BLUR)
    dst = cv2.filter2D(img,-1,kernel)
    #cv2.imwrite("dst.jpg",dst)
    #Convert to hsv to detect green pixels more easily
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (36, 25, 25), (75, 255,255))

    ## slice the green, replacing other colors with black
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    #Replace all the locations where there are green pixels with pink
    green[imask] = (127,0,255)

    #Smooth the image to cut out rough edges
    #Note: with 300,300: 30000 as the denominator produces a hollow outline while 30000 produces a filled outline
    kernel = np.ones((10,10),np.float32)/100
    dst = cv2.filter2D(green,-1,kernel)
    #Find the textures that are green and replace the green with pink
    mask = cv2.inRange(dst, (36, 25, 25), (75, 255,255))
    imask = mask>0
    pink = np.zeros_like(green, np.uint8)
    pink[imask] = (127,0,255)
    #Crop outsides which do not pick up the image very well
    

    #Displayed image
    orig = img
    #img data file
    img = dst
    #Used to calculate through the algorithm
    orig_img = dst
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, (160,250,248), (255,255,255))

    xC = []
    low = 0
    image_width = orig_img.shape[1]
    d = [[] for i in repeat(None, image_width)]
    pixels = np.argwhere(mask == 255)

    y = [i[0] for i in pixels]
    x = [i[1] for i in pixels]

    for i in range(len(x)):
        xCoord = x[i]
        d[xCoord].append(xCoord)

    for i in range(len(d)):
        l = len(d[i])
        xC.append(l)

    low = min(xC)
    index_min = np.argmin(xC) + 30
    #Set distance so 0 is centered to the middle
    dist = index_min - int(image_width/2)

    t2 = time.time()
    #print(low)
    #print(index_min)
    #print(t2-t1)
    print("Distance: ", dist)
    
    vanishing_line = cv2.line(orig,(index_min,0),(index_min,420),(0,0,255),2)
    center_line = cv2.line(orig,(640,0),(640,420),(0,255,0),2)
    distance_text = cv2.putText(orig,str(dist),(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.destroyAllWindows()
    #Output
    cv2.imshow("orig", orig)
    cv2.imshow("greenleaf", greenleaf)
    cv2.imshow("dst", dst)
    cv2.imshow("brown",brown)
    #cv2.imshow("mask", mask)
    #Wait until the user stops it
    cv2.waitKey(0)
    break