from ..models.geolocation import Geolocation
from ..geo.calculator import GeoCalculator
from PIL import Image
from abc import abstractmethod
import math


MAP_DEFAULT_ZOOM = 8
MAP_DEFAULT_SIZE_X = 2048
MAP_DEFAULT_SIZE_Y = 1536


class Map:
    @abstractmethod
    def get_url(geo: Geolocation, zoom: int = 19) -> str:
        pass

    @abstractmethod
    def render_map_image(
        geo: Geolocation,
        size_km: float,
        # zoom: int = MAP_DEFAULT_ZOOM,
        sizex: int = MAP_DEFAULT_SIZE_X,
        sizey: int = MAP_DEFAULT_SIZE_Y,
    ) -> Image:
        pass

    def deg2num(self, lat_deg: float, lon_deg: float, zoom: int):
        lat_rad = math.radians(lat_deg)
        n = 1 << zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return xtile, ytile

    def num2deg(self, xtile: int, ytile: int, zoom: int):
        n = 1 << zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return lat_deg, lon_deg

    def zoom_to_tile_degree(self, zoom: int) -> float:
        n = 1 << zoom
        width_deg = 360.0 / n
        return width_deg
