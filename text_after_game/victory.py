from pygame import display
from main import *
import time
import sys
import json
import pygame
from settings import *
from text_after_game.text import enter_name
from read_and_write_files.write_read_files import WriteRead


class Victory:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Arkanoid')
        self.background = self.create_background()

    def create_background(self):
        background_original = pygame.image.load('../images/background/background.jpg').convert()
        return background_original

    def run(self):
        last_time = time.time()
        while True:
            pygame.init()
            delta_time = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        from game_menu import Menu
                        return Menu()

                # update the game
            self.display_surface.blit(self.background, (0, 0))
            font_victory = pygame.font.SysFont("arial", 100)
            text_victory = font_victory.render("You won!", True, (255, 230, 0))
            self.display_surface.blit(text_victory, (430, 340))
            display.update()
            list = []
            score = WriteRead().read2()# score
            for i in score.values():
                a = i
            with open('../config/score.json') as fp:
                data = json.load(fp)
            for i in range(len(data)):
                for m in data[i].values():
                    b = m
                    list.append(b)
            info = large(list)
            if a <= info:
                pass
            elif a > info:
                with open('../config/score.json') as fp:
                    data = json.load(fp)
                entry = enter_name()
                data.append({str(entry): a})
                with open('../config/score.json', 'w') as json_file:
                    json.dump(data, json_file, indent=4, separators=(',', ': '))


def large(arr):
    max = arr[0]
    for i in arr:
        if i > max:
            max = i
    return max
if __name__ == '__main__':
    victory = Victory()
    victory.run()
