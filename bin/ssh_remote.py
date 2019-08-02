#Filename: ssh_remote.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith

import subprocess

class SSHRemote():
    """
    This static class is in charge of sending an ssh signal to another ip address on the network to run a script
    NOTE: depending on which linux deployment is being used, ssh may need to be enabled for this script to work
    Main pi last IP: 169.254.124.81
    Secondary pi last IP: 169.254.247.170
    """
    def __init__(self):
        pass

    @classmethod
    def SendSignalToRunScript(self, IPIn, scriptName):
        """
        Sends a signal to the second raspberry pi using ssh
        telling it to take a picture. 
        """
        subprocess.run("sshpass -p 'Password01' ssh pi@" + IPIn + " 'python3 " + scriptName + "'", shell=True)
    
    


    