from __future__ import print_function
import time
from dual_g2_hpmd_rpi import motors, MAX_SPEED
 

def runTest():
    try:
        motors.enable()
        while True:
            motors.motor1.setSpeed(300)
            motors.motor2.setSpeed(300)
            


        

    finally:
      # Stop the motors, even if there is an exception
      # or the user presses Ctrl+C to kill the process.
      
      motors.setSpeeds(0,0)
      motors.disable()

runTest()
      

