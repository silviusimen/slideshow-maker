from .base_object import BaseObject


class Geolocation(BaseObject):
    def __init__(self, lat: float = None, lon: float = None):
        BaseObject.__init__(self)
        self._set("lat", lat)
        self._set("lon", lon)
