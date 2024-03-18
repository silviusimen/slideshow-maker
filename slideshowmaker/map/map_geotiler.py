from ..models.geolocation import Geolocation
import geotiler
from PIL import Image
from .map import Map, MAP_DEFAULT_ZOOM, MAP_DEFAULT_SIZE_X, MAP_DEFAULT_SIZE_Y


class Map_GeoTtiler(Map):
    def get_url(geo: Geolocation, zoom: int = 19) -> str:
        return f"https://www.openstreetmap.org/#map={zoom}/{geo.lat}/{geo.lon}"

    def get_image(
        geo: Geolocation,
        zoom: int = MAP_DEFAULT_ZOOM,
        sizex: int = MAP_DEFAULT_SIZE_X,
        sizey: int = MAP_DEFAULT_SIZE_Y,
    ) -> Image:
        map = geotiler.Map(
            center=(geo.lon, geo.lat), zoom=zoom, size=(sizex, sizey), provider="osm"
        )
        image = geotiler.render_map(map)
        return image
