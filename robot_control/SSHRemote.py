import subprocess

class SSHRemote():
    def __init__(self):
        pass

    @classmethod
    def SendSignalToRunScript(self, IPIn, scriptName):
        """
        Sends a signal to the second raspberry pi using ssh
        telling it to take a picture. 
        """
        subprocess.open("ssh pi@" + IPIn + " 'cd ~ && python " + scriptName + "'", shell=True)
    
    


    