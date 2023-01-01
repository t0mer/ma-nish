from typing import Optional, List
import json
from json import JSONEncoder
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json


class Currency:
    fallback_value: str
    code: str
    amount_1000: int

    def __init__(self, fallback_value: str, code: str, amount_1000: int) -> None:
        self.fallback_value = fallback_value
        self.code = code
        self.amount_1000 = amount_1000

class Media:
    id: str
    link: str
    def __init__(self, id: str="", link: str="") -> None:
        self.id = id
        self.link = link

class Parameter:
    type: str
    text: Optional[str]

    def __init__(self, type: str, text: Optional[str]) -> None:
        self.type = type
        self.text = text


class CurrencyParameter:
    type: str
    currency: Optional[Currency] 
    def __init__(self, type: str, currency: Optional[Currency]) -> None:
        self.type = type
        self.currency = currency


class MediaParameter:
    type: str
    image: Media

    def __init__(self, type: str, image: Media) -> None:
        self.type = type
        self.image = image
        

class Component:
    type: str
    parameters: List[Parameter]

    def __init__(self, type: str, parameters: List[Parameter]) -> None:
        self.type = type
        self.parameters = parameters

class Components:
    components: List[Component]

    def __init__(self, components: List[Component]):
        self.components = components

class TemplateEncoder(JSONEncoder):
    """
    Returns Template object as json
    """
    def default(self, o):
        return o.__dict__


