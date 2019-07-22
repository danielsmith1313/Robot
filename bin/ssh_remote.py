#Filename: ssh_remote.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith

import subprocess

class SSHRemote():
    """
    This static class is in charge of sending an ssh signal to another ip address on the network to run a script
    NOTE: depending on which linux deployment is being used, ssh may need to be enabled for this script to work
    """
    def __init__(self):
        pass

    @classmethod
    def SendSignalToRunScript(self, IPIn, scriptName):
        """
        Sends a signal to the second raspberry pi using ssh
        telling it to take a picture. 
        """
        subprocess.open("ssh pi@" + IPIn + " 'cd ~ && python " + scriptName + "'", shell=True)
    
    


    