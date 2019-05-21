import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import *
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Creates a base window by inhereting the QMainWindow class from PyQt5
        Loads the ui from the .ui file generated from the qt designer
        
        """
        super(MyWindow, self).__init__()
        uic.loadUi('RobotUI.ui', self)
        self.setupUI()
        self.show()
    def setupUI(self):
        """
        The widgets are already created, however in order to add listeners to them they must be manually added here
        """
        self.btnAdd.clicked.connect(self.addCoordinates)
        self.btnRemoveCoordinates.clicked.connect(self.removeCoordinates)
        self.btnBegin.clicked.connect(self.beginMovement)
    
    #-----
    #Functions for event handlers
    #-----
        
    #btnAdd
    def addCoordinates(self):
        """
        Whenever the btnAdd is clicked (Add Coordinates) trigger this action
        """
        #Temporary command
        print('btnAdd clicked')

    #btnRemoveCoordinates
    def removeCoordinates(self):
        """
        Whenever the btnRemoveCoordinates is clicked (Remove Coordinates) trigger this action
        """
        #Temporary command
        print('btnRemoveCoordinates clicked')

    #btnBegin
    def beginMovement(self):
        """
        Whenever the btnBegin is clicked (Begin Movement) trigger this action
        """
        #Temporary command
        print('btnBegin clicked')

    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())