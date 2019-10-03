import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#1st authentification
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles 
#authentication.
drive = GoogleDrive(gauth)

rootdir = 'C:/Users/dsmith129/Documents/GitHub/Robot/bin/data'
for subdir,dirs,files in os.walk(rootdir):
    for file in files:
        fileToUpload = os.path.join(subdir, file)
        newFile = drive.CreateFile({'RowBot': os.path.basename(fileToUpload)})
        newFile.SetContentFile(fileToUpload)
        newFile.Upload()
