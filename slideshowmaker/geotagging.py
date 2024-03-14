from geopy.geocoders import Nominatim
import xml.etree.ElementTree as ET
import re

from exif import Image
import json

import slideshowmaker.melt as melt
import overpy


def dms2dd(degrees, minutes, seconds, direction: str):
    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction.upper() == "W" or direction.upper() == "S":
        dd *= -1
    return dd


def convert_exif_gps_location(
    gps_latitude: tuple,
    gps_latitude_ref: str,
    gps_longitude: tuple,
    gps_longitude_ref: str,
) -> tuple:
    dec_la = dms2dd(gps_latitude[0], gps_latitude[1], gps_latitude[2], gps_latitude_ref)
    dec_lor = dms2dd(
        gps_longitude[0], gps_longitude[1], gps_longitude[2], gps_longitude_ref
    )
    return (dec_la, dec_lor)


def get_gps_coordinates_image(filename: str) -> tuple:
    with open(filename, "rb") as image_file:
        try:
            my_image = Image(image_file)
            if not my_image.has_exif:
                return (None, None)

            return convert_exif_gps_location(
                my_image["gps_latitude"],
                my_image["gps_latitude_ref"],
                my_image["gps_longitude"],
                my_image["gps_longitude_ref"],
            )
        except Exception:
            return (None, None)


# "meta.attr.creation_time.markup">2023-12-03T23:14:07.000000Z</property>
def melt_get_gps_location_info_from_xml_output(output: str) -> tuple:
    try:
        root = ET.fromstring(output)
        gps_info = root.find(
            "./producer/property/[@name='meta.attr.location.markup']"
        ).text
        gps_info = gps_info.strip("/")
        regex = r"([\+\-]*\d+[.]\d+)([\+\-]*\d+[.]\d+)"
        matches = re.match(regex, gps_info)
        l1 = float(matches.group(1))
        l2 = float(matches.group(2))
        return (l1, l2)
    except Exception:
        return (None, None)


def get_gps_coordinates(filename: str) -> tuple:
    if filename.lower().endswith("mp4"):
        xml_file_info = melt.melt_get_xml_info_for_video_file(filename)
        return melt_get_gps_location_info_from_xml_output(xml_file_info)
    if filename.lower().endswith("jpg"):
        return get_gps_coordinates_image(filename)
    if filename.lower().endswith("jpeg"):
        return get_gps_coordinates_image(filename)


def get_location_info(gps_location: tuple) -> dict:
    print("---------------------------------------------------------")
    print(gps_location)
    geolocator = Nominatim(user_agent="slideshow_maker/0.1")
    location_gps_location = f"{gps_location[0]}, {gps_location[1]}"
    location = geolocator.reverse(location_gps_location)
    # print(json.dumps(location.raw, indent=4))
    print(f"Name = {location.raw['display_name']}")
    api = overpy.Overpass()
    api_query = f"[out:json];node[tourism=attraction](around: 30000, {location_gps_location});out;"
    result = api.query(api_query)
    for node in result.nodes:
        print(node.tags)
    # print(result)
    # print(json.dumps(result, indent=4))
    return {}
