import pygame as pg
from settings import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.debug = False
        self.start_new()

    def start_new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.trapdoors = pg.sprite.Group()

        self.map = Map(self)
        self.map.load()
        self.camera = Camera(self.map.width, self.map.height)
        self.grid = WeightedGrid(
            self, (self.map.gridwidth, self.map.gridheight))

    def draw_grid(self,):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGRAY, (0, y), (WIDTH, y))

    def draw_text(self, text, pos, font_size=30, color=WHITE, centred=False):
        fonts = pg.font.get_fonts()
        font = pg.font.SysFont(fonts[0], font_size)
        drawable_text = font.render(str(text), 1, color)
        text_rect = drawable_text.get_rect()
        if centred:
            pos = (pos[0] - text_rect.center[0], pos[1] - text_rect.center[1])
            self.screen.blit(drawable_text, pos)
        else:
            self.screen.blit(drawable_text, pos)

    def show_fps(self):
        self.draw_text(int(self.clock.get_fps()), (0, 0))

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.debug:
            self.draw_grid()
        self.show_fps()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.debug = not(self.debug)


if __name__ == '__main__':
    game = Game()
    while True:
        game.run()
