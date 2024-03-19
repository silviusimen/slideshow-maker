from .cacheable_object import CacheableObject
from .cache import Cache
from .geolocation import Geolocation


class Metadata(CacheableObject):
    def __init__(self, name: str, timestamp=None, geo=None):
        super().__init__(name)
        self.set("name", name)
        self.set("ts", timestamp)
        self.set("geo", geo)

    def get_fields_to_unserialize(self):
        return {"geo": (lambda: Geolocation())}
