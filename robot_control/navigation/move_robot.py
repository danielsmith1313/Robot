#Filename: move_robot.py
# Author: Daniel Smith
#Created: 5/23/2019
# Last edited: 5/29/2019 by Daniel Smith
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'network'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sensors_and_modules'))
# Import libraries
from gps_reader import GPS
from fisheye_camera import FisheyeCamera as fsh
from ssh_remote import SSHRemote as ssh
#Used for exception handling
import traceback
#Library for time measurment
import time
#Library contains many math functions for algorithms
import math
#Library contains many array manipulating functions
import numpy as np

from .control import control

# Note: due to python not indexing folders other than the executable and current class
# the parent folder must be manually appended to the system path.







class MoveRobot():
    """
    This class is in charge of moving the robot to follow a set amount of points
    """

    #STARTING AND CORRECTING SPEED OF THE MOTORS:
    #Edit these values to change how much the different options change
    LOW_SPEED = .8
    MEDIUM_SPEED = .9
    HIGH_SPEED = 1

    # Coordinate length +- of error before taking a picture and moving on to the next point
    #Note: .1 = 1 mile
    #Note: margin of error is in a square around the point
    MARGIN_OF_ERROR = .000005
    DISTANCE_CALIBRATION = .1
    def __init__(self):
        # Declare variables
        self.__lattitude = []  # Coordinates imported from main
        self.__longitude = []
        self.__currentLattitude = 0  # Stores coordinate data
        self.__currentLongitude = 0
        self.__distance = 0
        
        
        self.__speed = 0  # Stores the speed to be ussed in the motor power
        self.__rightSpeed = 0   #Stores the speed of the robot
        self.__leftSpeed = 0
        self.__control = control()  #Motor controller object
        self.__coordinates = []     #Holds the gps coordinates
        
        # Create objects
        self.__gps = GPS()

    def FollowCoordinates(self, lattitudeIn, longitudeIn, speed, option1, option2, option3, option4):
        """
        The main move method of the function
        lattitudeIn is a list of lattitude points
        longitudeIn is a list of longitude points
        Both lat and long arguments must be the same length
        """
        #Set them to private fields
        self.__lattitude = lattitudeIn
        self.__longitude = longitudeIn
        # Add two 0 to each list to represent the end of the array
        self.__lattitude.append('nan')
        self.__longitude.append('nan')
        # Get the speed of the function from the application
        if(speed == 1):
            self.__speed = self.LOW_SPEED
            self.__speedCalibration = self.LOW_SPEED + .4
        elif(speed == 2):
            self.__speed = self.MEDIUM_SPEED
            self.__speedCalibration = self.MEDIUM_SPEED + .2
        elif (speed == 3):
            self.__speed = self.HIGH_SPEED
            self.__speedCalibration = self.HIGH_SPEED
        
        #Gets the current coordinates from the gps chip
        #NOTE: Gps must be attached to USB0 port by default
        
        #Set the speeds to the factor already set
        self.__leftSpeed = self.__speed
        self.__rightSpeed = self.__speed
        # Go through every single point
        for i in range(len(self.__lattitude)):
            #Set coordinates of current position
            self.__coordinates = self.__gps.GetCurrentCoordinates(0)
            
            self.__distance = self.CalculateDistance(self.__lattitude[i], self.__lattitude[i+1], self.__longitudde[i], self.__longitude[i])
            self.__control.forward(self.__dist * self.DISTANCE_CALIBRATION * self.__speedCalibration, self.__speed)
            # Take the picture
            # if(option1 == True):
            #    ssh.SendSignalToRunScript("","")
            # Take the second picture
            if(option2 == True):
                print("Taking Picture...")
                fsh.TakePicture(self.__coordinates[0], self.__coordinates[1])

    def CalculateBearing(self, indx):
        """
        Calculates the bearing (Degree on the earth) the current point to another
        """
        # Calculate the bearing of two points
        angle = math.degrees(math.atan2(self.__lattitude[indx] - self.__coordinates[0], self.__longitude[indx] - self.__coordinates[1]))
        # If the angle is over 360 or under 0 set it so it is at the correct angle
        bearing1 = (angle + 360) % 360
        return bearing1

    def CalculateTrackAngle(self, la1,la2,lo1,lo2):
            bearing = 90 - (180/math.pi)*math.atan2(la2-la1, lo2-lo1)
            return bearing
    def CalculateDistance(self, la1,la2,lo1,lo2):
        """
        Takes two gps coordinates and calculates the distance between the two in kilometers
        """
        radiousOfEarth = 6373.0
        dlon = lo2 - lo1
        dlat = la2 - lo1

        a = math.sin(dlat/2)**2 + math.cos(la1) * math.cos(la2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))



    def TakePhotos(self):
        """
        Uses the FisheyeCam class to take ssa upward facing picture
        Uses SSH to execute a remote file to take a forward facing picture
        """
        ssh.SendSignalToRunScript()
        fsh.TakePicture()
