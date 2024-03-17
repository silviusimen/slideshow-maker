class Serializer:
    def serialize(data):
        if isinstance(data, SerializableObject):
            return data.serialize()
        if isinstance(data, list):
            return [serialize(x) for x in data]
        if isinstance(data, dict):
            d = dict()
            for key, value in data.items():
                d[key] = serialize(value)
            return d
        return data
