from dataclasses import dataclass


@dataclass
class DataInfo:
    dataType: str
    name: str
    inputBy: str
    userInput: str
    getter_class: str
    persistence_ref: str
    persistence_class: str
    serialize_class: str
