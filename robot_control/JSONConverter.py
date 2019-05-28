import json

class JSONConverter():
    def __init__(self, longitudePath, lattitudePath, altitudePath):
        self.__lattitude = []
        self.__longitude = []
        self.__altitude = []
        self.__longitudePath = longitudePath
        self.__lattitudePath = lattitudePath
        self.__altitudePath = altitudePath

    def VehicleDataToJSON(self, path):
        """
        Converts the file of points from the given path to the file
        """
        pass
    def ListToJSON(self, lattitude, longitude, altitude):
        """
        Converts three lists to a JSON file
        """
        with open(self.__lattitudePath, "w") as f:
            json.dump(lattitude, f, ensure_ascii=False)
        with open(self.__longitudePath, "w") as f:
            json.dump(longitude, f, ensure_ascii=False)
        with open(self.__altitudePath, "w") as f:
            json.dump(altitude, f, ensure_ascii= False)
        
    def JSONToList(self):
        """
        Converts JSON to Longitude Lattitude and Altitude lists
        """
        with open(self.__lattitudePath) as f:
            self.__lattitude = json.load(f)
        with open(self.__longitudePath) as f:
            self.__longitude = json.load(f)
        with open(self.__altitudePath) as f:
            self.__altitude = json.load(f)

    #-----
    #Getters and setters
    #-----
    def getLongitude(self):
        return self.__longitude
    def getLattitude(self):
        return self.__lattitude
    def getAltitude(self):
        return self.__altitude