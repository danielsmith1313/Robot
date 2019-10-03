#Note: Untested
import dropbox, sys, os

dbx = dropbox.Dropbox('zKAyq68NMfAAAAAAAAAALCvDPQzGNLaxSsZAWYEURF_lOxfoY3hdFkNrRlox41-n')
rootdir = '../resources' 

print ("Attempting to upload...")
# walk return first the current folder that it walk, then tuples of dirs and files not "subdir, dirs, files"
for dir, dirs, files in os.walk(rootdir):
    for file in files:
        try:
            file_path = os.path.join(dir, file)
            dest_path = os.path.join('/test', file)
            print('Uploading '+file_path+ ' to ' + dest_path)
            with open(file_path) as f:
                dbx.files_upload(f, dest_path, mute=True)
        except Exception as err:
            print("Upload failed "+ file + " " + err)

print("Finished upload.")