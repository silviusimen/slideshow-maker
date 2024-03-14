from slideshowmaker.image_metadata import get_image_metadata
from slideshowmaker.video_metadata import get_video_metadata

from slideshowmaker.cache import get_cache, set_cache


def get_metadata(filename: str) -> tuple:
    cache_key = "metadata_info_" + filename
    metadata = get_cache(cache_key)
    if metadata != None:
        return metadata

    if filename.lower().endswith("mp4"):
        metadata = get_video_metadata(filename)
        set_cache(cache_key, metadata)
        return metadata

    if filename.lower().endswith("jpg"):
        metadata = get_image_metadata(filename)
        set_cache(cache_key, metadata)
        return metadata

    if filename.lower().endswith("jpeg"):
        metadata = get_image_metadata(filename)
        set_cache(cache_key, metadata)
        return metadata