import sys
import csv
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import *
from dual_g2_hpmd_rpi import motors, MAX_SPEED
import time

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Creates a base window by inhereting the QMainWindow class from PyQt5
        Loads the ui from the .ui file generated from the qt designer
        
        """
        #Pass into the constructor
        super(MyWindow, self).__init__()
           
        
        #Load the file 
        uic.loadUi('control.ui', self)
        
        #Setup widgets and event handlers
        self.setupUI()
        
        #Set it able to be seen
        self.show()
        
        
        
    
    def setupUI(self):
        """
        The widgets are already created, however in order to add listeners to them they must be manually added here
        """
        self.btnForward.clicked.connect(self.forward)
        self.btnReverse.clicked.connect(self.reverse)
        self.btnLeft.clicked.connect(self.left)
        self.btnRight.clicked.connect(self.right)
        self.btnStop.clicked.connect(self.stop)
        
               
    #-----
    #Functions for event handlers
    #-----         
    
    def forward(self):
        self.lblDisplay.setText("forward")
        
        try:
            for i in range(100):
                
                motors.enable()
                motors.setSpeeds(300, 300)
                time.sleep(.005)
            
        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()



    def reverse(self):
        #Output
        self.lblDisplay.setText("reverse")
        #Reset the motors
        motors.disable()
        try:
            for i in range(100):
                
                motors.enable()
                motors.setSpeeds(-300, -300)
                time.sleep(.005)
            
        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()
    def left(self):
        self.lblDisplay.setText("left")
        #Reset the motors
        motors.disable()
        try:
            for i in range(100):
                
                motors.enable()
                motors.setSpeeds(300, -300)
                time.sleep(.005)
            
        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()

    def right(self):
        self.lblDisplay.setText("right")
        #Reset the motors
        motors.disable()
        try:
            for i in range(100):
                
                motors.enable()
                motors.setSpeeds(-300, 300)
                time.sleep(.005)
            
        finally:
            # Stop the motors, even if there is an exception
            # or the user presses Ctrl+C to kill the process.
            motors.setSpeeds(0, 0)
            motors.disable()

    def stop(self):
        self.lblDisplay.setText("stop")
        motors.setSpeeds(0,0)
        motors.disable()

#Test if this is being run directly or being imported as a class
if __name__ == '__main__':
    #Launch the program
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
    
