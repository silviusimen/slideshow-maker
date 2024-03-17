import json

from .models.cache import Cache


class FileCache(Cache):
    def __init__(self, filenme: str):
        Cache.__init__(self)
        self.filename = filenme

    def load(self):
        try:
            new_cache = dict()
            with open(self.filename, mode="r") as file:
                data = file.read()
                new_cache = json.loads(data)
            self.cache.clear()
            self.cache.update(new_cache)
        except:
            pass

    def save(self):
        str_data = json.dumps(self.cache, indent=4)
        with open(self.filename, "w") as outfile:
            print(str_data, file=outfile)
