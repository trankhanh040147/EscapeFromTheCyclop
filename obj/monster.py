import pygame
from math import atan2
from math import pi

from obj.define import *
from obj.map import *
from obj.bullet import *

class Monster(pygame.sprite.Sprite):

    def __init__(self, position):
        # init sprite để quản lý obj
        pygame.sprite.Sprite.__init__(self)
        
        # Vận tốc
        self.speed = MONSTER_SPEED

        # vector di chuyển
        self.movex = 0
        self.movey = 0     
        
        # Ảnh gốc
        self.image_original = self.AddImage("./assets/img/MONSTER/monster1.png")
        
        # Góc xoay nhân vật
        self.angle = 0

        # Ảnh thật (đã xoay)
        self.image = self.image_original
        
        # vị trí vẽ
        self.rect = self.image_original.get_rect()
        self.rect[0], self.rect[1] = position

        # vị trí nhân vật
        self.position = list(position)
        self.position_center = [position[0] + PLAYER_SIZE[0]/2, position[1] + PLAYER_SIZE[1]/2]

        # monster hit player
        self.hit_player = False
    
    def AddImage(self, path):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, MONSTER_SIZE)
        img.convert_alpha() 
        img.set_colorkey(ALPHA)
        return img

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def isMovableX(self, x):
        if self.position[0] + x < 0 or self.position[0] + x > WORLD_X - MONSTER_SIZE[0]:
            return False
        return True
    
    def isMovableY(self, y):
        if self.position[1] + y < 0 or self.position[1] + y > WORLD_Y - MONSTER_SIZE[0]:
            return False
        return True    

    def rotate(self, pos):
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

    def attack(self, player_rect):
        if player_rect.collidepoint(self.rect.center):
            return True
        return False

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
            (rect[0] - MONSTER_RADIUS + self.movex, rect[1] - MONSTER_RADIUS + self.movey),             
            (rect[0] - MONSTER_RADIUS + self.movex, rect[1] + MONSTER_RADIUS + self.movey), 
            (rect[0] + MONSTER_RADIUS + self.movex, rect[1] - MONSTER_RADIUS + self.movey), 
            (rect[0] + MONSTER_RADIUS + self.movex, rect[1] + MONSTER_RADIUS + self.movey), 
                )

    def update(self, player, blocks):
        # AI tim vi tri tiep theo
        pos = self.__AI__(player.position_center)

        # Tìm góc so với vị trí chuột
        self.angle = 180/pi*atan2(-(pos[1]-self.rect.centery),(pos[0]-self.rect.centerx))

        # Tính toán vector vận tốc
        self.movex = self.speed * cos(self.angle/180*pi)
        self.movey = -self.speed * sin(self.angle/180*pi)

        # MONSTER tấn công
        self.hit_player = self.attack(player.rect)

        # Di chuyển Monster
        if self.isMovable(blocks):
            if (self.isMovableX(self.movex)):
                self.position[0] = self.position[0] + self.movex
            if (self.isMovableY(self.movey)):
                self.position[1] = self.position[1] + self.movey
        self.position_center = [self.position[0] + PLAYER_SIZE[0]/2, self.position[1] + PLAYER_SIZE[1]/2]
        self.rect[0], self.rect[1] = self.position
        # Xoay ảnh hướng đến vị trí tiếp theo
        self.rotate(pos)

    def __AI__(self, pos):
        # Viết code AI ở đây
        return pos