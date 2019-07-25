# import the necessary packages
from picamera.array import PiRGBArray
import picamera
from itertools import repeat
import itertools
import random
from itertools import starmap
import matplotlib
import cv2
import numpy as np
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import io
import matplotlib
import matplotlib.pyplot as plt

BLUR = 200
camera = picamera.PiCamera()

while True:
    motors.enable()
    #Capture the image
    stream = io.BytesIO()
    time.sleep(2)
    camera.capture(stream,format="jpeg")
    #Convert the stream from the capture to an array
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #Convert to BGR order for cv2
    img=cv2.imdecode(data,1)
    
    ##Uncomment to test a specific image
    #img = cv2.imread("test3.jpg")
    #img = cv2.resize(img,(1280,840))
    # Camera warm-up time

    
    
    #Change to 480 p
    t1 = time.time()
    #Blur the initial image to get an estimate of the average shape of the green
    kernel = np.ones((BLUR,BLUR),np.float32)/(BLUR*BLUR)
    dst = cv2.filter2D(img,-1,kernel)
    #cv2.imwrite("dst.jpg",dst)
    #Convert to hsv to detect green pixels more easily
    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (18, 44, 0), (81, 255,255))

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
    mask = cv2.inRange(dst, (125,0,250),(130,0,255))
    imask = mask>0
    pink = np.zeros_like(green, np.uint8)
    pink[imask] = (127,0,255)
    #Crop outsides which do not pick up the image very well
    def cropImgSides(img, scale):
        centerX,centerY=img.shape[1] / 2, img.shape[0] /2
        widthScaled, heightScaled = img.shape[1] * scale, img.shape[0]
        leftX,rightX=centerX - widthScaled / 2, centerX + widthScaled /2
        topY,bottomY= centerY - heightScaled / 2, centerY + heightScaled / 2
        imgCropped = img[int(topY):int(bottomY),int(leftX):int(rightX)]
        return imgCropped
    pink = cropImgSides(img,0.6)

    #Displayed image
    orig = pink
    #img data file
    img = pink
    #Used to calculate through the algorithm
    orig_img = pink
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
    #Using the calculated distance, control the robot
    try:
        if dist < -50 and dist >= -350:
            
            for i in range (20):
                motors.setSpeeds(-160, -220)
                time.sleep(.05)
        
        elif dist > 50 and dist >= 350:
            
            for i in range (20):
                motors.setSpeeds(-220, -160)
                time.sleep(.05)
        elif dist > -50 and dist < 50:
            
            for i in range (25):
                motors.setSpeeds(-210, -217)
                time.sleep(.05)
        
        elif dist < -350:
            
            motors.setSpeeds(0, 0)
            time.sleep(0.05)
            for i in range(20):
                motors.setSpeeds(-100, -200)
                time.sleep(.05)
        
        elif dist > 350:
            
            motors.setSpeeds(0, 0)
            time.sleep(0.05)
            for i in range(15):
                motors.setSpeeds(-200, -100)
                time.sleep(.05)
    except KeyboardInterrupt:
        break
    finally:
        motors.setSpeeds(0,0)
        motors.disable()
    t2 = time.time()
    print(t2-t1)
    vanishing_line = cv2.line(orig,(index_min,0),(index_min,420),(0,0,255),2)
    center_line = cv2.line(orig,(640,0),(640,420),(0,255,0),2)
    distance_text = cv2.putText(orig,str(dist),(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.destroyAllWindows()
    cv2.imshow("image", orig)
    #cv2.imshow("mask", mask)
    
    cv2.waitKey(500)
    