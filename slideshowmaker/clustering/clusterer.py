from ..metadata.tools import MetadataTools

from ..geo.geocalculator import GeoCalculator
from datetime import datetime
from ..models.cache import Cache


class Clusterer:
    def _get_date_as_str(metadata: dict) -> str:
        return datetime.fromisoformat(metadata["ts"]).date().isoformat()

    def _cluster_by_day(metadata_list: list) -> dict:
        dates = dict()
        for md in metadata_list:
            date_str = Clusterer._get_date_as_str(md)
            if not date_str in dates:
                dates[date_str] = {"items": [md]}
            else:
                dates[date_str]["items"].append(md)
        return dates

    def _set_cluster_size(cluster_dict: dict) -> None:
        for key in cluster_dict.keys():
            metadata_list = cluster_dict[key]["items"]
            size = GeoCalculator.get_bounding_size([x["geo"] for x in metadata_list])
            cluster_dict[key]["size"] = size

    def cluster_media(metadata_list: list) -> dict:
        cluster_by_day = Clusterer._cluster_by_day(metadata_list)
        Clusterer._set_cluster_size(cluster_by_day)

        return cluster_by_day
