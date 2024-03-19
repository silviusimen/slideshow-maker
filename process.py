from slideshowmaker.metadata.metadata import MetadataTools
from slideshowmaker.clustering.clusterer import Clusterer
from slideshowmaker.util.file_cache import FileCache
from slideshowmaker.util.serializer import jprint
from slideshowmaker.util.files import FileUtil
from slideshowmaker.map.map_osm import Map_OSM as Map
from slideshowmaker.map.tile_manager import TileManager

import os

cache = FileCache("cache/cache.json")
cache.load()

os.makedirs("tmp", exist_ok=True)

files = FileUtil.get_input_files()

metadata_list = MetadataTools.get_metadata_for_files(files, cache)
# jprint(metadata_list)
clusters = Clusterer.cluster_media(metadata_list)
# jprint(clusters)

http_cache = FileCache("cache/http_cache.json")
http_cache.load()

tileManager = TileManager(http_cache)
map = Map(tileManager)

for key, value in clusters.items():
    size = value["size"]
    center = value["center"]
    print(f"{key} size={size} center={center}")
    filename = f"tmp/map_{key}.png"
    image = map.render_map_image(center, 12)
    image.save(filename)

# cluster_dict[key]["bounding_box"] = boundig_box

cache.save()
http_cache.save()
