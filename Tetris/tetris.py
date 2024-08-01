from settings import *
from tetromino import Tetromino
import math
import pygame.freetype as ft
import pygame.font as pf
import pygame.time as pt
from collections import deque

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)
        self.font_2 = ft.Font(FONT_PATH_2) 

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.33, WIN_H * 0.03),
                            text='Tetris.E60', fgcolor= TEXT_COLOR,
                            size=TILE_SIZE, bgcolor= FIELD_COLOR)
        self.font.render_to(self.app.screen, (WIN_W * 0.05, WIN_H * 0.15),
                            text='Score:', fgcolor= TEXT_COLOR,
                            size=TILE_SIZE*0.5 , bgcolor= FIELD_COLOR)
        self.font.render_to(self.app.screen, (WIN_W * 0.2, WIN_H * 0.15),
                            text=f'{self.app.tetris.score}', fgcolor= TEXT_COLOR,
                            size=TILE_SIZE*0.5)
        
        attribution_text = "Inspired by the original Tetris Electronika 60 and developed by M0bstos"
        text_size = TILE_SIZE * 0.3
        text_pos = (WIN_W * 0.15, WIN_H * 0.95) 
        self.font.render_to(self.app.screen, text_pos,
                              text=attribution_text, fgcolor=TEXT_COLOR,
                              size=text_size, bgcolor=FIELD_COLOR)

class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.accelerate = False

        self.line_clear_sound = pg.mixer.Sound(LINE_CLEAR_MUSIC_PATH)
        self.line_clear_sound.set_volume(0.2)

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def check_lines(self):
     row = FIELD_H - 1
     for y in range(FIELD_H - 1, -1, -1):
        for x in range(FIELD_W):
            self.field_array[row][x] = self.field_array[y][x]

            if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)

        if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
        else:
            for x in range(FIELD_W):
                self.field_array[row][x].alive = False
                self.field_array[row][x] = 0

            self.full_lines += 1
        if self.full_lines > 0:
         self.line_clear_sound.play()
    
    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block
    
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    
    def game_over(self):
        if self.tetromino.blocks[0].pos.y == START_POSITION[1]:
            pg.time.wait(300)
            return True

    def check_landing(self):
        if self.tetromino.landing:
            if self.game_over():
                self.__init__(self.app)
            else:
                self.accelerate = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:    
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.accelerate = True

    def grid(self):
     dot_color = DOT_COLOR

     x_offset = (WIN_W - FIELD_RES[0]) // 2
     y_offset = (WIN_H - FIELD_RES[1]) // 2

     for x in range(FIELD_W):
        for y in range(FIELD_H):
            dot_x = (x + 1) * TILE_SIZE + x_offset
            dot_y = (y + 1) * TILE_SIZE + y_offset

            pg.draw.circle(self.app.screen, dot_color, (dot_x, dot_y), 1)

    def borders(self):
     border_color = TEXT_COLOR
     border_font = pf.Font(FONT_PATH, 15)
     left_border_char = "<!" 
     right_border_char = "!>"
     bottom_border_char = "="
     second_bottom_border_char = "\\/"

     x_offset = (WIN_W - FIELD_RES[0]) // 2
     y_offset = (WIN_H - FIELD_RES[1]) // 2

     border_shift_up = 5
     bottom_border_shift_up = 20
     
     for y in range(FIELD_H):
        dot_y = (y + 1) * TILE_SIZE + y_offset - border_shift_up

        left_border = border_font.render(left_border_char, True, border_color)
        right_border = border_font.render(right_border_char, True, border_color)

        self.app.screen.blit(left_border, (x_offset - TILE_SIZE// 2 - 5, dot_y))
        self.app.screen.blit(right_border, (x_offset + FIELD_RES[0] + TILE_SIZE // 2 - 5, dot_y))

     char_width = border_font.size(bottom_border_char)[0]
     num_chars = FIELD_RES[0] // char_width + 2

    # First bottom border
     for x in range(1, num_chars-1):
        dot_x = x * char_width + x_offset - char_width + 5
        bottom_dot_y = (FIELD_H + 1) * TILE_SIZE + y_offset - 5 - bottom_border_shift_up
        bottom_border = border_font.render(bottom_border_char, True, border_color)
        self.app.screen.blit(bottom_border, (dot_x, bottom_dot_y))

    # Second bottom border
     second_bottom_border_font = pf.Font(FONT_PATH, 10)
     second_char_width = second_bottom_border_font.size(second_bottom_border_char)[0]
     second_num_chars = num_chars - 8
     for x in range(second_num_chars):
      dot_x = x * second_char_width + x_offset - char_width + 8 + second_char_width
      second_bottom_dot_y = (FIELD_H + 1) * TILE_SIZE + y_offset + 10 - border_shift_up
      second_bottom_border = second_bottom_border_font.render(second_bottom_border_char, True, border_color)
      self.app.screen.blit(second_bottom_border, (dot_x, second_bottom_dot_y))

    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.accelerate]
        if trigger:
            self.check_lines()
            self.tetromino.update()
            self.check_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.grid()
        self.borders()
        self.sprite_group.draw(self.app.screen)
        self.next_tetromino.draw_next(self.app.screen, WIN_W - TILE_SIZE * 6, TILE_SIZE * 2)


