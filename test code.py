import pygame
import time
from player import *
from constant import *
from spritesheet_functions import SpriteSheet
import sys
import math

pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Enemy(pygame.sprite.Sprite):
    # Sprite for the Player

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.walking_frames_d = [] # Images for animated walking.
        self.walking_frames_u = []
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.direction= ""

        sprite_sheet = SpriteSheet("enemy_spritesheet.png")

        for i in range(7):
            image = sprite_sheet.get_image((150 * i) + 40, 0, 54, 96)
            image.set_colorkey(DARK_GREEN)
            self.walking_frames_d.append(image)

        for i in range(7):
            image = sprite_sheet.get_image((150 * i) + 40, 120, 54, 82)
            image.set_colorkey(DARK_GREEN)
            self.walking_frames_u.append(image)

        for i in range(7):
            image = sprite_sheet.get_image((150 * i) + 40, 235, 61, 82)
            image.set_colorkey(DARK_GREEN)
            self.walking_frames_l.append(image)

        for i in range(7):
            image = sprite_sheet.get_image((150 * i) + 40, 352, 60, 80)
            image.set_colorkey(DARK_GREEN)
            self.walking_frames_r.append(image)


        self.frame = 0
        self.frames = self.walking_frames_d
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (120, 100)
        self.speedx = -2
        self.speedy = -2

        self.last_update = pygame.time.get_ticks()

        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.animate_sprite()
        self.check_bullets()
        self.scrolling()
        self.move_towards_player(player)
        self.check_direction()

    def animate_sprite(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.frame = (self.frame + 1) % 7
            self.image = self.frames[self.frame]

    def check_bullets(self):
        hits = pygame.sprite.groupcollide(enemy_sprites, bullets, True, True)
        for hit in hits:
            self.kill()

    def scrolling(self):
        self.rect.x += -player.speedx
        self.rect.y += -player.speedy

    def move_towards_player(self, player):
        # find normalized direction vector (dx, dy) between enemy and player
        self.dx = self.rect.x - player.rect.x
        self.dy = self.rect.y - player.rect.y
        dist = math.hypot(self.dx, self.dy)

        try:
            self.dx = self.dx /dist
            self.dy = self.dy / dist
        except ZeroDivisionError:
            dist = 1

        # move along this normalized vector towards the player at current speed
        self.rect.x += self.dx * self.speedx
        self.rect.y += self.dy * self.speedy

    def check_direction(self):
        if abs(self.dx) > abs(self.dy):
            if self.dx >= 0:
                self.frames = self.walking_frames_l
                self.direction = "right"
            elif self.dx < 0:
                self.frames = self.walking_frames_r
                self.direction = "left"
        else:
            if self.dy >= 0:
                self.frames = self.walking_frames_u
                self.direction = "down"
            elif self.dy < 0:
                self.frames = self.walking_frames_d
                self.direction = "up"

enemy = Enemy()
all_sprites.add(enemy)
enemy_sprites.add(enemy)