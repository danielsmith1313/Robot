#Filename: run_import.py
#Author: Daniel Smith
#Created: 5/23/2019
#Last edited: 5/29/2019 by Daniel Smith

"""
This file is an executable script used by an external ssh_remote.py file in order to execute an image import
"""

from .ImportImage import ImportImage
imageHandler = ImportImage()
imageHandler.RecieveImage()
