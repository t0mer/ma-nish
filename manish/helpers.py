import os
import json
import time
import requests
from os import path
from urllib.parse import urlparse
from PIL import Image
from loguru import logger
class Helpers:
    def __init__(self):
        self.temp_directory = os.getcwd() + "/temp"
        self.create_temp_directory()

    def create_temp_directory(self):
        if not os.path.isdir(self.temp_directory):
            os.makedirs(self.temp_directory) 


    def download_file(self,url):
        """
        Saving remote file to local pash.
        """
        file = requests.get(url)
        open(self.temp_directory +"/" + os.path.basename(urlparse(url).path), "wb").write(file.content)
        return self.temp_directory +"/" +  os.path.basename(urlparse(url).path)   


    def convert_to_webp(self,source):
        logger.info(source)
        """Convert image to WebP.

        Args:
            source (pathlib.Path): Path to source image

        Returns:
            pathlib.Path: path to new image
        """
        destination = str(os.path.splitext(source)) +".webp"

        image = Image.open(source)  # Open image
        image.save(destination, format="webp")  # Convert image to webp

        return destination