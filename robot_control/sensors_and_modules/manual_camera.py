#This class will take a signle picture and save it with a unique filename

from picamera import PiCamera
# import
import piexif
from PIL import Image
from time import sleep
import uuid
import datetime
from gps_reader import GPS
import fractions
#Create gps object
gps = GPS()
# Create object to get date and time
#now = datetime.datetime.now()

def change_to_rational(number):
    """convert a number to rantional
    Keyword arguments: number
    return: tuple like (1, 2), (numerator, denominator)
    """
    f = Fraction(str(number))
    return (f.numerator, f.denominator)



coordinates = gps.GetCurrentCoordinates(0)
latitude = coordinates[0]
longitude = coordinates[1]
latitude = fractions.Fraction(latitude)
longitude = fractions.Fraction(longitude)
#latitude = latitude * 1000000
#longitude = longitude * 1000000
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

gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N',
        piexif.GPSIFD.GPSLatitude: latitude,
        piexif.GPSIFD.GPSLongitudeRef: 'W',
        piexif.GPSIFD.GPSLongitude: longitude,
    }
exif_dict = {"GPS": gps_ifd}
exif_bytes = piexif.dump(exif_dict)
piexif.insert(exif_bytes, path)