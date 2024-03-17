from abc import abstractmethod


class Cache:
    def __init__(self):
        self.cache = dict()

    def get(self, key: str):
        if key in self.cache:
            return self.cache[key]
        return None

    def delete(self, key: str):
        del self.cache[key]

    def set(self, key: str, value):
        self.cache[key] = value
