import sys
sys.path.append(".")
from .dual_g2_hpmd_rpi import motors, MAX_SPEED
import time


class control():
    # controls the forward movement of the robot
    # This function accepts how long the motors should run and the speed for both motors
    
    #Declare constants
    

    
    def __init__(self):
        self.LEFT_OFFSET = 1
        self.RIGHT_OFFSET = .93
    def forward(self, distance, speed):
        motors.enable()
        
        try:
            for i in range(distance):
                
                motors.setSpeeds(int(-1 * speed * MAX_SPEED),
                                 int(-1 * speed * MAX_SPEED))
                time.sleep(.005)

        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()

    # controls the reverse movement of the robot
    # This function accepts how long the motors should run and the speed for both motors
    # It multiplies the speed inputs by negative one to run the motors backwards

    def reverse(self, distance, speed):
        motors.enable()
        try:
            for i in range(distance):
                
                motors.setSpeeds(int(speed * MAX_SPEED),
                                 int(speed * MAX_SPEED))
                time.sleep(.005)

        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()

    # controls the left or right movement of the robot
    # This function accepts how long the motors should run and the speed for both motors
    # Depending on the speed difference between the left and right motors, it will either move left or right
    
    def leftOrRight(self, speedM1, speedM2, distance):
        # Reset the motors
        motors.enable()
        self.speed1 = speedM1 * self.LEFT_OFFSET
        self.speed2 = speedM2 * self.RIGHT_OFFSET
        try:
            for i in range(int(distance)):
                motors.motor1.setSpeed(int(-1 * self.speed1 * MAX_SPEED))
                motors.motor2.setSpeed(int(-1 * self.speed2 * MAX_SPEED))
                time.sleep(.005)

        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()

    # Stops all motors from running
    
    def stop(self):
        motors.setSpeeds(0, 0)
        motors.disable()
