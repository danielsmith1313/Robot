import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime

#This program loads 

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if it can not be found
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
#authentication.
drive = GoogleDrive(gauth)

#Create folder
fisheyeFolderMetadata = {'title':'Fisheye '+ str(datetime.datetime.now()), 'mimeType' : 'application/vnd.google-apps.folder'}
fisheyeFolder = drive.CreateFile(fisheyeFolderMetadata)
fisheyeFolder.Upload()


#Find folder info
fisheyeFolderTitle = fisheyeFolder['title']
fisheyeFolderID = fisheyeFolder['id']


rootdir = 'C:/Users/dsmith129/Documents/GitHub/Robot/bin/data'
#Go through every single file and upload to Drive
for subdir,dirs,files in os.walk(rootdir):
    for file in files:
        fileToUpload = os.path.join(subdir, file)
        newFile = drive.CreateFile({'title':os.path.basename(fileToUpload), 'parents':[{'kind': 'drive#fileLink', 'id': fisheyeFolderID}]})
        newFile.SetContentFile(fileToUpload)
        newFile.Upload()
