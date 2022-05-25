from random import randrange as rnd

import pygame


class SurfaceMaker:
    def get_surf(self, size):
        image = pygame.Surface(size)
        image.fill([rnd(30, 256), rnd(30, 256), rnd(30, 256)])
        return image
