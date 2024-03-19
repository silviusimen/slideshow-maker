from ..models.cache import Cache
from ..models.geolocation import Geolocation
from .tile_manager import TileManager

from PIL import Image
from .map import Map, MAP_DEFAULT_ZOOM, MAP_DEFAULT_SIZE_X, MAP_DEFAULT_SIZE_Y

import math

# https://stackoverflow.com/questions/28476117/easy-openstreetmap-tile-displaying-for-python
# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
# https://wiki.openstreetmap.org/wiki/Raster_tile_providers
# https://wiki.openstreetmap.org/wiki/Zoom_levels
# https://{a|b|c}.tile.opentopomap.org/{z}/{x}/{y}.png


def deg2num(lat_deg: float, lon_deg: float, zoom: int):
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


def num2deg(xtile: int, ytile: int, zoom: int):
    n = 1 << zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def zoom_to_tile_degree(zoom: int) -> float:
    n = 1 << zoom
    width_deg = 360.0 / n
    return width_deg


class Map_OSM(Map):
    def __init__(self, tile_manager: TileManager):
        self.tile_manager = tile_manager

    def get_url(geo: Geolocation, zoom: int = 19) -> str:
        return f"https://www.openstreetmap.org/#map={zoom}/{geo.lat}/{geo.lon}"

    def getTileRanges(self, geo: Geolocation, zoom: int):
        delta = zoom_to_tile_degree(zoom)
        xmin, ymin = deg2num(geo.lat - delta / 2, geo.lon - delta / 2, zoom)
        xmax, ymax = deg2num(geo.lat + delta / 2, geo.lon + delta / 2, zoom)
        return (xmin, ymin, xmax, ymax)

    def getImageCluster(self, geo: Geolocation, zoom: int):
        xmin, ymin, xmax, ymax = self.getTileRanges(geo, zoom)

        Cluster = Image.new(
            "RGB", ((xmax - xmin + 1) * 256 - 1, (ymax - ymin + 1) * 256 - 1)
        )
        for xtile in range(xmin, xmax + 1):
            for ytile in range(ymin, ymax + 1):
                try:
                    tyle_bytes = self.tile_manager.getTileAsBytes(zoom, xtile, ytile)
                    tile = Image.open(tyle_bytes)
                    Cluster.paste(
                        tile, box=((xtile - xmin) * 255, (ytile - ymin) * 255)
                    )
                except Exception as e:
                    print(e)
                    tile = None

        return Cluster

    def render_map_image(
        self,
        geo: Geolocation,
        zoom: int = MAP_DEFAULT_ZOOM,
        sizex: int = MAP_DEFAULT_SIZE_X,
        sizey: int = MAP_DEFAULT_SIZE_Y,
    ) -> Image:
        a = self.getImageCluster(geo, zoom)
        return a
