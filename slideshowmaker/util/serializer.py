from ..models.base_object import SerializableObject
import json


class Serializer:
    def serialize(data):
        if isinstance(data, SerializableObject):
            return data.serialize()
        if isinstance(data, list):
            return [Serializer.serialize(x) for x in data]
        if isinstance(data, dict):
            d = dict()
            for key, value in data.items():
                d[key] = Serializer.serialize(value)
            return d
        return data


def jprint(data):
    print(json.dumps(Serializer.serialize(data), indent=4))
