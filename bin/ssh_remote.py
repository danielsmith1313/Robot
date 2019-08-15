#Filename: ssh_remote.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith

from subprocess import Popen, PIPE
import subprocess
import sys
import os
import paramiko
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
        #proc = subprocess.run(["ssh","pi@"+IPIn," sudo python3 "+scriptName],stdin=PIPE)
        
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect('<hostname>', username='<username>', password='<password>', key_filename='<path/to/openssh-private-key-file>')

        stdin, stdout, stderr = ssh.exec_command(["ssh","pi@"+IPIn," sudo python3 "+scriptName])
        print(stdout.readlines())
        ssh.close()
    
    


    