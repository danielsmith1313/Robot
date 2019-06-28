import sys
import csv
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import *

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


    def reverse(self):
        self.lblDisplay.setText("reverse")
    
    def left(self):
        self.lblDisplay.setText("left")


    def right(self):
        self.lblDisplay.setText("right")

    def stop(self):
        self.lblDisplay.setText("stop")

#Test if this is being run directly or being imported as a class
if __name__ == '__main__':
    #Launch the program
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
    
