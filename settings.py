import os, sys
def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def vec2int(v):
    return (int(v.x), int(v.y))

def get_gridpos(pos):
	return pos // TILESIZE

def get_screenpos(gridpos):
	return gridpos*TILESIZE

from pygame.math import Vector2
vec = Vector2

vecLEFT = vec(-1, 0)
vecRIGHT = vec(1, 0)
vecUP = vec(0, -1)
vecDOWN = vec(0, 1)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGRAY = (30, 30, 30)
LIGHTGRAY = (100, 100, 100)
YELLOW = (255, 255, 0)


WIDTH = 1024
HEIGHT = 768
FPS = 60
FRAME_CONSTANT = 11
TITLE = "THE GAME"
BGCOLOR = DARKGRAY

TILESIZE = 64
GRIDWIDTH = WIDTH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE

PLAYER_SPEED = 0.5


