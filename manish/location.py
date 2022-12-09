import json
from json import JSONEncoder
from geopy.geocoders import Nominatim
class Location(object):
    name: str
    address: str
    latitude: str
    longitude: str

    def __init__(self, name: str ="", address: str="", latitude: str="", longitude: str=""):
        self.latitude = None
        self.longitude = None
        self.name = name
        self.address = address

        if self.latitude == "" or self.longitude == "":
            geolocator = Nominatim(user_agent = "MaNish")
            location = geolocator.geocode(address)
            self.latitude = location.latitude
            self.longitude = location.longitude

class LocationEncoder(JSONEncoder):
    """
    Methon to json encode
    """
    def default(self, o):
        return o.__dict__
