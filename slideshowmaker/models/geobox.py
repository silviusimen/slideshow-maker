from .base_object import SerializableObject
from .geolocation import Geolocation


class GeoBox(SerializableObject):
    def __init__(self, min: Geolocation = None, max: Geolocation = None):
        SerializableObject.__init__(self)
        self.set("min", min)
        self.set("max", max)

    def get_fields_to_unserialize(self):
        return {"min": (lambda: Geolocation()), "max": (lambda: Geolocation())}
