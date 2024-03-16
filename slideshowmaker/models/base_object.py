from collections import UserDict
import json


class BaseObject(UserDict):
    def __init__(self):
        UserDict.__init__(self)

    def _set(self, name: str, value) -> None:
        setattr(self, name, value)
        self[name] = value

    def to_dict(self) -> dict:
        return dict(self)

    def json_print(self) -> None:
        print(json.dumps(self.to_dict(), indent=4))
