import os
from settings import resource_path, TILESIZE
import spritesheets
import pygame as pg

resource_dir = resource_path('pics')
player_sheet_location = os.path.join(resource_dir, 'mort_sprite_sheets.png')
player_sheet = spritesheets.spritesheet(player_sheet_location)
PLAYER_RUN = player_sheet.multi_crop(((408, 0, 24, 24),
                                      (408 + 24 * 1, 0, 24, 24),
                                      (408 + 24 * 2, 0, 24, 24),
                                      (408 + 24 * 3, 0, 24, 24),
                                      (408 + 24 * 4, 0, 24, 24),
                                      (408 + 24 * 5, 0, 24, 24),
                                      (408 + 24 * 6, 0, 24, 24)), colorkey=(0, 0, 0))
PLAYER_RUN = [pg.transform.scale(sprite, (TILESIZE, TILESIZE))
              for sprite in PLAYER_RUN]


PLAYER_IDE = player_sheet.multi_crop(((0, 0, 24, 24),
                                      (0 + 24 * 1, 0, 24, 24),
                                      (0 + 24 * 2, 0, 24, 24),
                                      (0 + 24 * 3, 0, 24, 24)), colorkey=(0, 0, 0))

PLAYER_IDE = [pg.transform.scale(sprite, (TILESIZE, TILESIZE))
              for sprite in PLAYER_IDE]

wall_sheet_location = os.path.join(resource_dir, 'walls_sheet.png')
walls_sheet = spritesheets.spritesheet(wall_sheet_location)
WALL_SPRITE = {
    'up-left': walls_sheet.crop((0, 0, 32, 32),),
    'up': walls_sheet.crop((32, 0, 32, 32)),
    'up-right': walls_sheet.crop((64, 32, 32, 32)),
    'solo_up': walls_sheet.crop((96, 0, 32, 32)),
    'left': walls_sheet.crop((0, 32, 32, 32)),
    'mid': walls_sheet.crop((32, 32, 32, 32)),
    'right': walls_sheet.crop((64, 32, 32, 32)),
    'down-right': walls_sheet.crop((64, 64, 32, 32)),
    'down': walls_sheet.crop((32, 64, 32, 32)),
    'down-left': walls_sheet.crop((0, 64, 32, 32)),
    'solo': walls_sheet.crop((96, 96, 32, 32)),
    'solo_down': walls_sheet.crop((96, 64, 32, 32)),
    'solo_mid_ver': walls_sheet.crop((96, 32, 32, 32)),
    'solo_left': walls_sheet.crop((0, 96, 32, 32)),
    'solo_mid_hor': walls_sheet.crop((32, 96, 32, 32)),
    'solo_right': walls_sheet.crop((64, 96, 32, 32)), }
WALL_SPRITE = {sprite: pg.transform.scale(
    WALL_SPRITE[sprite], (TILESIZE, TILESIZE)) for sprite in WALL_SPRITE}

floor_sheet_location = os.path.join(resource_dir, 'background_brick_1.png')
floor_sheet = spritesheets.spritesheet(floor_sheet_location)
FLOOR = pg.transform.scale(floor_sheet.crop(
    (0, 0, 32, 32)), (TILESIZE, TILESIZE))

trapdoor_sheet_location = os.path.join(resource_dir, 'trapdoor_sheet.png')
trapdoor_sheet = spritesheets.spritesheet(trapdoor_sheet_location)
TRAPDOOR_SPRITE = {
    'open': trapdoor_sheet.crop((32, 0, 32, 32)),
    'closed': trapdoor_sheet.crop((0, 0, 32, 32)),
}
TRAPDOOR_SPRITE = {sprite: pg.transform.scale(
    TRAPDOOR_SPRITE[sprite], (TILESIZE, TILESIZE)) for sprite in TRAPDOOR_SPRITE}
