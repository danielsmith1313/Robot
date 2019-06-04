#Filename: gps_reader.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith
#Code adapted from gps_simpletest.py: 

class GPS:
    """
    This class is in charge of reading data and setting up the GPS.
    """
    def __init__():
        # for a computer, use the pyserial library for uart access
        import serial
        uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3000)
        # Create a GPS module instance.
        gps = adafruit_gps.GPS(uart, debug=False)
        
        # Initialize the GPS module by changing what data it sends and at what rate.
        # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
        # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
        # the GPS module behavior:
        #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

        # Turn on the basic GGA and RMC info (what you typically want)
        gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on the basic GGA and RMC info (what you typically want)
        gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on just minimum info (RMC only, location):
        #gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything:
        #gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on everything (not all of it is parsed!)
        #gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
        
        # Set update rate to once a second (1hz) which is what you typically want.
        gps.send_command(b'PMTK220,1000')
    #ClassMethod
    def GetHasFix(self):
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            return False
    def GetCurrentCoordinates(self, latOrLong):
        """
        Returns the most recent coordinates [lattitude, longitude, altitude]
        """
        
        #Return based on which option was chosen
        gps.update()
        
        
        if (latOrLong == 0):
            self.__currentLattitude = gps.latitude
            return self.__currentLattitude
        elif(latOrLong == 1):
            self.__currentLongitude = gps.longitude
            return self.__currentLongitude
            
    def GetCurrentTrackAngle(self):
        """
        Returns the most recent track angle
        """
        #TODO: use gps coordinates to get actual tracking
        return self.__trackAngle