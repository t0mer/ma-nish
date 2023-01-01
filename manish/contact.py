import json
from json import JSONEncoder
from enum import Enum

class Contact(object):
    """
    Whatsapp Contact object
    Args:
        >>> name: Name object (formatted_name, First, Last, etc.)
        >>> addresses: List of addresses
        >>> emails: List of email addresses
        >>> phones: List of email addresses
    """
    def __init__(self, name, addresses: list = [], emails: list = [], phones: list = []):
        self.name = name
        self.addresses = addresses
        self.emails = emails
        self.phones = phones


class ContactEncoder(JSONEncoder):
    """
    Return Contact object as json
    """
    def default(self, o):
        return o.__dict__



class Address(object):
    street: str
    cist: str
    state: str
    zip: str
    country: str
    country_code: str
    type: str

    def __init__(self, street:str = "", city: str = "", state: str = "",zip: str="", country: str = "", country_code: str = "", type: str = ""):
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.country_code = country_code
        self.type = type


class Email(object):
    email: str
    type: str

    def __init__(self, email:str = "", type: str = ""):
        self.email = email
        self.type = type


class Name(object):
    formatted_name: str
    first_name: str
    last_name: str
    middle_name: str
    suffix: str
    prefix: str

    def __init__(self, formatted_name: str, first_name: str = "", last_name: str = "", middle_name: str = "",suffix: str = "", prefix: str = ""):
        self.formatted_name = formatted_name
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.suffix = suffix
        self.prefix = prefix

class Phone(object):
    phone: str
    type: str
    wa_id: str

    def __init__(self, phone:str = "", type: str = "", wa_id: str=""):
        self.phone = phone
        self.type = type
        self.wa_id = wa_id


class Url(object):
    url: str
    type: str

    def __init__(self, url: str = "", type: str = ""):
        self.url = url
        self.type = type
