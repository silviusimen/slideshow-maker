import json
import glob
import os

from slideshowmaker.metadata import get_metadata
from slideshowmaker.cache import read_cache, write_cache
from slideshowmaker.geotagging import get_location_info
from slideshowmaker.clustering import cluster_media

CACHE_FILE = "cache/cache.json"


def jprint(data):
    print(json.dumps(data, indent=4))


read_cache(CACHE_FILE)

files = glob.glob(os.path.join("", "data/", "*.*"))

clusters = cluster_media(files)
jprint(clusters)

# for filename in files:
#     metadata = get_metadata(filename)
#     # location_info = get_location_info(filename, (metadata[1], metadata[2]))
#     # print(metadata)

write_cache(CACHE_FILE)
