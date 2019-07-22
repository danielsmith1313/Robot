from itertools import repeat
import itertools
import random
from itertools import starmap
import matplotlib
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
import cv2
import numpy as np
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import threading

#capturing video through webcam
cap=cv2.VideoCapture(0)
dist = 0
orig = None
orig_img = None
def getDist():
    motors.enable()
    cap.set(3,720)
    cap.set(4,480)
    _, image = cap.read()
    img = image
    #Change to 480 p
    
    #cv2.imwrite("compressed.jpg",img)
    t1 = time.time()
    #Blur the initial image to get an estimate of the average shape of the green
    kernel = np.ones((200,200),np.float32)/40000
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

    
    orig = img
    orig = cv2.resize(orig, (640, 420))
    
    img = pink
    orig_img = img
    orig_img = cv2.resize(orig_img, (640, 420))
    image = cv2.resize(img, (640, 420))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
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
    dist = index_min - int(image_width/2)

    t2 = time.time()
    print(t2-t1)
    vanishing_line = cv2.line(orig,(index_min,0),(index_min,420),(0,0,255),2)
    center_line = cv2.line(orig,(320,0),(320,420),(0,255,0),2)
    distance_text = cv2.putText(orig,str(dist),(10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("image", orig)
    #cv2.imshow("mask", mask)
    cv2.imshow("original", orig_img)
    key = cv2.waitKey(1)
    if key == 27:
        motors.disable()
        cv2.destroyAllWindows()

def moveRobot():
    
    #print(low)
    #print(index_min)
    #print(t2-t1)

    if dist < -20 and dist > -280:
        cv2.putText(orig_img,('go left'),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        for i in range (30):
            motors.setSpeeds(-90, -170)
            time.sleep(.05)
        
    if dist > 20 and dist > 280:
        cv2.putText(orig_img,('go right'),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        for i in range (30):
            motors.setSpeeds(-170, -90)
            time.sleep(.05)
    if dist > -20 and dist < 20:
        cv2.putText(orig_img,('go straight'),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        for i in range (30):
            motors.setSpeeds(-150, -155)
            time.sleep(.05)
        
    if dist < -280:
        cv2.putText(orig_img,('stop and turn left'),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        motors.setSpeeds(0, 0)
        time.sleep(0.05)
        for i in range(30):
            motors.setSpeeds(0, -120)
            time.sleep(.05)
        
    if dist > 280:
        cv2.putText(orig_img,('stop and turn right'),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        motors.setSpeeds(0, 0)
        time.sleep(0.05)
        for i in range(50):
            motors.setSpeeds(-120, 0)
            time.sleep(.05)
    
def move():
    #Initialize calculation for the image
    nextPic = 0
    getDist()
    #Create a thread to speed up the calculations
    running = True
    while(running == True):
        imgThread = threading.Thread(target=getDist)
        motorThread = threading.Thread(target=moveRobot)
        try:
            #Start both threads
            imgThread.start()
            motorThread.start()

            imgThread.join()
            motorThread.join()
            nextPic = nextPic + 1
            if(nextPic == 3):
                
        except Exception:
            break