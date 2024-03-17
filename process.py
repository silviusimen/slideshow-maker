from slideshowmaker.metadata.tools import MetadataTools
from slideshowmaker.clustering.clusterer import Clusterer
from slideshowmaker.file_cache import FileCache
from slideshowmaker.util.serializer import jprint
from slideshowmaker.util.files import FileUtil

cache = FileCache("cache/cache.json")
cache.load()


files = FileUtil.get_input_files()

metadata_list = MetadataTools.get_metadata_for_files(files, cache)
# jprint(metadata_list)
clusters = Clusterer.cluster_media(metadata_list)
jprint(clusters)

cache.save()
