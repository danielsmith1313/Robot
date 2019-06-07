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

    def __init__(self):
        # Declare variables
        self.__lattitude = []  # Coordinates imported from main
        self.__longitude = []
        self.__currentLattitude = 0  # Stores coordinate data
        self.__currentLongitude = 0

        self.__desiredTrackAngle = 0  # Stores the calculated bearing
        self.__trackAngle = 0  # Bearing
        self.__speed = 0  # Stores the speed to be ussed in the motor power
        self.__rightSpeed = 0   #Stores the speed of the robot
        self.__leftSpeed = 0
        self.__turningRate = .015  # Percent of motor speed increased and decreased each time
        self.__correctionTime = 90  # Time in between gps measurements and turning corrections
        self.__startupTime = 250    #The startup time is the initial time it takes the robot to move
        self.__control = control()  #Motor controller object
        self.__coordinates = []     #Holds the gps coordinates
        #1 is left 2 is right. Used to straighten out the gps on correction
        self.__lastTurn = 0
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
        elif(speed == 2):
            self.__speed = self.MEDIUM_SPEED
        elif (speed == 3):
            self.__speed = self.HIGH_SPEED
        
        #Gets the current coordinates from the gps chip
        #NOTE: Gps must be attached to USB0 port by default
        self.startingCoordinates = self.__gps.GetCurrentCoordinates(0)
        
        #Set the speeds to the factor already set
        self.__leftSpeed = .9 * self.__speed
        self.__rightSpeed = .9 * self.__speed
        #Do an initial movement to give the robot a chance to find the heading
        self.__control.leftOrRight(
            self.__leftSpeed, self.__rightSpeed, self.__startupTime)
        #Get the coordinates again after the movement to calculate the bearing
        self.__coordinates = self.__gps.GetCurrentCoordinates(0)
        #Calculate the bearing
        self.__currentTrackAngle = self.CalculateTrackAngle(self.__coordinates[0],self.startingCoordinates[0],self.__coordinates[1],self.startingCoordinates[1])
        # Go through every single point
        for i in range(len(self.__lattitude)):
            #Debug
            self.__coordinates = self.__gps.GetCurrentCoordinates(0)
            print("Coordinates:", self.__coordinates)
            # while the robot is not close enough to the specified point
            #As long as you have not hit the end of the points
            if(self.__lattitude[i+1] == 'nan'):
                break
            #While the robot IS NOT inside the square "drawn" around a point
            while((((self.__lattitude[i+1] + self.MARGIN_OF_ERROR) < self.__coordinates[0]) or (self.__lattitude[i+1] - self.MARGIN_OF_ERROR > (self.__coordinates[0] ))) or (((self.__longitude[i+1] + self.MARGIN_OF_ERROR) < self.__coordinates[1] ) or (self.__longitude[i+1] - self.MARGIN_OF_ERROR > (self.__coordinates[1])))):
                
                #Get the bearing from the previous point to the next point
                #self.__desiredTrackAngle = self.CalculateTrackAngle(self.__coordinates[0], self._MoveRobot__lattitude[i+1], self._MoveRobot__coordinates[1], self._MoveRobot__longitude[i+1])
                self.__desiredTrackAngle = self.CalculateTrackAngle(self.__lattitude[i+1],self.__lattitude[i],self.__longitude[i+1],self.__longitude[i])
                print("Track angle desired:", self._MoveRobot__desiredTrackAngle)
                print("Current Track Angle", self._MoveRobot__currentTrackAngle)

                #Test if the coordinates are off
                if(self.__desiredTrackAngle < self.__currentTrackAngle):
                    #If the robot needs to correct to the right
                    print("Turning right")
                    if(self.__lastTurn == 1):
                        self.__leftSpeed =  .9 *self.__speed
                        self.__rightSpeed = .9 * self.__speed
                    if(self.__leftSpeed > .7):
                        self.__leftSpeed = self.__leftSpeed + self.__turningRate
                    if(self.__rightSpeed < .95):
                        self.__rightSpeed = self.__rightSpeed - self.__turningRate
                    self.__lastTurn = 2
                elif(self.__desiredTrackAngle > self.__currentTrackAngle):
                    #If the robot needs to correct to the left
                    print("Turning left")
                    if(self.__lastTurn == 2):
                        self.__leftSpeed =  .9 *self.__speed
                        self.__rightSpeed = .9 * self.__speed
                    if(self.__rightSpeed > .7):
                        self.__rightSpeed = self.__rightSpeed + self.__turningRate
                        
                    if(self.__leftSpeed < .95):
                        self.__leftSpeed = self.__leftSpeed - self.__turningRate
                    self.__lastTurn = 1
                else:
                    #Otherwise continue straight
                    print("Straight")
                #Get the coordinates before it has corrected
                self.__formerTrackAngle = self.__gps.GetCurrentCoordinates(0)
                #Correct and move forward
                self.__control.leftOrRight(
                    self.__leftSpeed, self.__rightSpeed, self.__correctionTime)
                #Get the current coordinates again
                self.__coordinates = self.__gps.GetCurrentCoordinates(0)
                #Calculate the current track angle so it can be used to calculate in the next loop
                self.__currentTrackAngle = self.CalculateTrackAngle(self.__coordinates[0], self.__formerTrackAngle[0], self.__coordinates[1], self.__formerTrackAngle[1])

            #Reset both speeds since the robot is correct
            self.__leftSpeed =  .9 *self.__speed
            self.__rightSpeed = .9 * self.__speed
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

    def TakePhotos(self):
        """
        Uses the FisheyeCam class to take ssa upward facing picture
        Uses SSH to execute a remote file to take a forward facing picture
        """
        ssh.SendSignalToRunScript()
        fsh.TakePicture()
