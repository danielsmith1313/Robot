#Import libraries
import traceback
try:
    from SSHRemote import SSHRemote
    from FrontFacingCamera import FrontFacingCamera
except ImportError:
    print("Error importing local classes")
    tb = traceback.format_exc()
    print(tb)
try:
    import numpy as np
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
        self.__currentLattitude = 0
        self.__currentLongitude = 0
        
        
        self.__trackAngle = 0       #Bearing
        self.__speed = 0
    
    def FollowCoordinates(self, lattitudeIn, longitudeIn, speed, option1, option2, option3, option4):
        """
        The main move method of the function
        lattitudeIn is a list of lattitude points
        longitudeIn is a list of longitude points
        Both lat and long arguments must be the same length
        """
        self.__lattitude = lattitudeIn
        self.__longitude = longitudeIn
        #Get the speed of the function
        if(speed == 1):
            self.__speed = self.LOW_SPEED
        elif(speed == 2):
            self.__speed = self.MEDIUM_SPEED
        elif (speed == 3):
            self.__speed = self.HIGH_SPEED

        for i in range(len(lattitudeIn)):
            #while the robot is not close enough to the specified point
            while(self.__lattitude[i] < (self.GetCurrentCoordinates(0) + self.MARGIN_OF_ERROR) and self.__lattitude[i] > (self.GetCurrentCoordinates(0) - self.MARGIN_OF_ERROR) and self.__longitude[i] < (self.GetCurrentCoordinates(1) + self.MARGIN_OF_ERROR) and self.__longitude[i] > (self.GetCurrentCoordinates(1) - self.MARGIN_OF_ERROR)):
                #Move robot to the point
                break
            #Take the picture
            if(option1 == True):
                SSHRemote.SendSignalToTakePicture()
            #Take the second picture
            if(option2 == True):
                FrontFacingCamera.TakePicture



        
    

        

            
    
    def TakePhotos(self):
        """
        Uses the FisheyeCam class to take a upward facing picture
        Uses SSH to execute a remote file to take a forward facing picture
        """
        SSHRemote.SendSignalToTakePicture()
        FrontFacingCamera.TakePicture()
        

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
    