from .base_object import SerializableObject
from .cache import Cache


class CacheableObject(SerializableObject):
    def __init__(self, name: str):
        SerializableObject.__init__(self)
        self.__cache_name = name

    def save_to_cache(self, cache: Cache):
        cache.set(self.__cache_name, self.serialize())

    def load_from_cache(self, cache: Cache) -> bool:
        d = cache.get(self.__cache_name)
        if d != None:
            self.unserialize(d)
            return True
        else:
            return False
