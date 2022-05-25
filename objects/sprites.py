from random import randint, choice
import pygame
from text_after_game.victory import *


class Upgrade(pygame.sprite.Sprite):
    def __init__(self, pos, upgrade_type, groups):
        super().__init__(groups)
        self.upgrade_type = upgrade_type
        self.image = pygame.image.load(f'../images/upgrades/{upgrade_type}.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(midtop=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def update(self, delta_time):
        self.pos.y += self.speed * delta_time
        self.rect.y = round(self.pos.y)
        if self.rect.top > WINDOW_HEIGHT + 100:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # setup %platform
        self.image = pygame.Surface((WINDOW_WIDTH // 10, WINDOW_HEIGHT // 20))
        self.image.fill('red')

        # position
        self.rect = self.image.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.hearts = 3
        self.score_delta_upgrades = 0

    def input(self):
        pygame.init()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def screen_collision(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.left

    def upgrade(self, upgrade_type):
        if upgrade_type == 'speed_fast':
            self.speed += 50
            self.score_delta_upgrades += 2
        if upgrade_type == 'speed_slow':
            self.speed -= 50
            self.score_delta_upgrades += 0
        if upgrade_type == 'extra_heart':
            self.hearts += 1
            self.score_delta_upgrades += 2
        if upgrade_type == 'size_big':
            new_width = self.rect.width * 1.1
            self.image = pygame.Surface((new_width, self.rect.height))
            self.image.fill('red')
            self.rect = self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x
            self.score_delta_upgrades += 2
        if upgrade_type == 'size_small':
            new_width = self.rect.width // 1.1
            self.image = pygame.Surface((new_width, self.rect.height))
            self.image.fill('red')
            self.rect = self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x
            self.score_delta_upgrades += 0

    def update(self, delta_time):
        self.previous_rect = self.rect.copy()
        self.input()
        self.pos.x += self.direction.x * self.speed * delta_time
        self.rect.x = round(self.pos.x)
        self.screen_collision()


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, player, blocks):
        super().__init__(groups)
        # collision object
        self.player = player
        self.blocks = blocks
        self.image = pygame.image.load('../images/ball/ball.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (400, 400))
        self.image.set_colorkey((255, 255, 255))
        # position
        self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        # previous rectangle
        self.previous_rect = self.rect.copy()
        self.direction = pygame.math.Vector2((choice((1, -1)), -1))
        self.speed = 400
        self.pos = pygame.math.Vector2(self.rect.topleft)
        # sounds
        self.fail_sound = pygame.mixer.Sound('../sounds/collision_sounds/fail.wav')
        self.collision_sound = pygame.mixer.Sound('../sounds/collision_sounds/collision.wav')
        self.fail_sound.set_volume(0.1)
        self.score_delta = 0

        # active
        self.active = False

    def window_collision(self, direction):
        if direction == 'horizontal':
            if self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1
            if self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x *= -1
        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1
            if self.rect.bottom > WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1
                self.player.hearts -= 1
                self.fail_sound.play()

    def horizontal_collision(self, direction):

        # find overlaping objects
        number = 0
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)

        if overlap_sprites:
            if direction == 'horizontal':
                for sprite in overlap_sprites:
                    if self.rect.right >= sprite.rect.left and self.previous_rect.right <= sprite.previous_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.collision_sound.play()
                        self.score_delta += 1

                    if self.rect.left <= sprite.rect.right and self.previous_rect.left >= sprite.previous_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.collision_sound.play()
                        self.score_delta += 1

                    if getattr(sprite, 'remaining_blocks', None):
                        sprite.get_damage(1)
                        number += 1
        if len(self.blocks) == 0:
            self.score_delta += 1
            #from main import Game
            #Game().stage_setup("../levels/level_0.json")
            Victory().run()

    def vertical_collision(self, direction):
        number = 0
        overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)
        if overlap_sprites:
            if direction == 'vertical':
                for sprite in overlap_sprites:
                    if self.rect.bottom >= sprite.rect.top and self.previous_rect.bottom <= sprite.previous_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.collision_sound.play()
                        self.score_delta += 1

                    if self.rect.top <= sprite.rect.bottom and self.previous_rect.top >= sprite.previous_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.collision_sound.play()
                        self.score_delta += 1
                    if getattr(sprite, 'remaining_blocks', None):
                        sprite.get_damage(1)
                        number += 1

        if len(self.blocks) == 0:
            self.score_delta += 1
            #from main import Game
            #Game().stage_setup('../levels/level_0.json')
            Victory().run()

    def update(self, delta_time):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # create previous rectangle
        self.previous_rect = self.rect.copy()
        if self.active:
            # horizontal movement + collision
            self.pos.x += self.direction.x * self.speed * delta_time
            self.rect.x = round(self.pos.x)
            self.window_collision('horizontal')
            self.horizontal_collision('horizontal')
            # vertical movement + collision
            self.pos.y += self.direction.y * self.speed * delta_time
            self.rect.y = round(self.pos.y)
            self.window_collision('vertical')
            self.vertical_collision('vertical')
        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)


class Block(pygame.sprite.Sprite):
    def __init__(self, type_of_block, pos, groups, surfacemaker, create_upgrade):
        super().__init__(groups)
        self.surfacemaker = surfacemaker
        self.image = self.surfacemaker.get_surf((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect(topleft=pos)
        self.previous_rect = self.rect.copy()
        self.remaining_blocks = int(type_of_block)
        # upgrade
        self.create_upgrade = create_upgrade

    def get_damage(self, amount):
        self.remaining_blocks -= amount

        if self.remaining_blocks > 0:
            pass
        else:
            if randint(0, 10) < 9:
                self.create_upgrade(self.rect.center)
                # print(Game().number)
        self.kill()
