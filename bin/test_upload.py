
import requests
url = 'http://phrec-irrigation.com/robot/upload'

files = {"fileToUpload" : open("./test.jpeg", 'rb')}
r = requests.post(url, files = files)

print(r.text) 