#Operating system compatibility
import os

#SSH remote class
from .SSHRemote import SSHRemote
#Low level networking library
import socket
import json
#INFO: Executable file that is remotely run to take a picture and send the picture back to the recieving end, 
# in this case another raspberry pi
recievingIP = ""
filename = "run_import.py"
#Take picture here and export it to the other pi as an array
pic = []

#export the data using socket
data = json.dumps({"A": pic})
socket.send(data.encode)

#Tell the socket to recieve data
SSHRemote.SendSignalToRunScript(recievingIP,)