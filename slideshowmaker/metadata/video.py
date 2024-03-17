import dateutil

import xml.etree.ElementTree as ET
import re

import slideshowmaker.melt as melt
from ..models.metadata import Metadata
from ..models.geolocation import Geolocation


def get_gps_location_info_from_melt_xml_output(root: ET) -> tuple:
    try:
        gps_info = root.find(
            "./producer/property/[@name='meta.attr.location.markup']"
        ).text
        gps_info = gps_info.strip("/")
        regex = r"([\+\-]*\d+[.]\d+)([\+\-]*\d+[.]\d+)"
        matches = re.match(regex, gps_info)
        lat = float(matches.group(1))
        lon = float(matches.group(2))
        return Geolocation(lat, lon)
    except Exception:
        return None


def get_timestamp_info_from_melt_xml_output(root: ET) -> tuple:
    try:
        timestamp = root.find(
            "./producer/property/[@name='meta.attr.creation_time.markup']"
        ).text
        timestamp = dateutil.parser.parse(timestamp).isoformat()
        return timestamp
    except Exception:
        return None


def get_video_metadata(filename: str) -> tuple:
    try:
        xml_file_info = melt.melt_get_xml_info_for_video_file(filename)
        root = ET.fromstring(xml_file_info)
        geo = get_gps_location_info_from_melt_xml_output(root)
        timestamp = get_timestamp_info_from_melt_xml_output(root)
        return Metadata(filename, timestamp, geo)

    except Exception:
        return None
