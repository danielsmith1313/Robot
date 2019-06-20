#This class will take a signle picture and save it with a unique filename

from picamera import PiCamera
# import
import piexif
from PIL import Image
from time import sleep
import time
import uuid
import datetime

# Create object to get date and time
now = datetime.datetime.now()

# Generate a unique filename
uniqueFilename = str(uuid.uuid4())
path = uniqueFilename
path += ".jpeg"
#picamera.PiCamera.close(self)
try:
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(path)
    print("Picture taken, filename: " + path)
finally:
    camera.close()