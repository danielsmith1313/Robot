#Filename: move_robot.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith

#Import libraries
import traceback
import time
import sys
import os
import control


    #Note: due to python not indexing folders other than the executable and current class
    #the parent folder must be manually appended to the system path. 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'network'))
from ssh_remote import SSHRemote as ssh
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors_and_modules'))
from fisheye_camera import FisheyeCamera as fsh
from gps_reader import GPS
print(sys.path)    

try:
    import numpy as np
    from math import degrees, atan2
except ImportError:
    print("Error importing external library, check to make sure it is installed")
    tb = traceback.format_exc()
    print(tb)

class MoveRobot():
    """
    This class is in charge of moving the robot to follow a set amount of points
    """
    LOW_SPEED = .3
    MEDIUM_SPEED = .6
    HIGH_SPEED = 1
      
    #Coordinate length +- of error before moving on to the next point
    MARGIN_OF_ERROR = .000005
    def __init__(self):
        #Declare variables
        self.__lattitude = []           #Coordinates imported from main
        self.__longitude = []
        self.__currentLattitude = 0     #Stores coordinate data
        self.__currentLongitude = 0
        
        
        self.__desiredTrackAngle = 0    #Stores the calculated bearing
        self.__trackAngle = 0           #Bearing
        self.__speed = 0                #Stores the speed to be ussed in the motor power
        self.__rightSpeed
        self.__leftSpeed
        self.__turningRate = 5          #Percent of motor speed increased and decreased each time
        self.__correctionTime = .2      #Time in between gps measurements and turning corrections
        self.__stoppingTime = .75       #Time the motors are stopped in order to take data
        self.__startupTime = 1

        #Create objects
        self.__gps = GPS()
    def FollowCoordinates(self, lattitudeIn, longitudeIn, speed, option1, option2, option3, option4):
        """
        The main move method of the function
        lattitudeIn is a list of lattitude points
        longitudeIn is a list of longitude points
        Both lat and long arguments must be the same length
        """
        self.__lattitude = lattitudeIn
        self.__longitude = longitudeIn
        #Add two 0 to each list to represent the end of the array
        self.__lattitude.append('nan')
        self.__longitude.append('nan')
        #Get the speed of the function
        if(speed == 1):
            self.__speed = self.LOW_SPEED
        elif(speed == 2):
            self.__speed = self.MEDIUM_SPEED
        elif (speed == 3):
            self.__speed = self.HIGH_SPEED

        self.__leftSpeed = 90 * self.__speed
        self.__rightSpeed = 90 * self.__speed
        control.leftOrRight(self.__leftSpeed, self.__rightSpeed, self.__startupTime)
        #Go through every single point
        for i in range(len(self.__lattitude)):
            
            #Move the robot forward
            control.leftOrRight(self.__leftSpeed, self.__rightSpeed, self.__startupTime)
            #while the robot is not close enough to the specified point
            if(self.__lattitude[i+1] == 'nan'):
                break;
            while(self.__lattitude[i+1] < (self.__gps.GetCurrentCoordinates(0) + self.MARGIN_OF_ERROR) and self.__lattitude[i+1] > (self.__gps.GetCurrentCoordinates(0) - self.MARGIN_OF_ERROR) and self.__longitude[i+1] < (self.__gps.GetCurrentCoordinates(1) + self.MARGIN_OF_ERROR) and self.__longitude[i+1] > (self.__gps.GetCurrentCoordinates(1) - self.MARGIN_OF_ERROR)):
                self.__desiredTrackAngle = self.CalculateBearing(i+1)
                
                if(self.__desiredTrackAngle < self.__gps.GetCurrentTrackAngle()):
                    if(self.__leftSpeed > 0):
                        self.__leftSpeed = self.__leftSpeed - self.__turningRate
                    if(self.__rightSpeed < 100):
                        self.__rightSpeed = self.__rightSpeed + self.__turningRate
                elif(self.__desiredTrackAngle > self.__gps.GetCurrentTrackAngle()):
                    if(self.__rightSpeed > 0 + self.__turningRate):
                        self.__rightSpeed = self.__rightSpeed - self.__turningRate
                    if(self.__leftSpeed < 100 - self.__turningRate):
                        self.__leftSpeed = self.__leftSpeed + self.__turningRate
                control.leftOrRight(self.__leftSpeed, self.__rightSpeed, self.__correctionTime)
            
            control.stop()
            time.sleep(self.__stoppingTime)
            #Take the picture
            #if(option1 == True):
            #    ssh.SendSignalToRunScript("","")
            #Take the second picture
            if(option2 == True):
                fsh.TakePicture(self.__gps.GetCurrentCoordinates(0), self.__gps.GetCurrentCoordinates(1))
    def CalculateBearing(self, indx):
        """
        Calculates the bearing (Degree on the earth) the current point to another
        """
        #Calculate the bearing of two points
        angle = degrees(atan2(self.__lattitude[indx] - self.__gps.GetCurrentCoordinates(0), self.__longitude[indx] - self.__gps.GetCurrentCoordinates(1)))
        #If the angle is over 360 or under 0 set it so it is at the correct angle
        bearing1 = (angle + 360) % 360
        return bearing1
    def TakePhotos(self):
        """
        Uses the FisheyeCam class to take a upward facing picture
        Uses SSH to execute a remote file to take a forward facing picture
        """
        ssh.SendSignalToRunScript()
        fsh.TakePicture()
        
