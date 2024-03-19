from ..models.cache import Cache

import requests
import base64
from io import BytesIO

class CachedHttpRequest:
    def __init__(self, cache: Cache):
        self.cache = cache
        self.__cache_prefix = "http_cache_"

    def get(self, url: str, headers: dict) -> BytesIO:
        cache_key = self.__cache_prefix + url
        tile_cache = self.cache.get(cache_key)
        if tile_cache != None:
            return BytesIO(base64.b64decode(tile_cache))

        response = requests.get(
            url, headers=headers
        )

        cache_value = base64.b64encode(response.content).decode("ascii")
        self.cache.set(cache_key, cache_value)
        # self.cache.save()
        result_bytes = BytesIO(response.content)
        return result_bytes
