import sys
import traceback
#Import external libraries

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5 import QtCore

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
#Import local classes
sys.path.append("..")
#Import from the local package
from robot_control.navigation.move_robot import MoveRobot
from robot_control.file_handling.json_converter import JSONConverter
from robot_control.network.ssh_remote import SSHRemote



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
        self.__coordString = ""             #Contains the concantenated string to output to the application
        self.__noImagePath = "../resources/no_image.png"                 #Filename of the image for when there is no image
        self.__guiPath = "../resources/robot_ui.ui"
        self.__noImagePixmap = QPixmap(self.__noImagePath)      #Convert the image to a QPixmap
        self.__controller = MoveRobot()                         #MoveRobot object
        self.__readwrite = JSONConverter("../data/longitude.txt", "../data/lattitude.txt","../data/altitude.txt")                      #JSONConverter object
        self.__speedSetting = 2                                     #Which speed rdo button is checked
        self.__option1 = False                  #Wether the four options are selected
        self.__option2 = False
        self.__option3 = False
        self.__option4 = False
        
        #Load the file 
        try:
            uic.loadUi(self.__guiPath, self)
        except TypeError:
            print("Error loading the .ui file, wrong type specified")
            tb = traceback.format_exc()
        except Exception:
            print("Error loading the .ui file, general failure")
            tb = traceback.format_exc()
        else:
            tb = "No error"
        finally:
            print(tb)
        
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
        #Set the action listeners for the menu items
        self.actionSaveCoordinates.triggered.connect(self.save)
        self.actionLoadCoordinates.triggered.connect(self.load)
        self.actionAbout.triggered.connect(self.about)
        #Set a default picture when there are no images that can be read
        self.lblFisheyeNormal.setPixmap(self.__noImagePixmap)
        self.lblFrontFacingNormal.setPixmap(self.__noImagePixmap)
        

        
    #-----
    #Functions for event handlers
    #-----

    #btnAdd
    def addCoordinates(self):
        """
        Whenever the btnAdd is clicked (Add Coordinates) trigger this action
        """
        #Get Lattitude Longitude and Altitude from the three QLineEdits text boxes
        self.__lattitude = self.txtLattitude.text()
        self.__longitude = self.txtLongitude.text()
        self.__altitude = self.txtAltitude.text()

        #Get the string version for output
        self.__strAltitude = str(self.__altitude)
        self.__strLattitude = str(self.__lattitude)
        self.__strLongitude = str(self.__longitude)
        
        #Append the data onto a list for use in other algorithms
        try:
            self.__lattitudeList.append(float(self.__lattitude))
            self.__longitudeList.append(float(self.__longitude))
            self.__altitudeList.append(float(self.__altitude))
            #Concantenate into a single string
            self.concantenateString()
        
            #Add to the list
            self.lstPoints.addItem(self.__coordString)
            #Clears the inputs for the next input
            self.clearData()
            self.txtLattitude.setFocus()
        except Exception:
            tb = traceback.format_exc()
            print("Error: invalid input")
            print(tb)
        


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

    #btnBegin
    def beginMovement(self):
        """
        Whenever the btnBegin is clicked (Begin Movement) trigger this action
        """
        #Check for each speed setting
        if(self.rdoLow.isChecked):
            self.__speedSetting = 1
        elif(self.rdoMedium.isChecked):
            self.__speedSetting = 2
        elif(self.rdoHigh.isChecked):
            self.__speedSetting = 3
        
        #Check for each setting
        if(self.chkPictures.isChecked):
            self.__option1 = True
        if(self.chkPictures2.isChecked):
            self.__option2 = True
            
        self.__controller.FollowCoordinates(self.__lattitudeList, self.__longitudeList, self.__speedSetting, self.__option1, self.__option2, self.__option3, self.__option4)

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
        self.__lattitudeList = []
        self.__longitudeList = []
        self.__altitudeList = []

    #actionSaveCoordinates
    def save(self):
        """
        Saves the current lists as a JSON text file
        """
        self.__readwrite.ListToJSON(self.__lattitudeList, self.__longitudeList, self.__altitudeList)

    def load(self):
        """
        Loads the saved list to the application
        """
        #Update by reading the files
        self.__readwrite.JSONToList()
        self.clearAll
        
        #Read from the files
        self.__lattitudeList = self.__readwrite.getLattitude()
        self.__longitudeList = self.__readwrite.getLongitude()
        self.__altitudeList = self.__readwrite.getAltitude()

        for i in range(len(self.__lattitudeList)):
            #Get the string version for output
            self.__strAltitude = str(self.__altitudeList[i])
            self.__strLattitude = str(self.__lattitudeList[i])
            self.__strLongitude = str(self.__longitudeList[i])
            #Concantenate into an output
            self.__coordString = str("Lat: " + self.__strLattitude) + "\t" + "   Long: " + str(self.__strLongitude) + "\t" + "   Alt: " + str(self.__strAltitude)
            self.lstPoints.addItem(self.__coordString)

        #Set focus to the beginning
        self.txtLattitude.setFocus()
    #Function clears the lattitude longitude and altitude input text widgets
    def clearData(self):
        """
        Resets the three input text boxes
        """
        self.txtLattitude.clear()
        self.txtLongitude.clear()
        self.txtAltitude.clear()

    def concantenateString(self):
        """
        Concantenates three data sets together
        """
        self.__coordString = str("Lat: " + self.__strLattitude) + "\t" + "   Long: " + str(self.__strLongitude) + "\t" + "   Alt: " + str(self.__strAltitude)

    

    def about(self):
        buttonAbout = QMessageBox.question(self, 'About This Application',
                                           "GPS Converter. \nVersion 1.0.0 \n\nThis program is to help read texts from specified files \nand convert the content to GPS coordinates.",
                                           QMessageBox.Ok, QMessageBox.Ok)

        
        

#Test if this is being run directly or being imported as a class
if __name__ == '__main__':
    #Launch the program
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
