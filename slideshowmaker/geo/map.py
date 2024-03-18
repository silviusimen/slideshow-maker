from ..models.geolocation import Geolocation
import geotiler
from PIL import Image


class Map:
    def get_url(geo: Geolocation, zoom: int = 19) -> str:
        return f"https://www.openstreetmap.org/#map={zoom}/{geo.lat}/{geo.lon}"

    def get_image(
        filename: str,
        geo: Geolocation,
        zoom: int = 15,
        sizex: int = 2048,
        sizey: int = 1536,
    ):
        map = geotiler.Map(
            center=(geo.lon, geo.lat), zoom=zoom, size=(sizex, sizey), provider="osm"
        )
        image = geotiler.render_map(map)
        image.save(filename)
