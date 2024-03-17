from .image import get_image_metadata
from .video import get_video_metadata

from ..models.metadata import Metadata
from ..models.cache import Cache
from ..geotagging import get_open_map_url


class MetadataTools:
    def get_metadata_for_file(filename: str, cache: Cache) -> Metadata:

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

    def get_metadata_for_files(files: list, cache: Cache) -> dict:
        metadata_list = []
        for filename in files:
            metadata = MetadataTools.get_metadata_for_file(filename, cache)
            metadata.set("map", get_open_map_url(metadata.geo, 12))
            metadata_list.append(metadata)
        return metadata_list
