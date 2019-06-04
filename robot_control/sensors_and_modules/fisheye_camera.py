#Filename: fisheye_camera.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 6/4/2019 by Daniel Smith

from picamera import PiCamera
from time import sleep
class FrontFacingCamera():
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
        camera.start_preview()
        sleep(1)
        #Capture and save the image
        camera.capture("../../data/pictures/fisheye")
    @classmethod
    def ExportImage(self):
        """
        Converts the image file into a readable image and saves it to the network folder
        """
        pass