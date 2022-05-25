import sys
import time
import pygame
from settings import *


class Loss:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Arkanoid')
        self.background = self.create_background()

    def create_background(self):
        background_original = pygame.image.load('../images/background/background.jpg').convert()
        return background_original

    def run(self):
        last_time = time.time()
        while True:
            delta_time = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # update the game
            self.display_surface.blit(self.background, (0, 0))
            font_loss = pygame.font.SysFont("arial", 100)
            text_loss = font_loss.render("Game over!", True, (255, 230, 0))
            self.display_surface.blit(text_loss, (430, 310))
            pygame.display.update()


if __name__ == '__main__':
    loss = Loss()
    loss.run()
