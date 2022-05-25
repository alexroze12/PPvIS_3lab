import sys
import time
import pygame



class HelpMenu:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1020, 750))
        pygame.display.set_caption('Help menu')
        self.background = self.create_background()

    def create_background(self):
        background_original = pygame.image.load('../images/background/background.jpg').convert()
        return background_original

    def display_score(self, score):
        extra_life_image = pygame.image.load('../images/upgrades/extra_heart.png')
        extra_life_image.set_colorkey((255, 255, 255))
        size_big_image = pygame.image.load('../images/upgrades/size_big.png')
        size_big_image.set_colorkey((255, 255, 255))
        size_small_image = pygame.image.load('../images/upgrades/size_small.png')
        size_small_image.set_colorkey((255, 255, 255))
        speed_fast_image = pygame.image.load('../images/upgrades/speed_fast.png')
        speed_fast_image.set_colorkey((255, 255, 255))
        speed_slow_image = pygame.image.load('../images/upgrades/speed_slow.png')
        speed_slow_image.set_colorkey((255, 255, 255))
        font_help = pygame.font.SysFont("arial", 35)
        explanation_help = pygame.font.SysFont("arial", 15)
        explanation_extra_life = explanation_help.render(
            "  Extra life - a game item that increases the number of player's lives.", True, (255, 255, 0))
        explanation_size_big = explanation_help.render(
            "  Increasing the length of the platform.", True, (255, 255, 0))
        explanation_size_small = explanation_help.render(
            "  Platform length reduction.", True, (255, 255, 0))
        explanation_speed_fast = explanation_help.render(
            "  Ball speed increase.", True, (255, 255, 0))
        explanation_speed_slow = explanation_help.render(
            "  Decrease in ball speed.", True, (255, 255, 0))
        self.display_surface.blit(explanation_extra_life, (30, 54))
        self.display_surface.blit(explanation_size_big, (30, 104))
        self.display_surface.blit(explanation_size_small, (30, 154))
        self.display_surface.blit(explanation_speed_fast, (30, 204))
        self.display_surface.blit(explanation_speed_slow, (30, 254))
        text_score = font_help.render("Help", True, (255, 0, 0))
        self.display_surface.blit(extra_life_image, (0, 50))
        self.display_surface.blit(size_big_image, (0, 100))
        self.display_surface.blit(size_small_image, (0, 150))
        self.display_surface.blit(speed_fast_image, (0, 200))
        self.display_surface.blit(speed_slow_image, (-5, 250))
        self.display_surface.blit(text_score, (450, 0))

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
                # update the game
            self.display_surface.blit(self.background, (0, 0))
            self.display_score(score=0)
            pygame.display.update()


if __name__ == '__main__':
    help_menu = HelpMenu()
    help_menu.run()
