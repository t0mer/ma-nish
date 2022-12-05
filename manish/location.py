import json
from json import JSONEncoder
from geopy.geocoders import Nominatim
class Location(object):
    name: str
    address: str

    def __init__(self, name: str ="", address: str = ""):
        self.latitude = None
        self.longitude = None
        self.name = name
        self.address = address

        geolocator = Nominatim(user_agent = "MaNish")
        location = geolocator.geocode("הגליל 48 רעננה")
        self.latitude = location.latitude
        self.longitude = location.longitude



class LocationEncoder(JSONEncoder):
    """
    Methon to json encode
    """
    def default(self, o):
        return o.__dict__
