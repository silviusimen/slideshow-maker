from slideshowmaker.image_metadata import get_image_metadata
from slideshowmaker.video_metadata import get_video_metadata

from slideshowmaker.cache import get_cache, set_cache


def get_metadata(filename: str) -> tuple:
    metadata = get_cache(filename)
    if metadata != None:
        return metadata

    if filename.lower().endswith("mp4"):
        metadata = get_video_metadata(filename)
        set_cache(filename, metadata)
        return metadata

    if filename.lower().endswith("jpg"):
        metadata = get_image_metadata(filename)
        set_cache(filename, metadata)
        return metadata

    if filename.lower().endswith("jpeg"):
        metadata = get_image_metadata(filename)
        set_cache(filename, metadata)
        return metadata
