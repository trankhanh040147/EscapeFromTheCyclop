import pygame
from math import atan2
from math import pi

from obj.define import *
from obj.map import *

class Player(pygame.sprite.Sprite):
    steps = PLAYER_SPEED
    def __init__(self, position=PLAYER_START_POS):
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
        self.rect[0], self.rect[1] = [position[0], position[1]]

        # vị trí nhân vật
        self.position = [position[0], position[1]]
        self.position_center = [position[0] + PLAYER_SIZE[0]/2, position[1] + PLAYER_SIZE[1]/2]

        # Player square
        self.square = [self.position_center[0]//BLOCK_SIZE[0], self.position_center[1]//BLOCK_SIZE[0]]

        # is next square
        self.isNextSquare = False
    
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
    def isMovableX(self, x, blocks):
        t = PLAYER_RADIUS
        if x < 0:
            t = -t
        for block in blocks:
            if block.collidepoint([self.position_center[0] + x + t, self.position_center[1]]):
                return False
        return True
    
    # Check chạm tường WIDTH
    def isMovableY(self, y, blocks):
        t = PLAYER_RADIUS
        if y < 0:
            t = -t
        for block in blocks:
            if block.collidepoint([self.position_center[0], self.position_center[1] + y + t]):
                return False
        return True 

    def update(self, pos, blocks):
        # Di chuyển nhân vật
        if (self.isMovableX(self.movex, blocks)):
            self.position[0] = self.position[0] + self.movex
        if (self.isMovableY(self.movey, blocks)):
            self.position[1] = self.position[1] + self.movey
        self.rect[0], self.rect[1] = self.position
        self.position_center = [self.position[0] + PLAYER_SIZE[0]/2, self.position[1] + PLAYER_SIZE[1]/2]
        if self.movex != 0 or self.movey!=0:
            self.rotate((self.rect.center[0] + self.movex, self.rect.center[1]+self.movey))
        self.isNextSquare = self.is_nextSquare()


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

    def is_nextSquare(self):
        new_square = [self.position_center[0]//BLOCK_SIZE[0], self.position_center[1]//BLOCK_SIZE[0]]
        if new_square != self.square:
            self.square = new_square
            return True 
        return False
