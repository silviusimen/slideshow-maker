import dateutil

import xml.etree.ElementTree as ET
import re

import slideshowmaker.melt as melt


def get_gps_location_info_from_melt_xml_output(root: ET) -> tuple:
    try:
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


def get_timestamp_info_from_melt_xml_output(root: ET) -> tuple:
    try:
        timestamp = root.find(
            "./producer/property/[@name='meta.attr.creation_time.markup']"
        ).text
        DT = dateutil.parser.parse(timestamp).isoformat()
        return (DT,)
    except Exception:
        return None


def get_video_metadata(filename: str) -> tuple:
    try:
        xml_file_info = melt.melt_get_xml_info_for_video_file(filename)
        root = ET.fromstring(xml_file_info)
        gps_data = get_gps_location_info_from_melt_xml_output(root)
        timestamp = get_timestamp_info_from_melt_xml_output(root)
        return timestamp + gps_data
    except Exception:
        return (None, None, None)
