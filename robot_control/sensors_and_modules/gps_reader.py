#Filename: gps_reader.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith
#TODO: Transfer gps readings from move_robot to this

class GPS:
    """
    This class is in charge of reading data and setting up the GPS.
    """
    def __init__():
        pass
    @ClassMethod
    def GetCurrentCoordinates(self, latorlong):
        """
        Returns the most recent coordinates [lattitude, longitude, altitude]
        """
        #TODO: Use gps to get current coordinates
        #Return based on which option was chosen
        if (latorlong == 0):
            return self.__currentLattitude
        elif(latorlong == 1):
            return self.__currentLongitude
    def GetCurrentTrackAngle(self):
        """
        Returns the most recent track angle
        """
        #TODO: use gps coordinates to get actual tracking
        return self.__trackAngle