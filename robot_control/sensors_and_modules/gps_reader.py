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
    # ClassMethod
        pass

    def GetHasFix(self):
        if not self.__gps.has_fix:
            # Try again if we don't have a fix yet.
            return False

    def GetCurrentCoordinates(self, option):
        """
        Returns the most recent coordinates [lattitude, longitude, altitude]
        """
        
        # for a computer, use the pyserial library for uart access
        import serial
        self.__uart = serial.Serial(
            "/dev/ttyUSB0", baudrate=9600, timeout=3000)
        # Create a GPS module instance.
        self.gps = adafruit_gps.GPS(self.__uart, debug=False)

        # Initialize the GPS module by changing what data it sends and at what rate.
        # These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
        # PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
        # the GPS module behavior:
        #   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(
            b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(
            b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on just minimum info (RMC only, location):
        # gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn off everything:
        # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # Turn on everything (not all of it is parsed!)
        # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

        # Set update rate to once a second (1hz) which is what you typically want.
        self.gps.send_command(b'PMTK220,1000')
        # Main loop runs forever printing the location, etc. every second.
        last_print = time.monotonic()
        running = True
        while running == True:
            # Make sure to call gps.update() every loop iteration and at least twice
            # as fast as data comes from the GPS unit (usually every second).
            # This returns a bool that's true if it parsed new data (you can ignore it
            # though if you don't care and instead look at the has_fix property).
            self.gps.update()
            # Every second print out current location details if there's a fix.
            current = time.monotonic()
            if current - last_print >= 1.0:
                last_print = current
                if not self.gps.has_fix:
                    # Try again if we don't have a fix yet.
                    print('Waiting for fix...')
                    continue

                if option == 0:
                    self.__currentLattitude =  self.gps.latitude
                    return self.__currentLattitude
                    running = False
                elif option == 1:
                    self.__currentLongitude = gps.longitude
                    return self.__currentLongitude
                    running = False
                # Some attributes beyond latitude, longitude and timestamp are optional
                # and might not be present.  Check if they're None before trying to use!
                elif option == 2:
                    if gps.track_angle_deg is not None:
                        self.__trackAngle = gps.track_angle_deg
                        return self.__trackAngle
                        running = False
                
                

    def GetCurrentTrackAngle(self):
        return self.GetCurrentCoordinates(3)
