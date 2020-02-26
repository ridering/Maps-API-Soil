import requests


def get_map(params):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=params)
    if not response:
        print(response.text)
        raise RuntimeError('Error on requesting static map')
    return response.content


def load_map(coordinates, scale):
    map_params = {
        "ll": ",".join(coordinates),
        "size": "450,450",
        "z": str(scale),
        "l": "map"
    }

    return get_map(map_params)