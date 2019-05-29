#Filename: import_image.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith

import socket
import json

class ImportImage():
    """
    This class is in charge of recieving socket data from an external source and saving it as a file
    """
    def __init__(self):
        #Declare variables
        self.__data = []
        self.__arr
        self.pic = 0
    def RecieveImage(self):
        """
        Reads an image from a socket and writes it to a file
        """
        self.__data = socket.recv(1024)
        self.__data = json.loads(self.__data.decode())
        
        
    def GetImage(self):
        """
        Return the image read
        """
        pass