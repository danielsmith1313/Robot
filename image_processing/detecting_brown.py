import cv2
import numpy as np
import matplotlib.pyplot as plt

def nothing(x):
    pass
#cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 37, 255, nothing)
cv2.createTrackbar("L - S", "Trackbars", 56, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 53, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 79, 255, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)

cv2.createTrackbar("w", "Trackbars", 5, 630, nothing)

while True:
    #_, frame = cap.read()
    img = cv2.imread('1.jpg')
    frame = cv2.resize(img, (640, 420), interpolation = cv2.INTER_AREA)

    h = frame.shape[0]
    w = frame.shape[1]

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")
    w = cv2.getTrackbarPos("w", "Trackbars")
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    BrownArea = cv2.inRange(img, (0,0,26), (21,255,255))
    kernel = np.ones((3,3), np.uint8)
    BrownArea = cv2.erode(BrownArea, kernel, iterations=5)
    BrownArea = cv2.dilate(BrownArea, kernel, iterations=9)
    contours_brown, hierarchy_brown = cv2.findContours(BrownArea.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #print("number of contours: ",len(contours_brown))
    ret,thresh = cv2.threshold(frame,127,255,0)
    contours,hierarchy = cv2.findContours(BrownArea.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    noGreensL = 0
    noGreensR = 0
    """
    for i in range(100,450):
        if mask[180,i] == 255:
            for j in range(180):
                if mask[180,(i+j)] == 0:
                    noGreensL += 1
                    print("mask ",mask[180,(i+j)])
            if noGreensL > 110:
                cv2.line(frame,(i,180),(i,280),(0,0,255),2)
                break
    
    for i in range(250,640):
        if mask[180,i] == 255:
            for j in range(i-120,i):
                if mask[180,j] == 0:
                    noGreensR += 1
            if noGreensR > 110:
                cv2.line(frame,(i,180),(i,280),(0,0,255),2)
                break
    """


    cv2.line(frame,(w,5),(w,300),(0,0,255),2)
    cv2.line(frame,(150,180),(500,180),(0,0,255),2)
    cv2.line(frame,(320,170),(320,420),(0,0,255),2)
    #print("cnt num: ", len(contours))

    #print(leftPoints)
    #cv2.line(frame, (200,200), (320, 419), (0,0,255), 5)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    key = cv2.waitKey(1)
    if key == 27:
        break
#cap.release()
cv2.destroyAllWindows()