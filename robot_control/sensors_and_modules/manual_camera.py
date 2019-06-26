#This class will take a signle picture and save it with a unique filename

from picamera import PiCamera
# import
import piexif
from PIL import Image
from time import sleep
import uuid
import datetime
from gps_reader import GPS
#Create gps object
gps = GPS()
# Create object to get date and time
#now = datetime.datetime.now()

coordinates = gps.GetCurrentCoordinates(0)
latitude = coordinates[0]
longitude = coordinates[1]
latitude = latitude * 1000000
longitude = longitude * 1000000
print(latitude)
print(longitude)
latitude

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
#Set the gps coordinates to the picture
img = Image.open(path)
exif_dict = piexif.load(img.info['exif'])

exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N'
exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'W'
exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = [int(latitude),1000000]
exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = [int(longitude),1000000]
exif_bytes = piexif.dump(exif_dict)
img.save('_%s' % uniqueFilename, "jpeg", exif=exif_bytes)