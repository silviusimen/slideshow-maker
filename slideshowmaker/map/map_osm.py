from ..models.cache import Cache
from ..models.geolocation import Geolocation
from ..geo.calculator import GeoCalculator
from .tile_manager import TileManager

from PIL import Image
from .map import Map, MAP_DEFAULT_ZOOM, MAP_DEFAULT_SIZE_X, MAP_DEFAULT_SIZE_Y

import math

MAP_NUM_TILES_PER_IMAGE = 32
MAP_TILE_NUM_PIXELS = 256

# https://stackoverflow.com/questions/28476117/easy-openstreetmap-tile-displaying-for-python
# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
# https://wiki.openstreetmap.org/wiki/Raster_tile_providers
# https://wiki.openstreetmap.org/wiki/Zoom_levels
# https://{a|b|c}.tile.opentopomap.org/{z}/{x}/{y}.png


class Map_OSM(Map):
    def __init__(self, tile_manager: TileManager):
        self.tile_manager = tile_manager

    def get_url(geo: Geolocation, zoom: int = 19) -> str:
        return f"https://www.openstreetmap.org/#map={zoom}/{geo.lat}/{geo.lon}"

    def _render_tiles(
        self, xmin: int, ymin: int, xmax: int, ymax: int, zoom: int, tile_size: int
    ):
        width = (xmax - xmin + 1) * tile_size - 1
        height = (ymax - ymin + 1) * tile_size - 1
        image = Image.new(
            "RGB",
            (width, height),
        )
        for xtile in range(xmin, xmax + 1):
            for ytile in range(ymin, ymax + 1):
                try:
                    tyle_bytes = self.tile_manager.getTileAsBytes(zoom, xtile, ytile)
                    tile = Image.open(tyle_bytes)
                    if tile != None:
                        image.paste(
                            tile,
                            box=(
                                (xtile - xmin) * (tile_size - 1),
                                (ytile - ymin) * (tile_size - 1),
                            ),
                        )
                except Exception as e:
                    print(e)

        return image

    def _getZoomLevelFromSize(self, size_km: float):
        if size_km < 0.01:
            return 18
        delta = GeoCalculator.distance_km_to_deg(size_km)
        zoom_for_size = math.log2(360.0 / delta)
        zoom = math.ceil(zoom_for_size)

        if zoom < 0:
            zoom = 0
        if zoom > 18:
            zoom = 18
        return zoom

    def _getTileRangesFromSize(self, geo: Geolocation, zoom: int, delta: float):
        x1, y1 = self.deg2num(geo.lat - delta / 2, geo.lon - delta / 2, zoom)
        x2, y2 = self.deg2num(geo.lat + delta / 2, geo.lon + delta / 2, zoom)
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    def render_map_image(
        self,
        geo: Geolocation,
        size_km: float,
    ) -> Image:
        # if size_km < 1.0:
        #     size_km = 1.0
        size_km = 10
        zoom = self._getZoomLevelFromSize(size_km)
        delta = GeoCalculator.distance_km_to_deg(size_km)
        delta = delta * 4  # make the map larger
        xmin, ymin, xmax, ymax = self._getTileRangesFromSize(geo, zoom, delta)
        image = self._render_tiles(xmin, ymin, xmax, ymax, zoom, MAP_TILE_NUM_PIXELS)
        return image
