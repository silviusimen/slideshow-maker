import json
import glob
import os

from slideshowmaker.metadata.common import get_metadata
from slideshowmaker.file_cache import FileCache

# from slideshowmaker.geotagging import get_location_info
# from slideshowmaker.clustering import cluster_media

cache = FileCache("cache/cache2.json")
cache.load()


# def jprint(data):
#     print(json.dumps(data, indent=4))

get_metadata("data/PXL_20231203_000521027.jpg", cache)
# read_cache(CACHE_FILE)

# md = get_metadata("data/PXL_20231203_000521027.jpg")
# write_cache(CACHE_FILE)
# md = Metadata("test", "2024-01-01")
# md.json_print()


# files = glob.glob(os.path.join("", "data/", "*.*"))

# # clusters = cluster_media(files)
# # jprint(clusters)

# for filename in files:
#     metadata = get_metadata(filename, cache)
#     # location_info = get_location_info(filename, (metadata[1], metadata[2]))
#     # print(metadata)

cache.save()
# write_cache(CACHE_FILE)
