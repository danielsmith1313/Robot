#Filename: camera.py
# Author: Daniel Smith
#Created: 5/23/2019
# Last edited: 6/4/2019 by Daniel Smith

import picamera
# import
from PIL import Image
from time import sleep
import time
import uuid
import datetime
from gps_reader import GPS
import fractions
import sys
from GPSPhoto import gpsphoto

class Camera():
    """
    This static class is in charge of getting data from the front facing camera
    """

    def __init__(self):
        pass

    @classmethod
    def TakePicture(self):
        """
        Sends a signal to recieve data from the front facing camera
        """
        # Create object to get date and time
        now = datetime.datetime.now()
        gps = GPS()
        self.__coordinates = gps.GetCurrentCoordinates(0)
        self.__longitude = self.__coordinates[0]
        self.__latitude = self.__coordinates[1]

        # Generate a unique filename
        self.uniqueFilename = str(uuid.uuid4())
        self.path = self.uniqueFilename
        self.path += ".jpeg"
        #picamera.PiCamera.close(self)
        with picamera.Picamera() as camera:
            camera.resolution = (1024,768)
            camera.start_preview()
            time.sleep(2)
            camera.capture(path)
            camera.stop_preview()

        #Set gps coordinates to exif data
        photo = gpsphoto.GPSPhoto(path)
        info = gpsphoto.GPSInfo(self.__latitude,self.__longitude)
        photo.modGPSData(info,path)

    @classmethod
    def ExportImage(self):
        """
        Converts the image file into a readable image and saves it to the network folder
        """
        pass
