#Import libraries
import traceback
import time
import sys
import os



    #Note: due to python not indexing folders other than the executable and current class
    #the parent folder must be manually appended to the system path. 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'network'))
from ssh_remote import SSHRemote as ssh
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors_and_modules'))
from front_facing_camera import FrontFacingCamera as ffc
from gps import GPS as ffc
print(sys.path)    

try:
    import numpy as np
    from math import degrees, atan2
except ImportError:
    print("Error importing external library, check to make sure it is installed")
    tb = traceback.format_exc()
    print(tb)

class MoveRobot():
    LOW_SPEED = 1
    MEDIUM_SPEED = 2
    HIGH_SPEED = 3
    #Coordinate length +- of error before moving on to the next point
    MARGIN_OF_ERROR = .01
    def __init__(self):
        #Declare variables
        self.__lattitude = []        #Coordinates imported from main
        self.__longitude = []
        self.__currentLattitude = 0 #Stores coordinate data
        self.__currentLongitude = 0
        
        
        self.__desiredTrackAngle = 0    #Stores the calculated bearing
        self.__trackAngle = 0           #Bearing
        self.__speed = 0                #Stores the speed to be ussed in the motor power
    
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
        self.__lattitude.append(0)
        self.__longitude.append(0)
        #Get the speed of the function
        if(speed == 1):
            self.__speed = self.LOW_SPEED
        elif(speed == 2):
            self.__speed = self.MEDIUM_SPEED
        elif (speed == 3):
            self.__speed = self.HIGH_SPEED
        #Go through every single point
        for i in range(len(lattitudeIn)):
            #while the robot is not close enough to the specified point
            #MoveForward(self.__speed)
            while(self.__lattitude[i+1] < (self.GetCurrentCoordinates(0) + self.MARGIN_OF_ERROR) and self.__lattitude[i+1] > (self.GetCurrentCoordinates(0) - self.MARGIN_OF_ERROR) and self.__longitude[i+1] < (self.GetCurrentCoordinates(1) + self.MARGIN_OF_ERROR) and self.__longitude[i+1] > (self.GetCurrentCoordinates(1) - self.MARGIN_OF_ERROR)):
                self.__desiredTrackAngle = self.CalculateBearing(i+1)
                
                if(self.__desiredTrackAngle < self.GetCurrentTrackAngle):
                    #IncreaseRightTurn(x)
                    #DecreaseLeftTurn(x)
                    pass
                elif(self.__desiredTrackAngle > self.GetCurrentTrackAngle):
                    #IncreaseLeftTurn(x)
                    #DecreaseLeftTurn(x)
                    pass
                time.sleep(.5)
            #Stop()
            #Take the picture
            if(option1 == True):
                ssh.SendSignalToRunScript("","")
            #Take the second picture
            if(option2 == True):
                ffc.TakePicture()
    def CalculateBearing(self, indx):
        """
        Calculates the bearing (Degree on the earth) the current point to another
        """
        angle = degrees(atan2(self.__lattitude[indx] - self.GetCurrentCoordinates(0), self.__longitude[indx] - self.GetCurrentCoordinates(1)))
        bearing1 = (angle + 360) % 360
        return bearing1
    def TakePhotos(self):
        """
        Uses the FisheyeCam class to take a upward facing picture
        Uses SSH to execute a remote file to take a forward facing picture
        """
        ssh.SendSignalToRunScript()
        ffc.TakePicture()
        

    def GetCurrentCoordinates(self, latorlong):
        """
        Returns the most recent coordinates [lattitude, longitude, altitude]
        """
        if (latorlong == 0):
            return self.__currentLattitude
        elif(latorlong == 1):
            return self.__currentLongitude

    def GetCurrentTrackAngle(self):
        """
        Returns the most recent track angle
        """
        return self.__trackAngle
    
