#Import libraries
from SSHRemote import SSHRemote
from FrontFacingCamera import FrontFacingCamera
class MoveRobot():
    def __init__(self):
        #Declare variables
        self.__lattitude = 0
        self.__longitude = 0
        self.__altitude = 0
        self.__trackAngle = 0
    
    def FollowCoordinates(self, lattitudeIn, longitudeIn):
        """
        The main move method of the function
        lattitudeIn is a list of lattitude points
        longitudeIn is a list of longitude points
        Both arguments must be the same length
        """
        pass
    
    def TakePhotos(self):
        """
        Uses the FisheyeCam class to take a upward facing picture
        Uses SSH to execute a remote file to take a forward faciing picture
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
    