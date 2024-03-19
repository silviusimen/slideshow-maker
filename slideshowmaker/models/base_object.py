from collections import UserDict
from typing import Callable

import json


class SerializableObject(UserDict):
    def __init__(self, **kwargs):
        super().__init__()
        self.unserialize(kwargs)

    def set(self, name: str, value) -> None:
        setattr(self, name, value)
        self[name] = value

    def get(self, name: str):
        return self[name]

    def serialize(self) -> dict:
        d = dict(self)
        for key, value in d.items():
            if isinstance(value, SerializableObject):
                d[key] = value.serialize()
        return d

    def unserialize(self, d: dict) -> None:
        for key, value in d.items():
            self.set(key, value)

    def json_print(self) -> None:
        print(json.dumps(self.serialize(), indent=4))

    def load_field(self, name: str, type_generator: Callable) -> bool:
        d = self.get(name)
        ser_object = type_generator()
        ser_object.unserialize(d)
        self.set(name, ser_object)
