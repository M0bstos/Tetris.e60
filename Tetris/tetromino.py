from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + START_POSITION
        self.next_pos = vec(pos) + NEXT_POSITION
        self.alive = True
        self.alpha = 255

        super().__init__(tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
      x_offset = (WIN_W - FIELD_RES[0]) // 2
      y_offset = (WIN_H - FIELD_RES[1]) // 2
      pos = [self.next_pos, self.pos][self.tetromino.current]
      self.rect.topleft = (pos.x * TILE_SIZE + x_offset, pos.y * TILE_SIZE + y_offset)

    def update(self):
        self.is_alive()
        self.set_rect_pos()

    def collision(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
                y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.image = random.choice(tetris.app.images)
        self.blocks = [Block(self, pos)for pos in TETROMINOES[self.shape]]
        self.landing = False
        self.current = current
    
    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.collision(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
    
    def collision(self, block_positions):
        return any(map(Block.collision, self.blocks, block_positions))

    def move(self, direction):
        move_direction  = MOVEMENT[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        collision = self.collision(new_block_positions)

        if not collision:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def update(self):
        self.move(direction='down')

    def draw_next(self, screen, x, y):
        for block in self.blocks:
            block_rect = block.image.get_rect()
            block_rect.topleft = (x + block.next_pos.x * TILE_SIZE, y + block.next_pos.y * TILE_SIZE)
            screen.blit(block.image, block_rect)

