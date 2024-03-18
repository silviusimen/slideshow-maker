from ..metadata.metadata import MetadataTools

from ..geo.calculator import GeoCalculator
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
            positions = [x["geo"] for x in cluster_dict[key]["items"]]
            boundig_box = GeoCalculator.get_bounding_box(positions)
            size = GeoCalculator.get_bounding_size(boundig_box)
            cluster_dict[key]["size"] = size
            cluster_dict[key]["bounding_box"] = boundig_box
            cluster_dict[key]["center"] = GeoCalculator.get_center(boundig_box)

    def cluster_media(metadata_list: list) -> dict:
        cluster_by_day = Clusterer._cluster_by_day(metadata_list)
        Clusterer._set_cluster_size(cluster_by_day)

        return cluster_by_day
