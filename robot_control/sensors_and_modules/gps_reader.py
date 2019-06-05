#Filename: gps_reader.py
# Author: Daniel Smith
#Created: 5/23/2019
# Last edited: 5/29/2019 by Daniel Smith
# Code adapted from gps_simpletest.py:
import adafruit_gps
import time


class GPS:
    """
    This class is in charge of reading data and setting up the GPS.
    """

    def __init__(self):
        # for a computer, use the pyserial library for uart access
        import serial
        self.__uart = serial.Serial(
            "/dev/ttyUSB0", baudrate=9600, timeout=3000)
        # Create a GPS module instance.
        self.__gps = adafruit_gps.GPS(self.__uart, debug=False)

        # Initialize the GPS module by changing what data it sends and at what rate.
        # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
        # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
        # the GPS module behavior:
        #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

        # Turn on the basic GGA and RMC info (what you typically want)
        self.__gps.send_command(
            b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on the basic GGA and RMC info (what you typically want)
        self.__gps.send_command(
            b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on just minimum info (RMC only, location):
        # gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything:
        # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on everything (not all of it is parsed!)
        # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

        # Set update rate to once a second (1hz) which is what you typically want.
        self.__gps.send_command(b'PMTK220,1000')
    # ClassMethod

    def GetHasFix(self):
        if not self.__gps.has_fix:
            # Try again if we don't have a fix yet.
            return False

    def GetCurrentCoordinates(self, latOrLong):
        """
        Returns the most recent coordinates [lattitude, longitude, altitude]
        """

        running = True
        last_print = time.monotonic()
        while running == True:
            # Return based on which option was chosen
            self.__gps.update()
            current = time.monotonic()
            if current - last_print >= 1.0:
                if not self.__gps.has_fix:
                    print('waiting for fix')
                    continue

                    if (latOrLong == 0 and self.__gps.latitude is not None):
                        self.__currentLattitude = self.__gps.latitude
                        return self.__currentLattitude
                        running = False
                    elif(latOrLong == 1 and self.__gps.longitude is not None):
                        self.__currentLongitude = self.__gps.longitude
                        return self.__currentLongitude
                        running = False

    def GetCurrentTrackAngle(self):
        """
        Returns the most recent track angle
        """
        # TODO: use gps coordinates to get actual tracking

        running = True
        last_print = time.monotonic()
        while running == True:
            # Return based on which option was chosen
            self.__gps.update()
            current = time.monotonic()
            if current - last_print >= 1.0:
                if not self.__gps.has_fix:
                    print('waiting for fix')
                    continue
                if self.__gps.track_angle_deg is not None:
                    self.__trackAngle = self.__gps.track_angle_deg
                    return self.__trackAngle
