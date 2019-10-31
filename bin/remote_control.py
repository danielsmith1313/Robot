# Filename: remote_control.py
# Author: Daniel Smith


"""
The role of this function is that as long as it is running, will listen to infared signals and perform the functions assigned to each button.
This function is for use with usb infared recievers, which means it is read as a usb keyboard. NOTE: seperate keyboard output will be unavailable
during the execution of this script.
"""


import time
import os
#from camera import Camera
from dual_g2_hpmd_rpi import motors, MAX_SPEED
#Import navigation library
from vision_navigation import VisionNavigation
if(os.name=='nt'):
    import msvcrt
    num = 0
    done = False
    while not done:
        print(num)
        num += 1
        if msvcrt.kbhit():
            print ("you pressed",msvcrt.getch(),"so now i will quit")
            done = True
            print(os.name)

else:
    import pygame
    from pygame.locals import *

    vision = VisionNavigation()

    def display(str):
        text = font.render(str, True, (255, 255, 255), (159, 182, 205))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery

        screen.blit(text, textRect)
        pygame.display.update()

    pygame.init()
    screen = pygame.display.set_mode( (640,480) )
    pygame.display.set_caption('Robot')
    screen.fill((159, 182, 205))

    font = pygame.font.Font(None, 17)

    num = 0
    done = False
    while not done:
        display( str(num) )
        num += 1

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            try:
                for i in range(1):
                
                    motors.enable()
                    motors.setSpeeds(-250, -250)
                    time.sleep(.005)
            except Exception as e:
                print("Failed going forward")
                print(e)
            finally:
                # Stop the motors, even if there is an exception
                # or the user presses Ctrl+C to kill the process.
                motors.setSpeeds(0, 0)
                motors.disable()
                
            pass
        if keys[K_s]:
            #Reset the motors
        
            try:
                for i in range(1):
                
                    motors.enable()
                    motors.setSpeeds(-250, -250)
                    time.sleep(.005)
            except Exception as e:
                print("Failed going backwards")
                print(e)
            finally:
                # Stop the motors, even if there is an exception
                # or the user presses Ctrl+C to kill the process.
                motors.setSpeeds(0, 0)
                motors.disable()
        if keys[K_d]:
            try:
                for i in range(1):
                    motors.enable()
                    motors.setSpeeds(-250,-125)
                    time.sleep(.005)
            except Exception as e:
                print("Failed moving right")
                print(e)
            finally:
                motors.setSpeeds(0,0)
                motors.disable()

        if keys[K_a]:
            try:
                for i in range(1):
                    motors.enable()
                    motors.setSpeeds(-125,-250)
                    time.sleep(.005)
            except Exception as e:
                print("Failed moving left")
                print(e)
            finally:
                motors.setSpeeds(0,0)
                motors.disable()
        if keys[K_1]:
            Camera.TakePicture()
        if keys[K_RETURN]:
            pass
        if keys[K_f]:
            while True:
                vision.navigate()
                
        
        if keys[K_e]:
            done = True