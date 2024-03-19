from .base_object import SerializableObject


class Geolocation(SerializableObject):
    def __init__(self, lat: float = None, lon: float = None):
        super().__init__()
        self.set("lat", lat)
        self.set("lon", lon)
