from .cacheable_object import CacheableObject
from .cache import Cache
from .geolocation import Geolocation


class Metadata(CacheableObject):
    def __init__(self, name: str, timestamp=None, geo=None):
        CacheableObject.__init__(self, name)
        self.set("name", name)
        self.set("ts", timestamp)
        self.set("geo", geo)

    def load_from_cache(self, cache: Cache) -> bool:
        loadad = CacheableObject.load_from_cache(self, cache)
        if loadad:
            geo_dict = self.get("geo")
            geo = Geolocation()
            geo.unserialize(geo_dict)
            self.set("geo", geo)
        return loadad
