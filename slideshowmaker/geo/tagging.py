from ..models.geolocation import Geolocation
from geopy.geocoders import Nominatim
import json

import overpy

from ..models.geolocation import Geolocation
from ..models.geobox import GeoBox


class GeoTag:

    pass


# def _lookup_location_metadata(lat: float, lon: float) -> dict:
#     cache_key = f"gps_location_info_lat_{round(lat, 5)}_lon_{round(lon, 5)}"
#     # data = get_cache(cache_key)
#     # if data != None:
#     #     return data

#     geolocator = Nominatim(user_agent="slideshow_maker/0.1")
#     location_gps_location = f"{lat}, {lon}"
#     location = geolocator.reverse(location_gps_location)
#     location_data = location.raw
#     # set_cache(cache_key, location_data)
#     return location_data

# def _lookup_location_arround(tag: str, value: str, lat: float, lon: float) -> dict:
#     cache_key = (
#         f"location_attractions_{tag}_{value}_lat_{round(lat, 5)}_lon_{round(lon, 5)}"
#     )
#     # data = get_cache(cache_key)
#     # if data != None:
#     #     return data

#     api = overpy.Overpass()
#     location_gps_location = f"{lat}, {lon}"
#     tag_api_string = f"{tag}={value}" if value != None else f"{tag}"
#     api_query = f"[out:json];node[{tag_api_string}](around: 20000, {location_gps_location});out;"
#     result = api.query(api_query)
#     local_data = []
#     for node in result.nodes:
#         info = {"tags": node.tags, "lat": float(node.lat), "lon": float(node.lon)}
#         local_data.append(info)
#     # set_cache(cache_key, local_data)
#     return local_data


# def _lookup_location_poi(lat: float, lon: float) -> dict:
#     attractions = _lookup_location_arround("tourism", "attraction", lat, lon)
#     viewpoints = _lookup_location_arround("tourism", "viewpoint", lat, lon)
#     all_tourism = _lookup_location_arround("tourism", None, lat, lon)
#     return attractions + viewpoints + all_tourism


# def _list_local_poi(location_poi: list, lat: float, lon: float):
#     for poi in location_poi:
#         print(poi)


# def get_location_info(file: str, gps_location: tuple) -> dict:
#     lat = gps_location[0]
#     lon = gps_location[1]
#     location_data = _lookup_location_metadata(lat, lon)
#     url = get_open_map_url(lat, lon)
#     location_poi = _lookup_location_poi(lat, lon)
#     print(f"{file} - {location_data['display_name']} {url}")
#     _list_local_poi(location_poi, lat, lon)
