import pygame
from math import atan2
from math import pi

from obj.define import *
from obj.map import *
from obj.bullet import *

class Player(pygame.sprite.Sprite):
    steps = PLAYER_SPEED
    def __init__(self, position):
        # init sprite để quản lý obj
        pygame.sprite.Sprite.__init__(self)
        
        # vector di chuyển
        self.movex = 0
        self.movey = 0     
        
        # Ảnh gốc
        self.image_original = self.AddImage("./assets/img/PLAYER/player1.png")
        
        # Góc xoay nhân vật
        self.angle = 0

        # Ảnh thật (đã xoay)
        self.image = self.image_original
        
        # vị trí vẽ
        self.rect = self.image_original.get_rect()
        self.rect[0], self.rect[1] = position

        # vị trí nhân vật
        self.position = position
        self.position_center = [position[0] + PLAYER_SIZE[0]/2, position[1] + PLAYER_SIZE[1]/2]

        # Đạn đang được bắn
        self.bullets = pygame.sprite.Group()
    
    def AddImage(self, path):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, PLAYER_SIZE)
        img.convert_alpha() 
        img.set_colorkey(ALPHA)
        return img

    def control(self, x, y):
        self.movex += x
        self.movey += y

    # Check chạm tường HEIGHT
    def isMovableX(self, x):
        if self.position[0] + x < 0 or self.position[0] + x > WORLD_X - PLAYER_SIZE[0]:
            return False
        return True
    
    # Check chạm tường WIDTH
    def isMovableY(self, y):
        if self.position[1] + y < 0 or self.position[1] + y > WORLD_Y - PLAYER_SIZE[0]:
            return False
        return True    

    def isMovable(self, blocks):
        for block in blocks:
            corners = self.get_corners(self.position_center)
            if block.collidepoint(corners[0])\
                or block.collidepoint(corners[1])\
                    or block.collidepoint(corners[2])\
                        or block.collidepoint(corners[3]):
                return False
        return True

    def get_corners(self, rect):
        return (
            (rect[0] - PLAYER_RADIUS + self.movex, rect[1] - PLAYER_RADIUS + self.movey),             
            (rect[0] - PLAYER_RADIUS + self.movex, rect[1] + PLAYER_RADIUS + self.movey), 
            (rect[0] + PLAYER_RADIUS + self.movex, rect[1] - PLAYER_RADIUS + self.movey), 
            (rect[0] + PLAYER_RADIUS + self.movex, rect[1] + PLAYER_RADIUS + self.movey), 
                )

    def update(self, pos, blocks):
        # Di chuyển nhân vật
        if self.isMovable(blocks):
            if (self.isMovableX(self.movex)):
                self.position[0] = self.position[0] + self.movex
            if (self.isMovableY(self.movey)):
                self.position[1] = self.position[1] + self.movey
            self.rect[0], self.rect[1] = self.position
            self.position_center = [self.position[0] + PLAYER_SIZE[0]/2, self.position[1] + PLAYER_SIZE[1]/2]
        self.rotate(pos)

        # Xóa đạn dư
        for bullet in self.bullets:
            if not (bullet.isMovableX(bullet.movex) and bullet.isMovableY(bullet.movey)) or not bullet.isMovable(blocks):
                self.bullets.remove(bullet)
                del bullet

    def rotate(self, pos):
        # Tìm góc so với vị trí chuột
        self.angle = 180/pi*atan2(-(pos[1]-self.rect.centery),(pos[0]-self.rect.centerx))
        
        # Xoay hình
        self.image = pygame.transform.rotate(self.image_original, self.angle)
        
        # Tìm vị trí vẽ hình mới
        p1 = self.image.get_size()
        p0 = self.image_original.get_size()
        beta = ((p1[0]-p0[0])/2,(p1[1] - p0[1])/2)
        self.rect[0] = self.position[0] - beta[0]
        self.rect[1] = self.position[1] - beta[1]
        
        # Xoá khung
        self.image.set_colorkey(ALPHA)

    def attack(self):
        bullet = Bullet(self.angle, self.rect.center)
        self.bullets.add(bullet)
