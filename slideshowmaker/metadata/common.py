from .image import get_image_metadata
from .video import get_video_metadata

from ..models.metadata import Metadata
from ..models.geolocation import Geolocation
from slideshowmaker.models.cache import Cache


def get_metadata(filename: str, cache: Cache) -> Metadata:

    md = Metadata(filename)
    if md.load_from_cache(cache):
        return md

    if filename.lower().endswith("mp4"):
        metadata = get_video_metadata(filename)

    if filename.lower().endswith("jpg"):
        metadata = get_image_metadata(filename)

    if filename.lower().endswith("jpeg"):
        metadata = get_image_metadata(filename)

    if metadata != None:
        metadata.save_to_cache(cache)

    return metadata
