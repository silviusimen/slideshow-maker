from .base_object import BaseObject


class Metadata(BaseObject):
    def __init__(self, name: str = None, timestamp=None):
        BaseObject.__init__(self)
        self._set("name", name)
        self._set("ts", timestamp)
