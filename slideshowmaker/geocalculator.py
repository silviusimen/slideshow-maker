# from https://www.geeksforgeeks.org/program-distance-two-points-earth/

from math import radians, cos, sin, asin, sqrt
from collections.abc import Iterable


def distance_km(lat1, lat2, lon1, lon2):

    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


def get_bounding_box(lats: Iterable[float], lons: Iterable[float]):
    return (min(lats), min(lons), max(lats), max(lons))


def get_bounding_size(lat: Iterable[float], lon: Iterable[float]):
    lats = [l for l in lat]
    lons = [l for l in lon]
    boundig_box = get_bounding_box(lats, lons)
    size = distance_km(boundig_box[0], boundig_box[2], boundig_box[1], boundig_box[3])
    return size
