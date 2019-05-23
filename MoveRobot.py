#Import libraries
from SSHRemote import SSHRemote
from FrontFacingCamera import FrontFacingCamera
class MoveRobot():
    LOW_SPEED = 1
    MEDIUM_SPEED = 2
    HIGH_SPEED = 3
    def __init__(self):
        #Declare variables
        self.__lattitude = []        #Coordinates imported from main
        self.__longitude = []
        
        
        self.__trackAngle = 0       #Bearing
        self.__speed = 0
    
    def FollowCoordinates(self, lattitudeIn, longitudeIn, speed, option1, option2, option3, option4):
        """
        The main move method of the function
        lattitudeIn is a list of lattitude points
        longitudeIn is a list of longitude points
        Both lat and long arguments must be the same length
        """
        #Get the speed of the function
        if(speed == 1):
            self.__speed = self.LOW_SPEED
        elif(speed == 2):
            self.__speed = self.MEDIUM_SPEED
        elif (speed == 3):
            self.__speed = self.HIGH_SPEED
        
        

        

            
    
    def TakePhotos(self):
        """
        Uses the FisheyeCam class to take a upward facing picture
        Uses SSH to execute a remote file to take a forward facing picture
        """
        SSHRemote.SendSignalToTakePicture()
        FrontFacingCamera.TakePicture()
        

    def GetCurrentCoordinates(self):
        """
        Returns the most recent coordinates [lattitude, longitude, altitude]
        """
        return self.__lattitude, self.__longitude, self.__altitude

    def GetCurrentTrackAngle(self):
        """
        Returns the most recent track angle
        """
        return self.__trackAngle
    