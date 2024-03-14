from exif import Image
import dateutil


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


def get_gps_coordinates(image: Image) -> tuple:
    if not image.has_exif:
        return (None, None)

    return convert_exif_gps_location(
        image["gps_latitude"],
        image["gps_latitude_ref"],
        image["gps_longitude"],
        image["gps_longitude_ref"],
    )


def get_timestamp(image: Image) -> tuple:
    DT = dateutil.parser.parse(image["datetime"]).isoformat()
    return (DT,)


def get_image_metadata(filename: str) -> tuple:
    with open(filename, "rb") as image_file:
        try:
            image = Image(image_file)
            gps_data = get_gps_coordinates(image)
            timestamp = get_timestamp(image)
            return timestamp + gps_data
        except Exception:
            return (None, None, None)
