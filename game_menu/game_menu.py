import pygame
import sys
from pygame import *
from main import *
from help_menu import HelpMenu
from score_menu import ScoreMenu

init()
size = (1020, 750)
screen = display.set_mode(size)
ARIAL = font.SysFont('arial', 80)
background_image = pygame.image.load("../images/background/background.jpg")


class Menu:
    def __init__(self):
        self._options_surface = []
        self._call_backs = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._options_surface.append(ARIAL.render(option, True, (255, 255, 255)))
        self._call_backs.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options_surface) - 1))

    def select(self):
        self._call_backs[self._current_option_index]()

    def draw(self, surface, x, y, option_y_padding):
        for i, option in enumerate(self._options_surface):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surface, (0, 100, 0), option_rect)
            surface.blit(option, option_rect)

running = True


def quit_game():
    global running
    running = False
    pygame.quit()
    sys.exit()
menu = Menu()
menu.append_option('Start', lambda: Game().run())
menu.append_option('Score', lambda: ScoreMenu().run())
menu.append_option('Help', lambda: HelpMenu().run())
menu.append_option('Quit', quit_game)

while running:
    pygame.init()
    screen.blit(background_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                menu.switch(-1)
            elif event.key == K_DOWN:
                menu.switch(1)
            elif event.key == K_RETURN:
                menu.select()

    screen.fill((0, 0, 0))
    menu.draw(screen, 400, 100, 100)
    display.flip()




