# Filename: remote_control.py
# Author: Daniel Smith


"""
The role of this function is that as long as it is running, will listen to infared signals and perform the functions assigned to each button.
This function is for use with usb infared recievers, which means it is read as a usb keyboard. NOTE: seperate keyboard output will be unavailable
during the execution of this script.
"""


import time
import os
from camera import Camera
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

    def display(str):
        text = font.render(str, True, (255, 255, 255), (159, 182, 205))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery

        screen.blit(text, textRect)
        pygame.display.update()

    pygame.init()
    screen = pygame.display.set_mode( (640,480) )
    pygame.display.set_caption('Python numbers')
    screen.fill((159, 182, 205))

    font = pygame.font.Font(None, 17)

    num = 0
    done = False
    while not done:
        display( str(num) )
        num += 1

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_1]:
            Camera.TakePicture()
        if keys[K_RETURN]:
            pass
        if keys[K_ESCAPE]:
            done = True