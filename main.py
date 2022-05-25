from objects.sprites import *
import json

from text_after_game.loss import Loss


class Game:
    def __init__(self):
        file = input('Enter file:')
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.scroll(10,10)
        pygame.display.set_caption('Arkanoid')
        self.background = self.create_background()
        # sprite group setup
        self.all_sprites = pygame.sprite.Group()
        self.blocks_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        # setup
        self.number = 0
        from objects.blocks_graphics import SurfaceMaker
        self.surfacemaker = SurfaceMaker()
        self.stage_setup(file)
        self.player = Player(self.all_sprites)
        self.ball = Ball(self.all_sprites, self.player, self.blocks_sprites)
        # hearts
        self.heart_surf = pygame.image.load('../images/hearts/heart.png').convert_alpha()
        self.heart_surf.set_colorkey((255, 255, 255))
        self.upgrade_sound = pygame.mixer.Sound('../sounds/upgrades_sound/upgrades.wav')
        self.score = 0
        self.music = pygame.mixer.Sound('../sounds/background_sound/background.wav')
        self.music.set_volume(0.1)
        self.music.play(loops=-1)

    def create_upgrade(self, pos):
        upgrade_type = choice(UPGRADES)
        Upgrade(pos, upgrade_type, [self.all_sprites, self.upgrade_sprites])

    def display_score(self, score):
        font_score = pygame.font.SysFont("arial", 30)
        text_score = font_score.render("Score: ", True, COLOR_TEXT)
        text_score_val = font_score.render(f"{score}", True, COLOR_TEXT)
        self.display_surface.blit(text_score, (900, 0))
        self.display_surface.blit(text_score_val, (1090, 0))

    def display_hearts(self):
        for i in range(self.player.hearts):
            x = i * self.heart_surf.get_width()
            self.display_surface.blit(self.heart_surf, (x, 4))

    def create_background(self):
        background_original = pygame.image.load('../images/background/background.jpg').convert()
        return background_original

    def collision_with_upgrades(self):
        overlap_sprites = pygame.sprite.spritecollide(self.player, self.upgrade_sprites, True)
        for sprite in overlap_sprites:
            self.player.upgrade(sprite.upgrade_type)
            self.upgrade_sound.play()

    def stage_setup(self, file):
        # cycle through all rows and all columns of BLOCK_MAP
        # find x and y position for each individual block
        my_file = open("../levels/"+ file)
        data = json.load(my_file)
        my_file.close()
        for row_index, row in enumerate(data["BLOCK_MAP"]):
            for column_index, column in enumerate(row):
                if column != ' ':
                    x = column_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE // 2
                    y = TOP_OFFSET + row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE // 2
                    Block(column, (x, y), [self.all_sprites, self.blocks_sprites], self.surfacemaker,
                          self.create_upgrade)

    def run(self):
        value = 0
        pygame.init()
        last_time = time.time()
        while True:
            delta_time = time.time() - last_time
            last_time = time.time()
            for event in pygame.event.get():
                if self.player.hearts <= 0:
                    Loss().run()
                    pygame.quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True
                    if event.key == pygame.K_ESCAPE:
                        from game_menu.game_menu import Menu
                        Menu()
                        return

            # update the game
            self.all_sprites.update(delta_time)
            self.collision_with_upgrades()
            # draw the frame
            self.display_surface.blit(self.background, (0, 0))
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()
            self.display_score((self.ball.score_delta + self.player.score_delta_upgrades))
            value = (self.ball.score_delta + self.player.score_delta_upgrades)
            to_json = {'player': value}
            WriteRead().write2(to_json)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
