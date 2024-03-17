from collections import UserDict
import json


class SerializableObject(UserDict):
    def __init__(self, **kwargs):
        UserDict.__init__(self)
        for key, value in kwargs.items():
            self.set(key, value)

    def set(self, name: str, value) -> None:
        setattr(self, name, value)
        self[name] = value

    def get(self, name: str):
        return self[name]

    def serialize(self) -> dict:
        d = dict(self)
        for k in d.keys():
            if isinstance(d[k], SerializableObject):
                d[k] = d[k].serialize()
        return d

    def unserialize(self, d: dict) -> None:
        for k in d.keys():
            self.set(k, d[k])

    def json_print(self) -> None:
        print(json.dumps(self.serialize(), indent=4))
