#Filename: fisheye_camera.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 6/4/2019 by Daniel Smith

from picamera import PiCamera
#import 
import piexif
from PIL import Image
from time import sleep
import uuid
import datetime
class FisheyeCamera():
    """
    This static class is in charge of getting data from the front facing camera
    """
    
    def __init__(self):
        pass

    @classmethod
    def TakePicture(self,longitude,lattitude):
        """
        Sends a signal to recieve data from the front facing camera
        """
        #Create object to get date and time
        now = datetime.datetime.now()
        
        #Generate a unique filename
        self.uniqueFilename = str(uuid.uuid4())
        self.path = str("../../data/pictures/fisheye/",self.uniqueFilename,".jpeg",sep='')
        camera.start_preview()
        sleep(1)
        #Capture and save the image
        camera.capture(self.path)
        img = Image.open(fname)
        exif_dict = piexif.load(img.info['exif'])
        exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = (longitude, 1)
        exif_dict['GPS'][piexif.GPSIFD.GPSLattitude] = (lattitude,1)
        #Get the current date and time
        currentDateAndTime = str(now.year, ":", now.month, ":", now.day, " ", now.hour, ":", now.minute, ":", now.second, sep='').decode(encoding = "utf-8")
        exif_dict['GPS'][piexif.GPSIFD.GPSDateStamp] = (currentDateAndTime) 
        

        
        exif_bytes = piexif.dump(exif_dict)
        img.save(self.path)
    @classmethod
    def ExportImage(self):
        """
        Converts the image file into a readable image and saves it to the network folder
        """
        pass