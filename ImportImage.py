import socket
import json

class ImportImage():
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