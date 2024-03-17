from slideshowmaker.metadata.common import get_metadata

from slideshowmaker.geotagging import get_open_map_url
from slideshowmaker.geocalculator import get_bounding_size
from datetime import datetime

# "metadata_info_data/PXL_20231203_000521027.jpg": {
#     "ts": "2023-12-03T13:05:21",
#     "lat": -43.691380555555554,
#     "lon": 170.17721388888887
# },


def _get_date_as_str(metadata: dict) -> str:
    return datetime.fromisoformat(metadata["ts"]).date().isoformat()


def _cluster_by_day(metadata_list: list) -> dict:
    dates = dict()
    for md in metadata_list:
        date_str = _get_date_as_str(md)
        if not date_str in dates:
            dates[date_str] = {"items": [md]}
        else:
            dates[date_str]["items"].append(md)
    return dates


def _get_metadata_for_files(files: list) -> dict:
    metadata_list = []
    for filename in files:
        metadata = get_metadata(filename)
        metadata["filename"] = filename
        metadata["map"] = get_open_map_url(metadata["lat"], metadata["lon"], 12)
        metadata_list.append(metadata)
    return metadata_list


def _set_cluster_size(cluster_dict: dict) -> None:
    for key in cluster_dict.keys():
        metadata_list = cluster_dict[key]["items"]
        lats = map(lambda x: x["lat"], metadata_list)
        lons = map(lambda x: x["lon"], metadata_list)
        size = get_bounding_size(lats, lons)
        cluster_dict[key]["size"] = size


def cluster_media(files: list) -> dict:
    metadata_list = _get_metadata_for_files(files)
    cluster_by_day = _cluster_by_day(metadata_list)
    _set_cluster_size(cluster_by_day)

    return cluster_by_day
