import json
import glob
import os

from slideshowmaker.metadata import get_metadata
from slideshowmaker.cache import read_cache, write_cache
from slideshowmaker.geotagging import get_location_info

CACHE_FILE = "cache/cache.json"

read_cache(CACHE_FILE)

files = glob.glob(os.path.join("", "data/", "*.*"))

for filename in files:
    metadata = get_metadata(filename)
    location_info = get_location_info(filename, (metadata[1], metadata[2]))
    # print(metadata)

write_cache(CACHE_FILE)
