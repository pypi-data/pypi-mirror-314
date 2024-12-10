from enum import Enum


class PersistentEnum(Enum):
    Memory = "memory"
    TinyDB = "tinydb"
    Mysql = "mysql"
