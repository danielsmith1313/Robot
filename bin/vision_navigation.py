#File Description:
#
#This program when called using navigate(), will begin movement based on the configured settings
#and navigate along a single row. 

# import the necessary packages
#Picamera is included in distributions of raspbian, and is used in conjunction with the raspberry pi camera slot to 
#take pictures with raspberry pi compatible cameras
from picamera.array import PiRGBArray
import picamera
from itertools import repeat                    #Itertools allows for faster and different approaches for iterations in Python

import cv2                                      #Open cv library, a powerful library used for image processing
import numpy as np                              #Numpy is a data manipulation library which allows for programs to calculate with classic arrays instead of the python lists
import time                                     #Allows recording of time and sleeping for correct camera pictures
from dual_g2_hpmd_rpi import motors, MAX_SPEED  #Motor control library provided by Polulu for their 
import io                                       #Python library used to manage inp ut and output of the computer
import matplotlib.pyplot as plt                 #Matplotlib is a library used to display and manage data specifically arrays
import sys                                      #Used to exit the program
from ssh_remote import SSHRemote                #SSHRemote is a local class that allows for sshing into a seperate computer on the same network
try:
    from configparser import ConfigParser       #Used to read .ini files
except ImportError:
    from ConfigParser import ConfigParser
class VisionNavigation:
    #Constructors
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.movements = 0
        self.config = ConfigParser()
        self.config.read("config.ini")
    
    def navigate(self):
        """
        Navigate is a function that when called activates the ROW-BOT, with the adjusted configuration settings, 
        to navigate across a row of crops, detect the row end, and move to the next row.
        """
        
        #Configurable constants,
        BLUR = self.config.getint("pathfinding","postblur")
        POSTBLUR = self.config.getint("pathfinding","postblur")
        OFFSET = self.config.getint("pathfinding","offset")
        PIXEL_PERCENT_TO_TURN = self.config.getfloat("pathfinding","brownpixelpercenttoturns")
        NUMOFROWS = self.config.getint("pathfinding", "numberofrows")
        MOTOR_TURNING_TIME = self.config.getint("pathfinding", "motorturningtime")
        MOTOR_STRAIGHT_TIME = self.config.getint("pathfinding", "motorstraighttime")
        MOTOR_U_TURN_TIME = self.config.getint("pathfinding", "motoruturntime")
        DISPLAY_OUTPUT = self.config.get("pathfinding","displayoutput")
        SECONDARY_IP = self.config.get("network","secondaryip")
        PIXEL_PERCENT_TO_TURN = self.config.get("pathfinding","pixelpercenttoturn")
        PIXEL_TYPE_TO_TURN= self.config.get("pathfinding","pixeltype")

        currentRow = 0
        motors.enable()

        #This section of code captures the image from a stream using picamera library, and then converts that image into an array
        # for data manipulation. 
        stream = io.BytesIO()
        time.sleep(1)
        self.camera.capture(stream,format="jpeg")
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        img=cv2.imdecode(data,1)
    
        ##Uncomment to test a specific image
        #img = cv2.imread("test3.jpg")

        #This section of code changes the resolution to the specified settings
        img = cv2.resize(img,(1280,840))
        
        #Declare variables
        ratioBrown = 0

        #This section of code isolates the brown or blue pixels with the rest of the image. NOTE: for all image isolation techniques, the
        # color range is in HSV (Hue, Saturation, Value). Additionally, for all image isolation techniques, the image is split into
        # pink pixels for targeted color, and black for all other colors outside the range.
        
        if(PIXEL_TYPE_TO_TURN==0):
            hsvbrown = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            maskbrown = cv2.inRange(hsvbrown,(0,0,80),(40,90,255))
            imaskbrown = maskbrown>0
            brown = np.zeros_like(img,np.uint8)
            brown[imaskbrown] = (127,0,255)
            ratio = (cv2.countNonZero(maskbrown)/(img.size/3))
            print("Ratio ", np.round(ratio*100,2))
        #Search blue pixels instead
        elif(PIXEL_TYPE_TO_TURN==1):
            hsvblue = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            maskblue = cv2.inRange(hsvblue,(0,0,80),(40,90,255))
            imaskblue = maskblue>0
            blue = np.zeros_like(img,np.uint8)
            blue[imaskblue] = (127,0,255)
            ratio = (cv2.countNonZero(maskblue)/(img.size/3))
            print("Ratio ", np.round(ratio*100,2))
        #This section of code blurs the image from a range in pixels equal to BLUR. 
        kernel = np.ones((BLUR,BLUR),np.float32)/(BLUR*BLUR)
        dst = cv2.filter2D(img,-1,kernel)
    
        #This section of code isolates the green pixels with the rest of the image
        hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (36, 25, 25), (75, 255,255))
        imask = mask>0
        green = np.zeros_like(img, np.uint8)
        green[imask] = (127,0,255)

        #This section of code performs a seconod blurring function, cutting down on edges in the image for higher accuracy
        kernel = np.ones((POSTBLUR,POSTBLUR),np.float32)/(POSTBLUR*POSTBLUR)
        dst = cv2.filter2D(green,-1,kernel)
        mask = cv2.inRange(dst, (36, 25, 25), (75, 255,255))
        imask = mask>0
        pink = np.zeros_like(green, np.uint8)
        pink[imask] = (127,0,255)
    
        #-----
        #Pathfinding algorithm
        #-----
        #This section of code organizes the images into easier to manage variables
        orig = img
        img = dst
        orig_img = dst
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (160,250,248), (255,255,255))

        #This section of code finds the column with the least amount of green in the center. 
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
        dist = index_min - int(image_width/2)                   #This line sets the distance to the center of the image (0)
        dist = dist + OFFSET
        
    
    

        #-----
        #Motor controll and navigation
        #-----
        #This block of code is the decision structure for the robot. First it is tested if the robot has made it to the end of the 
        # row (through pixel percent) If that is not true, the robot continues with its pathfinding forward.
        try:
            if (ratioBrown > PIXEL_PERCENT_TO_TURN):
                for i in range(40):
                    motors.setSpeeds(-100, -210)
                    time.sleep(.05)
            elif dist < -60 and dist >= -300:
            
                for i in range (MOTOR_TURNING_TIME):
                    motors.setSpeeds(-150, -220)
                    time.sleep(.05)
        
            elif dist > 60 and dist <= 300:
            
                for i in range (MOTOR_TURNING_TIME):
                    motors.setSpeeds(-220, -150)
                    time.sleep(.05)
            elif dist > -60 and dist < 60:
            
                for i in range (MOTOR_STRAIGHT_TIME):
                    motors.setSpeeds(-210, -217)
                    time.sleep(.05)
        
            elif dist < -300:
            
                for i in range(MOTOR_TURNING_TIME):
                    motors.setSpeeds(-100, -210)
                    time.sleep(.05)
        
            elif dist > 300:
            
                for i in range(MOTOR_TURNING_TIME):
                    motors.setSpeeds(-210, -100)
                    time.sleep(.05)
        except KeyboardInterrupt:
            sys.exit()

        #This block of code ends all control of the motors and increases the amount of movements before having to take
        # a measurment.
        finally:
            motors.setSpeeds(0,0)
            motors.disable()
            self.movements = self.movements + 1

        #This block of code, after three movements uses the SSHRemote file to send a secure shell command to the external raspberry pi to execute a 
        # camera script.
        if self.movements == 3:
            
            print("Sending ssh to take picture")
            
            SSHRemote.SendSignalToRunScript(SECONDARY_IP,"Desktop/Git/Robot/bin/camera.py")
            self.movements = 0

        
        if(self.config.getboolean("navigation","displayoutput")):
            #This block of code outputs the images along with visual lines
            vanishing_line = cv2.line(orig,(index_min+OFFSET,0),(index_min+OFFSET,840),(0,0,255),2)
            center_line = cv2.line(orig,(580,0),(580,840),(0,255,0),2)

            cv2.destroyAllWindows()
            cv2.imshow("image", orig)
            #cv2.imshow("mask", mask)

    
            cv2.waitKey(500)
