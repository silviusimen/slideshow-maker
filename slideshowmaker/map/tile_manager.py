from .cached_http_requests import CachedHttpRequest
from ..models.cache import Cache


from io import BytesIO


class TileManager(CachedHttpRequest):
    def __init__(self, cache: Cache):
        super().__init__(cache)

    def getTileAsBytes(self, zoom: int, xtile: int, ytile: int) -> BytesIO:
        smurl = r"https://a.tile.opentopomap.org/{0}/{1}/{2}.png"
        # smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
        imgurl = smurl.format(zoom, xtile, ytile)
        image_bytes = self.get(
            imgurl, headers={"User-Agent": "SlideShow Generator/1.0"}
        )
        return image_bytes
