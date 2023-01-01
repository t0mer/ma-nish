import json
from json import JSONEncoder
from geopy.geocoders import Nominatim
class Location(object):
    name: str
    address: str
    latitude: str
    longitude: str

    def __init__(self, name: str =None, address: str=None, latitude: str=None, longitude: str=None):
        """
        Create Location object.
        If latitude or longitude are None or Empty, i will generate it from address using [GeoPy](https://geopy.readthedocs.io/en/stable/)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.address = address

        if self.latitude is None or self.longitude is None:
            geolocator = Nominatim(user_agent = "MaNish")
            location = geolocator.geocode(address)
            self.latitude = location.latitude
            self.longitude = location.longitude

class LocationEncoder(JSONEncoder):
    """
    Returns Location object as json
    """
    def default(self, o):
        return o.__dict__
