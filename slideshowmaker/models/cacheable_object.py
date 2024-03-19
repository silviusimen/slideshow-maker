from .base_object import SerializableObject
from .cache import Cache


class CacheableObject(SerializableObject):
    def __init__(self, name: str):
        super().__init__()
        self.__cache_name = name

    def save_to_cache(self, cache: Cache):
        cache.set(self.__cache_name, self.serialize())

    def load_from_cache(self, cache: Cache) -> bool:
        d = cache.get(self.__cache_name)
        if d != None:
            self.unserialize(d)
            fields = self.get_fields_to_unserialize()
            for field_name in fields.keys():
                field_creator = fields[field_name]
                self.load_field(field_name, field_creator)
            return True
        else:
            return False

    def get_fields_to_unserialize(self):
        return dict()
