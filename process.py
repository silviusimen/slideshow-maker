import json
import glob
import os

from slideshowmaker.models.base_object import SerializableObject
from slideshowmaker.metadata.tools import MetadataTools
from slideshowmaker.clustering.clusterer import Clusterer
from slideshowmaker.file_cache import FileCache

cache = FileCache("cache/cache.json")
cache.load()


def serialize(data):
    if isinstance(data, SerializableObject):
        return data.serialize()
    if isinstance(data, list):
        return [serialize(x) for x in data]
    if isinstance(data, dict):
        d = dict()
        for key, value in data.items():
            d[key] = serialize(value)
        return d
    return data


def jprint(data):
    print(json.dumps(serialize(data), indent=4))


files = glob.glob(os.path.join("", "data/", "*.*"))

metadata_list = MetadataTools.get_metadata_for_files(files, cache)
# jprint(metadata_list)
clusters = Clusterer.cluster_media(metadata_list)
jprint(clusters)

cache.save()
