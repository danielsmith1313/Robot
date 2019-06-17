# Filename: remote_control.py
# Author: Daniel Smith


"""
The role of this function is that as long as it is running, will listen to infared signals and perform the functions assigned to each button.
This function is for use with usb infared recievers, which means it is read as a usb keyboard. NOTE: seperate keyboard output will be unavailable
during the execution of this script.
"""

# Import libraries
import usb.core
import usb.util
import time
import sys

#Import local classes
sys.path.append("..")
#Import from the local package
from robot_control.navigation.move_robot import MoveRobot
from robot_control.file_handling.json_converter import JSONConverter
from robot_control.network.ssh_remote import SSHRemote

# The seperate ports will be
# NOTE: USB_VENDOR and USB_PRODUCT can be recieved through lsusb or lsusb -l. It should output a line with xxxx:xxxx for vendor and product respectively
USB_IF = 0
USB_TIMEOUT = 5  #Measured in ms
# Both of these are hexadecimal
USB_VENDOR = 0x0000
USB_PRODUCT = 0x0000

MOVE_AND_DETECT = ""

#Declare variables
controller = MoveRobot()

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

#Setup the usb as a keyboard
endpoint = dev[0][(0, 0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

while True:
    control = None

    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        print(control)
        if(control == MOVE_AND_DETECT):
            pass
    except:
        pass

    time.sleep(0.01) #allows exiting more easily
