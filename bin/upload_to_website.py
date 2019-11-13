import requests
import os
class UploadToWebsite:
    """This class uploads a post request to the url"""
    def __init__(self):
        """Constructor, declares private fields"""
        self.__url = "http://phrec-irrigation.com/robot/upload" #Url to send the post
        self.__imagePath = "C:/Users/dsmith129/Documents/GitHub/Robot/bin/data/fisheye"
        self.__imageDirectory = os.fsencode(self.__imagePath)         #Loads the filename of the image folder with correct operating system compatibility use fsdecode to access
        
    def upload_images(self):
        """Upload all the images within the images folder to the specified website url with a post method"""
        #Loop through the files in the image directory
        for self.filename in os.listdir(self.__imageDirectory):
            #Load the filename wit
            self.fileName = os.fsdecode(self.filename)
            #As long as an image file is found, upload, otherwise continue the loop, skipping the file.
            if(self.fileName.endswith("jpeg") or self.fileName.endswith("jpg") or self.fileName.endswith("png")):

                self.imageFileDescriptor = open(self.__imagePath + "/" + self.fileName, 'rb')
                self.files = {'fileToUpload': self.imageFileDescriptor}
                requests.post(self.__url, files=self.files)
                #Close the loaded file, prevents bugs
                self.imageFileDescriptor.close()
                continue
            #Otherwise, continue the loop, passing the file
            else:
                continue
test = UploadToWebsite()
test.upload_images()