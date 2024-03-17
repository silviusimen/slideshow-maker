import json
import glob
import os

from slideshowmaker.models.base_object import SerializableObject
from slideshowmaker.metadata.tools import MetadataTools
from slideshowmaker.clustering.clusterer import Clusterer
from slideshowmaker.file_cache import FileCache
from slideshowmaker.util.serializer import Serializer

cache = FileCache("cache/cache.json")
cache.load()




def jprint(data):
    print(json.dumps(Serializer.serialize(data), indent=4))


files = glob.glob(os.path.join("", "data/", "*.*"))

metadata_list = MetadataTools.get_metadata_for_files(files, cache)
# jprint(metadata_list)
clusters = Clusterer.cluster_media(metadata_list)
jprint(clusters)

cache.save()
