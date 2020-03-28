import requests


def get_organization(pos):
    geosearch_api_server = 'https://search-maps.yandex.ru/v1/'
    params = {
        'apikey': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
        'll': ','.join(pos),
        'text': 'а',
        'lang': 'ru_RU',
        'type': 'biz'
    }
    response = requests.get(geosearch_api_server, params=params)
    if not response:
        raise RuntimeError
    return response.json()['features'][0]


def get_org_pos(org):
    return org['geometry']['coordinates']


def get_toponym(search):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": search,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # raise RuntimeError('Error on sending Geocode Request')
        return None

    try:
        json_response = response.json()
        return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except Exception:
        return None


def get_coordinates(toponym):
    return toponym["Point"]["pos"].split()
