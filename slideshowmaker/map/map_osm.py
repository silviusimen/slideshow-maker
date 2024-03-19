from ..models.cache import Cache
from ..models.geolocation import Geolocation
from .tile_manager import TileManager
import geotiler
from PIL import Image
from .map import Map, MAP_DEFAULT_ZOOM, MAP_DEFAULT_SIZE_X, MAP_DEFAULT_SIZE_Y

import math

# import urllib3
import requests
import base64
from io import BytesIO

# import urllib2
# import StringIO


# https://stackoverflow.com/questions/28476117/easy-openstreetmap-tile-displaying-for-python
# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
# https://wiki.openstreetmap.org/wiki/Raster_tile_providers
# https://{a|b|c}.tile.opentopomap.org/{z}/{x}/{y}.png


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 1 << zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


def num2deg(xtile, ytile, zoom):
    n = 1 << zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


class Map_OSM(Map):
    def __init__(self, tile_manager: TileManager):
        self.tile_manager = tile_manager

    def get_url(geo: Geolocation, zoom: int = 19) -> str:
        return f"https://www.openstreetmap.org/#map={zoom}/{geo.lat}/{geo.lon}"

    def getImageCluster(self, lat_deg, lon_deg, delta_lat, delta_long, zoom):
        xmin, ymax = deg2num(lat_deg, lon_deg, zoom)
        xmax, ymin = deg2num(lat_deg + delta_lat, lon_deg + delta_long, zoom)

        bbox_ul = num2deg(xmin, ymin, zoom)
        bbox_ll = num2deg(xmin, ymax + 1, zoom)
        # print bbox_ul, bbox_ll

        bbox_ur = num2deg(xmax + 1, ymin, zoom)
        bbox_lr = num2deg(xmax + 1, ymax + 1, zoom)
        # print bbox_ur, bbox_lr

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

        return Cluster, [bbox_ll[1], bbox_ll[0], bbox_ur[1], bbox_ur[0]]

    def render_map_image(
        self,
        geo: Geolocation,
        zoom: int = MAP_DEFAULT_ZOOM,
        sizex: int = MAP_DEFAULT_SIZE_X,
        sizey: int = MAP_DEFAULT_SIZE_Y,
    ) -> Image:
        # map = geotiler.Map(
        #     center=(geo.lon, geo.lat), zoom=zoom, size=(sizex, sizey), provider="osm"
        # )
        lat_deg, lon_deg, delta_lat, delta_long, zoom = (
            45.720 - 0.04 / 2,
            4.210 - 0.08 / 2,
            0.04,
            0.08,
            14,
        )
        a, bbox = self.getImageCluster(lat_deg, lon_deg, delta_lat, delta_long, zoom)
        return a
