#Importing the necessary modules and libraries to help access
#specific functions for this program
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
        #Declare fields
        self.__lattitudeList = []           #Contains the lattitude of all inputs
        self.__longitudeList = []           #Contains the longitude of all inputs
        self.__altitudeList = []            #Contains the altitude of all the inputs
        self.__coordString = ""             #Contains the concantenated string to output to the application
    
        
        #Load the graphical ui file 
        uic.loadUi('../../resources/gps_converter.ui', self)
        
        #Setup widgets and event handlers
        self.setupUI()
        
        #Set it able to be seen
        self.show()
    
    
    def setupUI(self):
        #The widgets are already created, however in order to add listeners to them they must be manually added here
        self.btnLoadNewFile.clicked.connect(self.loadNewFile)
        self.btnRemoveCoordinates.clicked.connect(self.removeCoordinates)
        self.btnConvertToGPSCoordinates.clicked.connect(self.convertToGPSCoordinates)
        self.btnSaveCoordinates.clicked.connect(self.showSaveDialog)
        self.btnClearAll.clicked.connect(self.clearAll)
        
        #Set the action listeners for the menu items
        self.actionLoad_New_File.triggered.connect(self.loadNewFile)
        self.actionSave.triggered.connect(self.showSaveDialog)
        self.actionExit.triggered.connect(self.exit)
        self.actionAbout.triggered.connect(self.about)

        
    #-----
    #Functions for event handlers
    #-----         
    
                
    #btnloadNewFile
    def loadNewFile(self):
        
        #Read from the files
        """
        self.__lattitudeList = [2,3,432,234,45,4546,897,5,7,32,234,432,234,45,4546,897]
        self.__longitudeList = [2,3,5,7,32,234,44,234,87,67,900,432,234,45,4546,897]
        self.__altitudeList = [2,32,34,56,32,234,55,234,45,65,897,432,234,45,4546,897]     

        for i in range(len(self.__lattitudeList)):
            #Get the string version for output
            self.__strAltitude = str(self.__altitudeList[i])
            self.__strLattitude = str(self.__lattitudeList[i])
            self.__strLongitude = str(self.__longitudeList[i])
            self.__coordString = str("Lat: " + self.__strLattitude) +'\t' + "   Long: " + str(self.__strLongitude) +'\t' + "   Alt: " + str(self.__strAltitude)
            self.loadList.addItem(self.__coordString)
        """

        #Verify from the user if they want to load a new file
        #because that will clear any data that already exists in the arrays for the coordinates
        buttonLoadFile = QMessageBox.question(self, 'Load New File',
                                              "Do you want to load a new file? \nDoing this will clear the existing data from the display boxes!",
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        #If the user chooses yes, open the file the user chooses and read the GPS coordinates from the file else do nothing
        if buttonLoadFile == QMessageBox.Yes:
            try:
                self.clearAll()
                path,_ = QtWidgets.QFileDialog().getOpenFileName(self,"Imported","","CSV Files (*.csv)")
                with open(path) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=',')
                    for row in readCSV:
                        lat = row[0]
                        long = row[1]
                        alt = row[2]

                        self.__lattitudeList.append(int(lat))
                        self.__longitudeList.append(int(long))
                        self.__altitudeList.append(int(alt))
                        self.__coordString = str("Lat: " + lat) +'\t' + "   Long: " + str(long) +'\t' + "   Alt: " + str(alt)
                        self.loadList.addItem(self.__coordString)
            except Exception as e:
                print (e)
        else:
            pass


    #btnRemoveCoordinates
    def removeCoordinates(self):
        """
        Whenever the btnRemoveCoordinates is clicked (Remove Coordinates) trigger this action
        """
        try:
            selectedIndex = self.loadList.currentRow()
            del(self.__lattitudeList[selectedIndex])
            del(self.__longitudeList[selectedIndex])
            del(self.__altitudeList[selectedIndex])
            self.loadList.takeItem(selectedIndex)

        except Exception as e:
            buttonMessage = QMessageBox.question(self, 'Error!', 'Please select the coordinates to remove first', QMessageBox.Ok, QMessageBox.Ok)

        

    #btnConvertToGPSCoordinates
    def convertToGPSCoordinates(self):
        try:
            
            self.convertedLatList = []
            self.convertedLongList = []
            self.convertedAltList = []

            for i in range(len(self.__lattitudeList)):
                self.convertedLatList.append((self.__lattitudeList[i] + self.__lattitudeList[i+1]) / 2)
                self.convertedLongList.append((self.__longitudeList[i] + self.__longitudeList[i+1]) / 2)
                self.convertedAltList.append(self.__altitudeList[i])
                self.__convertedCordString = "Lat: " + str(self.convertedLatList[i]) +'\t' + "   Long: " + str(self.convertedLongList[i]) +'\t' + "   Alt: " + str(self.convertedAltList[i])
                self.convertedList.addItem(self.__convertedCordString)

        except Exception as e:
            print (e)


    #btnSaveCoordinates
    def saveCoordinates(self):
        lattitude = open("../../data/lattitude.txt","w")
        lattitude.write(str(self.convertedLatList))
        lattitude.close()

        longitude = open("../../data/longitude.txt","w")
        longitude.write(str(self.convertedLongList))
        longitude.close()

        altitude = open("../../data/altitude.txt","w")
        altitude.write(str(self.convertedAltList))
        altitude.close()

        buttonConfirmSaveNotSaved = QMessageBox.question(self, 'Saved!', "GPS coordinates have been saved.", QMessageBox.Ok, QMessageBox.Ok)


    def showSaveDialog(self):
        try:
            buttonSaveReply = QMessageBox.question(self, 'Save Coordinates',
                                                   "Do you want to overwrite and save the new GPS coordinates?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonSaveReply == QMessageBox.Yes:
                self.saveCoordinates()
            else:
                pass
            
        except Exception as e:
            buttonMessage = QMessageBox.question(self, 'Error!', 'There were no GPS coordinates to save!', QMessageBox.Ok, QMessageBox.Ok)

    #btnClearAll
    def clearAll(self):
        """
        Whenever the btnClear is clicked (Clear All) trigger this action
        """
        #Clear the display
        self.loadList.clear()
        #Clear the list box for the converted GPS Coordinates
        self.convertedList.clear()
        #Reset the double data
        self.__lattitudeList = []
        self.__longitudeList = []
        self.__altitudeList = []
    

    def exit(self):
        buttonReply = QMessageBox.question(self, 'Close Application', "Are you sure you want to close the application?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            sys.exit()
        else:
            pass


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
    
