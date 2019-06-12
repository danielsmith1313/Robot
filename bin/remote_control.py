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

# The seperate ports will be
# NOTE: USB_VENDOR and USB_PRODUCT can be recieved through lsusb or lsusb -l. It should output a line with xxxx:xxxx for vendor and product respectively
USB_IF = 0
USB_TIMEOUT = 5  # Measured in ms
# Both of these are hexadecimal
USB_VENDOR = 0x0000
USB_PRODUCT = 0x0000

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

endpoint = dev[0][(0, 0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

while True:
    control = None

    try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        print(control)
    except:
        pass

    time.sleep(0.01) # allows exiting more easily
