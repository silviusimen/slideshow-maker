from .base_object import SerializableObject


class Geolocation(SerializableObject):
    def __init__(self, lat: float = None, lon: float = None):
        SerializableObject.__init__(self)
        self.set("lat", lat)
        self.set("lon", lon)
