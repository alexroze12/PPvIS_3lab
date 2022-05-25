import json
import time
import pygame
import sys


class ScoreMenu:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1020, 750))
        pygame.display.set_caption('Score menu')
        self.background = self.create_background()

    def create_background(self):
        background_original = pygame.image.load('../images/background/background.jpg').convert()
        return background_original

    def display_score(self):
        with open('../config/score.json') as fp:
            data = json.load(fp)
        result = {}
        for d in data:
            result.update(d)
        sorted_values = sorted(result.values())
        sorted_dict = {}
        for i in sorted_values:
            for k in result.keys():
                if result[k] == i:
                    sorted_dict[k] = result[k]
                    break
        sorted_reverse_dict = dict(sorted(sorted_dict.items(), reverse=True, key=lambda x: x[1]))
        counter = 0
        for i, j in sorted_reverse_dict.items():
            person = i
            score = j
            font_score = pygame.font.SysFont("arial", 35)
            text_people = font_score.render(str(person), True, (255, 230, 0))
            explanation_score = pygame.font.SysFont("arial", 35)
            text_score = explanation_score.render(str(score), True, (255, 230, 0))
            self.display_surface.blit(text_people, (200, counter*54))
            self.display_surface.blit(text_score, (800, counter*54))
            counter += 1

    def run(self):
        last_time = time.time()
        while True:
            delta_time = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        from game_menu import Menu
                        Menu()
                        return
            self.display_surface.blit(self.background, (0, 0))
            self.display_score()
            pygame.display.update()


if __name__ == '__main__':
    score_menu = ScoreMenu()
    score_menu.run()
