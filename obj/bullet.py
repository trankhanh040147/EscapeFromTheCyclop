import pygame
from math import sin
from math import cos
from math import pi
from obj.define import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, position):
        pygame.sprite.Sprite.__init__(self)

        # Ảnh gốc
        self.image_original = pygame.transform.scale(pygame.image.load('./assets/img/BULLET/bullet1.png'), BULLET_SIZE)
        
        # Tốc độ
        self.speed = 10
        
        # Vị trí thật của đán
        self.position = list(position)
        self.rect = self.image_original.get_rect()

        # Vector vận tốc
        self.movex = self.speed * cos(angle/180*pi)
        self.movey = -self.speed * sin(angle/180*pi)

        # Ảnh thật (đã xoay)
        self.image = self.rotate(angle)

        # Vị trí vẽ ảnh
        self.rect = self.image.get_rect()
        #self.rect[0], self.rect[1] = position

    def isMovableX(self, x):
        if self.position[0] + x < 0 or self.position[0] + x > WORLD_X:
            return False
        return True
    
    def isMovableY(self, y):
        if self.position[1] + y < 0 or self.position[1] + y > WORLD_Y:
            return False
        return True 

    def rotate(self, angle):        
        # Xoay hình
        image = pygame.transform.rotate(self.image_original, angle)
        
        # Tìm vị trí vẽ hình mới
        p1 = image.get_size()
        p0 = self.image_original.get_size()
        beta = ((p1[0]-p0[0])/2,(p1[1] - p0[1])/2)
        self.rect[0] = self.position[0] - beta[0]
        self.rect[1] = self.position[1] - beta[1]
        
        # Xoá khung
        image.set_colorkey(ALPHA)
        return image

    def isMovable(self, blocks):
        for block in blocks:
            if block.collidepoint(self.rect.topleft) or block.collidepoint(self.rect.bottomright):
                return False
        return True

    def update(self):
        self.position[0] = self.position[0] + self.movex
        self.position[1] = self.position[1] + self.movey
        self.rect[0], self.rect[1] = self.position
