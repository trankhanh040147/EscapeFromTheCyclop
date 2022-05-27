import pygame
from obj.define import *

class Block(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        # Ảnh
        self.image = pygame.transform.scale(pygame.image.load("./assets/img/BLOCK/block2.png"), BLOCK_SIZE)

        # Vị trí
        '''


        - Dùng hệ thống lưới tương tự 2D-array
        - 1 ô kích thước BLOCK_SIZE
        - width: 0 - 29
        - height: 0 - 16


        '''
        self.rect = self.image.get_rect()
        self.rect[0] = position[0] * BLOCK_SIZE[0]
        self.rect[1] = position[1] * BLOCK_SIZE[1]
        