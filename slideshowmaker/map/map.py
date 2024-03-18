from ..models.geolocation import Geolocation
from PIL import Image
from abc import abstractmethod

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
        zoom: int = MAP_DEFAULT_ZOOM,
        sizex: int = MAP_DEFAULT_SIZE_X,
        sizey: int = MAP_DEFAULT_SIZE_Y,
    ) -> Image:
        pass
