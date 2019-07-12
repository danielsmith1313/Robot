import time
import cv2
import numpy as np
from dual_g2_hpmd_rpi import motors, MAX_SPEED

x = 100
y = 250

leftPixPosition = []
rightPixPosition = []
leftPixPosition2 = []
rightPixPosition2 = []
middlePixPostion = []

goingLeft = False

for i in range(y,y+100):
    for j in range(x,x+50):
        leftPixPosition.append((i,j))
        #img[i,j] = (255,255,255)

for i in range(y,y+100):
    for j in range(x+390,x+440):
        rightPixPosition.append((i,j))
        #img[i,j] = (255,255,255)

for i in range(y-50,y):
    for j in range(x+90,x+140):
        leftPixPosition2.append((i,j))
        #img[i,j] = (255,255,255)

for i in range(y-50,y):
    for j in range(x+300,x+350):
        rightPixPosition2.append((i,j))
        #img[i,j] = (255,255,255)

for i in range(y-70,y-20):
    for j in range(x+170,x+270):
        middlePixPostion.append((i,j))
        #img[i,j] = (255,255,255)

#capturing video through webcam
cap=cv2.VideoCapture(0)

while True:
    motors.enable()
    _, img = cap.read()
    img = cv2.resize(img, (640, 360), interpolation = cv2.INTER_AREA)
    
    x = 100
    y = 250

    greenLeft = False
    greenRight = False
    greenLeft2 = False
    greenRight2 = False
    greenMiddle = False

    leftGreenPixCount = 0
    rightGreenPixCount = 0
    leftGreenPixCount2 = 0
    rightGreenPixCount2 = 0
    middleGreenPixCount = 0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (37,81,65), (91,255,255))
    #result = cv2.bitwise_and(img, img, mask=mask)

    leftBottom = cv2.rectangle(img,(x,y),(x+50,y+100),(0,0,255),3)
    rightBottom = cv2.rectangle(img,(x+390,y),(x+440,y+100),(0,0,255),3)
    leftTop = cv2.rectangle(img,(x+90,y-50),(x+140,y),(0,0,255),3)
    rightTop = cv2.rectangle(img,(x+300,y-50),(x+350,y),(0,0,255),3)
    middleTop = cv2.rectangle(img,(x+170,y-70),(x+270,y-20),(0,0,255),3)
    
    # Checking for greens in bottom left box
    for i in range(len(leftPixPosition)):
        x,y = leftPixPosition[i]
        if mask[x,y] == 255:
            leftGreenPixCount += 1
            greenLeft = True

    # Checking for greens in bottom right box
    for i in range(len(rightPixPosition)):
        x,y = rightPixPosition[i]
        if mask[x,y] == 255:
            rightGreenPixCount += 1
            greenRight = True

    # Checking for greens in left upper box
    for i in range(len(leftPixPosition2)):
        x,y = leftPixPosition2[i]
        if mask[x,y] == 255:
            leftGreenPixCount2 += 1
            greenLeft2 = True

    # Checking for greens in right upper box
    for i in range(len(rightPixPosition2)):
        x,y = rightPixPosition2[i]
        if mask[x,y] == 255:
            rightGreenPixCount2 += 1
            greenRight2 = True

    # Checking for greens in middle upper box
    for i in range(len(middlePixPostion)):
        x,y = middlePixPostion[i]
        if mask[x,y] == 255:
            middleGreenPixCount += 1
            greenMiddle = True

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.line(img, (320, 0), (320, 359), (0,255,0), 2)
    
    if ((greenLeft == True and greenLeft2 == True and greenRight == False) or (greenLeft == True and greenRight == False)):
        motors.setSpeeds(-170, -90)
        cv2.putText(img,"right",(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        goingLeft = False
        print("Go right")

    if greenLeft == True and greenLeft2 == True and greenMiddle == True and greenRight2 == True and greenRight == False:
        motors.setSpeeds(0, 0)
        time.sleep(0.05)
        for i in range(50):
            motors.setSpeeds(-120, 0)
        cv2.putText(img,"stop and go right",(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        goingLeft = False
        print("Go right")

    if ((greenRight == True and greenRight2 == True and greenLeft == False) or (greenRight == True and greenLeft == False)):
        motors.setSpeeds(-90, -170)
        cv2.putText(img,"left",(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        goingLeft = True
        print("Go left")

    if greenLeft == False and greenLeft2 == True and greenMiddle == True and greenRight2 == True and greenRight == True:
        motors.setSpeeds(0, 0)
        time.sleep(0.05)
        for i in range(50):
            motors.setSpeeds(0, -120)
        cv2.putText(img,"stop and go left",(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        goingLeft = True
        print("Go left")

    if greenLeft == False and greenRight == False and greenLeft2 == False and greenRight2 == False:
        motors.setSpeeds(-180, -185)
        cv2.putText(img,"straight",(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        goingLeft = False
        print("Go straight")

    if ((greenLeft == True and greenRight == True and greenLeft2 == True and greenRight2 == True) or (greenLeft2 == True and greenRight2 == True and greenMiddle == True)):
        cv2.putText(img,"stop",(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        print("Stop")
        motors.setSpeeds(0, 0)
    
        
        if goingLeft == True:
            motors.setSpeeds(0, 0)
            time.sleep(0.05)
            for i in range(50):
                motors.setSpeeds(0, -120)
        
        elif goingLeft == False:
            motors.setSpeeds(0, 0)
            time.sleep(0.05)
            for i in range(50):
                motors.setSpeeds(-200, 0)
        
    

    #cv2.imshow('image',img)
    #cv2.imshow('mask',mask)
    #cv2.imshow('result',result)
    
    cv2.imshow("orginal with line", img)  
    key = cv2.waitKey(1) & 0xFF     
    if key == ord("q"):
        motors.disable()
        break
        cv2.destroyAllWindows()
