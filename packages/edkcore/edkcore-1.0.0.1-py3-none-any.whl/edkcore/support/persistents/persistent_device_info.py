from dataclasses import dataclass
from typing import Any


@dataclass
class PersistentDeviceInfo:
    name: str
    clazz: Any
    configuration: dict
