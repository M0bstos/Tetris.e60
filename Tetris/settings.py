import pygame as pg

vec = pg.math.Vector2

FPS = 60
FIELD_COLOR = (42, 42, 42)
DOT_COLOR = (32, 255, 6)
BORDER_COLOR = (32, 255, 6)
TEXT_COLOR = (32, 255, 6)

SPRITE_PATH = r"Tetris\assets"
FONT_PATH = r"Tetris\assets\fonts\A Goblin Appears!.otf"
FONT_PATH_2 = r"Tetris\assets\fonts\tetris-1984.ttf"
BG_MUSIC_PATH = r"Tetris\assets\music\Theme.mp3"
LINE_CLEAR_MUSIC_PATH = r"Tetris\assets\music\line_clear.mp3"

ANIMATION_INTERVAL = 150
FAST_ANIMATION_INTERVAL = 15

TILE_SIZE = 30
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.07
WIN_RES = WIN_W, WIN_H = 800,800

START_POSITION = vec(FIELD_W // 2 - 1, 0)
NEXT_POSITION =  vec(FIELD_W * 1.3, FIELD_H * 0.45)
MOVEMENT = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}
