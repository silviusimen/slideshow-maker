import json

from slideshowmaker.metadata import get_metadata
from slideshowmaker.cache import read_cache, write_cache

CACHE_FILE = "cache/cache.json"

read_cache(CACHE_FILE)

img_metadata = get_metadata("data/PXL_20231203_000521027.jpg")
print(img_metadata)

vid_metadata = get_metadata("data/PXL_20231203_230925244.TS.mp4")
print(vid_metadata)

write_cache(CACHE_FILE)
