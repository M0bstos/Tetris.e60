import asyncio
from settings import *
from tetris import Tetris, Text
import sys
import pathlib

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        pg.mixer.music.load(BG_MUSIC_PATH)
        pg.mixer.music.set_volume(0.35) 
        pg.mixer.music.play(-1)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images
    
    def timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIMATION_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIMATION_INTERVAL)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=FIELD_COLOR)
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
