import json

_CACHE = dict()


def read_cache(filename: str):
    try:
        new_cache = dict()
        with open(filename, mode="r") as file:
            data = file.read()
            new_cache = json.loads(data)
        _CACHE.clear()
        _CACHE.update(new_cache)
    except:
        pass


def write_cache(filename: str):
    str_data = json.dumps(_CACHE, indent=4)
    with open(filename, "w") as outfile:
        print(str_data, file=outfile)


def get_cache(key: str):
    if key in _CACHE:
        return _CACHE[key]
    return None


def set_cache(key: str, value):
    _CACHE[key] = value
