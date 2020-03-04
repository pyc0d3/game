import pygame as pg
from settings import *
from image_processing import *
from collections import deque


class Player(pg.sprite.Sprite):
    def __init__(self, game, gridpos):
        self.groups = game.all_sprites
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)

        self.RUN_L = [pg.transform.flip(sprite, True, False)
                      for sprite in PLAYER_RUN]
        self.RUN_R = PLAYER_RUN
        self.IDE = PLAYER_IDE
        self.image = self.IDE[0]
        self.rect = self.image.get_rect()
        self.gridpos = vec(gridpos)
        self.pos = self.gridpos * TILESIZE
        self.rect.topleft = self.pos
        self.vel = vec(0, 0)
        self.last_update = 0
        self.current_frame = 0
        self.path = deque()
        self.moving_directions = deque()
        self.is_moving = False
        self.step_count = 0
        self.coords_to_move = self.pos

    def get_keys(self):
        start = self.gridpos
        end = start

        buttons = pg.mouse.get_pressed()
        keys = pg.key.get_pressed()
        if buttons[0]:
            click_pos = vec(pg.mouse.get_pos())
            end = get_gridpos(click_pos) - self.game.camera.gridoffset
            start = self.gridpos
        if not self.is_moving:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                start = self.gridpos
                end = self.gridpos + vecLEFT
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                start = self.gridpos
                end = self.gridpos + vecRIGHT
            if keys[pg.K_UP] or keys[pg.K_w]:
                start = self.gridpos
                end = self.gridpos + vecUP
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                start = self.gridpos
                end = self.gridpos + vecDOWN

        if not self.is_moving and end != start:
            self.path = self.game.grid.find_shortest_path(end, start)

    def move(self):
        if self.is_moving:
            self.pos = self.pos.lerp(self.coords_to_move, PLAYER_SPEED)
            if self.pos.distance_to(self.coords_to_move) < 5:
                self.pos = self.coords_to_move
                self.gridpos = get_gridpos(self.pos)
                self.is_moving = False

        if self.path and not self.is_moving:
            self.coords_to_move = get_screenpos(self.path.popleft())
            self.is_moving = True

    def update(self):
        self.get_keys()
        self.move()
        self.rect.topleft = self.pos
        if not self.is_moving and not self.path:
            self.pos = self.coords_to_move


"""
    def draw(self):
        self.game.screen.blit(self.image, self.rect.topleft)
"""


class Wall(pg.sprite.Sprite):
    def __init__(self, game, gridpos, sprite):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = WALL_SPRITE[sprite].convert_alpha()
        self.rect = self.image.get_rect()
        self.gridpos = vec(gridpos)
        self.pos = get_screenpos(self.gridpos)
        self.rect.topleft = self.pos


class Floor(pg.sprite.Sprite):
    def __init__(self, game, gridpos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = FLOOR.convert_alpha()
        self.rect = self.image.get_rect()
        self.gridpos = vec(gridpos)
        self.pos = get_screenpos(self.gridpos)
        self.rect.topleft = self.pos


class Trapdoor(pg.sprite.Sprite):
    def __init__(self, game, gridpos, is_open=True):
        self.groups = game.all_sprites, game.trapdoors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.is_open = is_open

        if self.is_open:
            self.image = TRAPDOOR_SPRITE['open']
        else:
            self.image = TRAPDOOR_SPRITE['closed']

        self.rect = self.image.get_rect()
        self.gridpos = vec(gridpos)
        self.pos = get_screenpos(self.gridpos)
        self.rect.topleft = self.pos

    def go_deeper(self):
        if self.is_open and (self.gridpos == self.game.player.gridpos):
            self.game.start_new()

    def update(self):
        self.go_deeper()
