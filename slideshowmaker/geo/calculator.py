# from https://www.geeksforgeeks.org/program-distance-two-points-earth/

from math import radians, cos, sin, asin, sqrt
from ..models.geolocation import Geolocation
from ..models.geobox import GeoBox


class GeoCalculator:
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

    def get_bounding_box(positions: list[Geolocation]) -> GeoBox:
        gmin = Geolocation(
            min(map(lambda x: x["lat"], positions)),
            min(map(lambda x: x["lon"], positions)),
        )
        gmax = Geolocation(
            max(map(lambda x: x["lat"], positions)),
            max(map(lambda x: x["lon"], positions)),
        )
        return GeoBox(gmin, gmax)

    def get_bounding_size(boundig_box: GeoBox):
        size = GeoCalculator.distance_km(
            boundig_box.min.lat,
            boundig_box.max.lat,
            boundig_box.min.lon,
            boundig_box.max.lon,
        )
        return size

    def get_center(boundig_box: GeoBox):
        center = Geolocation(
            (boundig_box.max.lat + boundig_box.min.lat) / 2.0,
            (boundig_box.max.lon + boundig_box.min.lon) / 2.0,
        )
        return center
