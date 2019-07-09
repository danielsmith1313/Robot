# Filename: remote_control.py
# Author: Daniel Smith


"""
The role of this function is that as long as it is running, will listen to infared signals and perform the functions assigned to each button.
This function is for use with usb infared recievers, which means it is read as a usb keyboard. NOTE: seperate keyboard output will be unavailable
during the execution of this script.
"""


import os
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
    import sys
    import select
    import tty
    import termios

    def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())

        i = 0
        while 1:
            print(i)
            i += 1

            if isData():
                c = sys.stdin.read(1)
                if c == '\x1b':         # x1b is ESC
                    print(c)
                    break

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)