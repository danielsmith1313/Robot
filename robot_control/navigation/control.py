from dual_g2_hpmd_rpi import motors, MAX_SPEED
import time

class control():
    #controls the forward movement of the robot
    #This function accepts how long the motors should run and the speed for both motors
    @classmethod
    def forward(distance, speed):
        try:
            for i in range(distance):
                motors.enable()
                motors.setSpeeds(int(speed * MAX_SPEED), int(speed * MAX_SPEED))
                time.sleep(.005)
            
        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()


    #controls the reverse movement of the robot
    #This function accepts how long the motors should run and the speed for both motors
    #It multiplies the speed inputs by negative one to run the motors backwards
    def reverse(distance, speed):
        try:
            for i in range(distance):
                motors.enable()
                motors.setSpeeds(int(-1 * speed * MAX_SPEED), int(-1 * speed * MAX_SPEED))
                time.sleep(.005)
            
        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()
    
            
    #controls the left or right movement of the robot
    #This function accepts how long the motors should run and the speed for both motors  
    #Depending on the speed difference between the left and right motors, it will either move left or right      
    def leftOrRight(distance, speedM1, speedM2):
        #Reset the motors
        motors.disable()
        try:
            for i in range(distance):
                motors.motor1.setSpeed(int(speedM1 * MAX_SPEED))
                motors.motor2.setSpeed(int(speedM2 * MAX_SPEED))
                time.sleep(.005)
            
        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()

    
    #Stops all motors from running
    def stop():
        motors.setSpeeds(0,0)
        motors.disable()

control.forward(200, 1)