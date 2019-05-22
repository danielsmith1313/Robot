import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from MoveRobot import MoveRobot

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Creates a base window by inhereting the QMainWindow class from PyQt5
        Loads the ui from the .ui file generated from the qt designer
        
        """
        #Pass into the constructor
        super(MyWindow, self).__init__()
        #Declare fields
        self.__lattitude = 0            #Contains the lattitude from the user input
        self.__longitude = 0            #Contains the longitude from the user input
        self.__altitude = 0             #Contains the altitude from the user input
        self.__strLattitude = ""            #Contains the lattitude from the user input
        self.__strLongitude = ""            #Contains the longitude from the user input
        self.__strAltitude = ""             #Contains the altitude from the user input
        self.__lattitudeList = []           #Contains the lattitude of all inputs
        self.__longitudeList = []           #Contains the longitude of all inputs
        self.__altitudeList = []            #Contains the altitude of all the inputs
        self.__coordString = ""
        self.__noImagePath = "NoImageFound.png"
        self.__noImagePixmap = QPixmap(self.__noImagePath)
        self.__controller = MoveRobot()
        
        #Load the file 
        uic.loadUi('RobotUI.ui', self)
        
        #Setup widgets and event handlers
        self.setupUI()
        
        #Set it able to be seen
        self.show()
    
    
    def setupUI(self):
        """
        The widgets are already created, however in order to add listeners to them they must be manually added here
        """
        self.btnAdd.clicked.connect(self.addCoordinates)
        self.btnRemoveCoordinates.clicked.connect(self.removeCoordinates)
        self.btnBegin.clicked.connect(self.beginMovement)
        self.btnClear.clicked.connect(self.clearAll)
        #Set a default picture when there are no images that can be read
        self.lblFisheyeNormal.setPixmap(self.__noImagePixmap)
        self.lblFisheyeProcessed.setPixmap(self.__noImagePixmap)
        self.lblFrontFacingNormal.setPixmap(self.__noImagePixmap)
        self.lblFrontFacingProcessed.setPixmap(self.__noImagePixmap)

        
    #-----
    #Functions for event handlers
    #-----

    #btnAdd
    def addCoordinates(self):
        """
        Whenever the btnAdd is clicked (Add Coordinates) trigger this action
        """
        #Get Lattitude Longitude and Altitude from the three QLineEdits
        self.__lattitude = self.txtLattitude.text()
        self.__longitude = self.txtLongitude.text()
        self.__altitude = self.txtAltitude.text()

        #Get the string version for output
        self.__strAltitude = str(self.__altitude)
        self.__strLattitude = str(self.__lattitude)
        self.__strLongitude = str(self.__longitude)
        
        #Append the data onto a list for use in other algorithms
        self.__lattitudeList.append(self.__lattitude)
        self.__longitudeList.append(self.__longitude)
        self.__altitudeList.append(self.__altitude)
        
        self.__coordString = str("Lat: " + self.__strLattitude) + "   Long: " + str(self.__strLongitude)+ "   Alt: " + str(self.__strAltitude)
        print(self.__coordString)
        self.lstPoints.addItem(self.__coordString)
        #Clears the inputs for the next input
        self.clearData()
        self.txtLattitude.setFocus()


    #btnRemoveCoordinates
    def removeCoordinates(self):
        """
        Whenever the btnRemoveCoordinates is clicked (Remove Coordinates) trigger this action
        """
        selectedIndex = self.lstPoints.currentRow()

        del(self.__lattitudeList[selectedIndex])
        del(self.__longitudeList[selectedIndex])
        del(self.__altitudeList[selectedIndex])

        self.lstPoints.takeItem(selectedIndex)

        print(self.__lattitudeList)

    #btnBegin
    def beginMovement(self):
        """
        Whenever the btnBegin is clicked (Begin Movement) trigger this action
        """
        self.__controller.FollowCoordinates(self.__lattitudeList, self.__longitudeList)

    #btnClear
    def clearAll(self):
        """
        Whenever the btnClear is clicked (Clear All) trigger this action
        """
        #Clear the display
        self.lstPoints.clear()
        #Clear the data that was inputted to the text widgets
        self.clearData()
        #Reset the double data
        self.lattitudeList = []
        self.longitudeList = []
        self.altitudeList = []

    #Function clears the lattitude longitude and altitude input text widgets
    def clearData(self):
        #Reset the
        self.txtLattitude.clear()
        self.txtLongitude.clear()
        self.txtAltitude.clear()

        

        
        

#Test if this is being run directly or being imported as a class
if __name__ == '__main__':
    #Launch the program
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())