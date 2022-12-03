import json


class address(object):
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


class email(object):
    email: str
    type: str

    def __init__(self, email:str = "", type: str = ""):
        self.email = email
        self.type = type


class name(object):
    formated_name: str
    first_name: str
    last_name: str
    middle_name: str
    suffix: str
    prefix: str

    def __init__(self, formated_name: str, first_name: str = "", last_name: str = "", middle_name: str = "",suffix: str = "", prefix: str = ""):
        self.formated_name = formated_name
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.suffix = suffix
        self.prefix = prefix

class phone(object):
    phone: str
    type: str
    wa_id: str

    def __init__(self, phone:str = "", type: str = "", wa_id: str=""):
        self.phone = phone
        self.type = type
        self.wa_id = wa_id


class url(object):
    url: str
    type: str

    def __init__(self, url: str = "", type: str = ""):
        self.url = url
        self.type = type