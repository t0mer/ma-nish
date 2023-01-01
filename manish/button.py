from typing import List
from json import JSONEncoder

class Row:
    id: str
    title: str
    description: str

    def __init__(self, id: str, title: str, description: str) -> None:
        self.id = id
        self.title = title
        self.description = description


class Section:
    title: str
    rows: List[Row]

    def __init__(self, title: str, rows: List[Row]) -> None:
        self.title = title
        self.rows = rows


class Action:
    button: str
    sections: List[Section]

    def __init__(self, button: str, sections: List[Section]) -> None:
        self.button = button
        self.sections = sections


class Button:
    header: str
    body: str
    footer: str
    action: Action

    def __init__(self, header: str, body: str, footer: str, action: Action) -> None:
        self.header = header
        self.body = body
        self.footer = footer
        self.action = action



class ButtonEncoder(JSONEncoder):
    """
    Returns Button object as json
    """
    def default(self, o):
        return o.__dict__

