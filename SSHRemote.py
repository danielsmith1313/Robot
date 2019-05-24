import subprocess

class SSHRemote():
    def __init__(self):
        self.__remoteIPAddress = ""
        self.__scriptPath = ""

    @classmethod
    def SendSignalToTakePicture(self, IPIn, scriptName):
        """
        Sends a signal to the second raspberry pi using ssh
        telling it to take a picture. 
        """
        subprocess.open("ssh pi@" + IPIn + " 'cd ~ && python " + scriptName + "'", shell=True)
    
    


    