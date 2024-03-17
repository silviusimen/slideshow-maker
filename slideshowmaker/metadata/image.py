from exif import Image
import dateutil
import datetime
from ..models.metadata import Metadata
from ..models.geolocation import Geolocation


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
    return Geolocation(dec_la, dec_lor)


def get_gps_coordinates(image: Image) -> tuple:
    if not image.has_exif:
        return None

    return convert_exif_gps_location(
        image["gps_latitude"],
        image["gps_latitude_ref"],
        image["gps_longitude"],
        image["gps_longitude_ref"],
    )


def get_timestamp(image: Image) -> tuple:
    try:
        datetime_str = image["datetime"]
        # for some reason dateutil.parser.parse() converts '2023:12:03 13:05:21' to '2024-03-15T13:05:21'
        # datetime_parsed = dateutil.parser.parse(datetime_str)
        # timestamp_iso = datetime_parsed.isoformat()
        datetime_parsed2 = datetime.datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
        timestamp_iso2 = datetime_parsed2.isoformat()
    except Exception as e:
        print(e)
        return None
    return timestamp_iso2


def get_image_metadata(filename: str) -> tuple:
    with open(filename, "rb") as image_file:
        try:
            image = Image(image_file)
            geo = get_gps_coordinates(image)
            timestamp = get_timestamp(image)
            return Metadata(filename, timestamp, geo)
        except Exception:
            return None
