import io

import pygame

from __main__ import screen, width
from request_coordinate import get_coordinates, get_toponym
from request_image import load_map


class Map:
    def __init__(self):
        self.scale = 5
        self.postal_code = ''
        self.center = [56.188484, 58.007144]
        self.map_type = 'map'
        self.pt = None
        self.address = None
        self.render()

    def render(self):
        pygame.draw.line(screen, pygame.Color("red"), (0, 45), (width, 45), 5)
        self.image = pygame.image.load(
            io.BytesIO(load_map([str(self.center[0]), str(self.center[1])],
                                self.scale,
                                self.map_type,
                                pt=self.pt if self.pt else None)))

    def search(self, request):
        result = get_toponym(request)
        if result:
            self.show_address(result)
            result = get_coordinates(result)
            self.center = [float(result[0]), float(result[1])]
            self.pt = self.center.copy()

    def show_address(self, result):
        self.address = result['metaDataProperty']['GeocoderMetaData']['text']
        if 'postal_code' in result['metaDataProperty']['GeocoderMetaData']['Address']:
            self.postal_code = result['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        else:
            self.postal_code = ''
