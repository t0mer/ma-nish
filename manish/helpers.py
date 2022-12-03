import os
import json
import time
import requests
from os import path
from urllib.parse import urlparse


class Helpers:
    def __init__(self):
        self.temp_directory = os.getcwd() + "/temp"
        self.create_temp_directory()

    def create_temp_directory(self):
        if not os.path.isdir(self.temp_directory):
            os.makedirs(self.temp_directory) 


    def download_file(self,url):
        file = requests.get(url)
        open(self.temp_directory +"/" + os.path.basename(urlparse(url).path), "wb").write(file.content)
        return self.temp_directory +"/" +  os.path.basename(urlparse(url).path)   


