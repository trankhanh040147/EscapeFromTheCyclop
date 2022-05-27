import pygame
import random
import numpy as np
from math import cos, sin, sqrt, pi, atan2

from obj.define import *
from obj.map import *
from obj.AStar import *


class Monster(pygame.sprite.Sprite):

    def __init__(self, position, Map):
        # init sprite để quản lý obj
        pygame.sprite.Sprite.__init__(self)
        
        # Vận tốc
        self.speed = MONSTER_SPEED

        # vector di chuyển
        self.movex = 0
        self.movey = 0     
        
        # Ảnh gốc
        self.image_original = pygame.transform.rotate(self.AddImage("./assets/img/MONSTER/monster1.png"), 90)
        
        # Góc xoay nhân vật
        self.angle = 0

        # Góc xoay mặt\
        self.face_angle = 0

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

        self.path = [[self.position[0] + PLAYER_SIZE[0]/2, self.position[1] + PLAYER_SIZE[1]/2]]
        self.index = 0

        self.speed_sqrt2 = self.speed*sqrt(2)

        # Ma trận kề các blocks
        self.maze = Map.maze

        # Các map nhỏ (arena)
        self.arena = arena = [[],[],[],[]]
        self.initArena(0,0,0,8,14)
        self.initArena(1,0,14,8,29)
        self.initArena(2,8,0,16,14)
        self.initArena(3,8,14,16,29)

        # Toạ độ để tịnh tiến từ maze về arena
        self.arenaDiff = [[0,0],[0,-14],[-8,0],[-8,-14]]
    
    def AddImage(self, path):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, MONSTER_SIZE)
        img.convert_alpha() 
        img.set_colorkey(ALPHA)
        return img

    def control(self, x, y):
        self.movex += x
        self.movey += y

   # Check chạm tường HEIGHT
    def isMovableX(self, x, blocks):
        t = MONSTER_RADIUS
        if x < 0:
            t = -t
        for block in blocks:
            if block.collidepoint([self.rect.center[0] + x + t, self.rect.center[1]]):
                return False
        return True
    
    # Check chạm tường WIDTH
    def isMovableY(self, y, blocks):
        t = MONSTER_RADIUS
        if y < 0:
            t = -t
        for block in blocks:
            if block.collidepoint([self.rect.center[0], self.rect.center[1] + y + t]):
                return False
        return True     

    def rotate(self):
        # Xoay hình
        self.image = pygame.transform.rotate(self.image_original, self.face_angle)
        
        # Tìm vị trí vẽ hình mới
        p1 = self.image.get_size()
        p0 = self.image_original.get_size()
        beta = ((p1[0]-p0[0])/2,(p1[1] - p0[1])/2)
        self.rect[0] = self.position[0] - beta[0]
        self.rect[1] = self.position[1] - beta[1]
        
        # Xoá khung
        self.image.set_colorkey(ALPHA)

    def attack(self, player_pos):
        if self.rect.collidepoint(player_pos):
            return True
        return False

    def update(self, player, blocks):
        # AI tim vi tri tiep theo
        if player.isNextSquare:
            temp = self.__AI__(player.position_center)
            self.index = 0
            if temp != None:
                self.path = temp
                self.path.append(player.position_center)
            else:
                self.path = [[self.position[0] + PLAYER_SIZE[0]/2, self.position[1] + PLAYER_SIZE[1]/2]]

        # Vị trí tiếp theo
        pos = player.rect.center
        if self.index < len(self.path):
            pos = self.path[self.index]
        else:
            self.index = 0

        # Tìm góc so với pos
        self.angle = 180/pi*atan2(-(pos[1]-self.rect.centery),(pos[0]-self.rect.centerx))

        # Tính toán vector vận tốc\
        if len(self.path) > 1:
            self.movex = self.speed * cos(self.angle/180*pi)
            self.movey = -self.speed * sin(self.angle/180*pi)

            vector_r = (self.rect.center[0] - self.path[self.index][0], self.rect.center[1] - self.path[self.index][1])
            radius = sqrt(vector_r[0]**2 + vector_r[1]**2)
            if 0 < radius and radius < self.speed_sqrt2:
                self.index += 1

            # MONSTER tấn công
            self.hit_player = self.attack(player.position_center)

            # Di chuyển Monster
            if (self.isMovableX(self.movex, blocks)):
                self.position[0] = self.position[0] + self.movex
            if (self.isMovableY(self.movey, blocks)):
                self.position[1] = self.position[1] + self.movey
            self.position_center = [self.position[0] + PLAYER_SIZE[0]/2, self.position[1] + PLAYER_SIZE[1]/2]
            self.rect[0], self.rect[1] = self.position

            self.face_angle = 180/pi*atan2(-(player.rect.center[1]-self.rect.centery),(player.rect.center[0]-self.rect.centerx))
            # Xoay ảnh hướng đến vị trí tiếp theo
            self.rotate()
            self.path[len(self.path)-1] = player.position_center
        else:
            self.movex = 0
            self.movey = 0

    def initArena(self,arena_num,x1,y1,x2,y2):
        """Khởi tạo arena với:
        x1,y1: Toạ độ điểm nhỏ góc trái trên
        x2,y2: Toạ đổ điểm góc phải dưới"""

        self.arena[arena_num] = []

        col = y2-y1+1
        #Số hàng
        row = x2-x1+1
        #Số cột

        for i in range(0,row):
            self.arena[arena_num].append(col*[0])

        for x in range(0,row):
            for y in range(0,col):
                self.arena[arena_num][x][y] = self.maze[x1+x][y1+y]


    def toPos(self,p):
        """Chuyển toạ độ pixel --> toạ độ khối blocks"""
        # Lấy số dư
        # rx= p[0] % BLOCK_SIZE[0]
        # ry = p[1] % BLOCK_SIZE[1]

        xpos = p[0]//BLOCK_SIZE[0] 
        ypos = p[1]//BLOCK_SIZE[1] 

        # if xpos == -1: xpos = 0
        # if ypos == -1: ypos = 0 

        # return (xpos,ypos)
        return [int(xpos),int(ypos)]

            

    def toPixel(self,p):
        """Chuyển toạ độ khối block --> toạ độ pixel (lấy giá trị giữa khối block)"""
        x = p[1]*BLOCK_SIZE[0] + BLOCK_SIZE[1]//2
        y = p[0]*BLOCK_SIZE[1] + BLOCK_SIZE[0]//2
        return [x,y]    
        
    def toArena(self,pos):
        """Kiểm tra xem toạ độ pos đang nằm ở area nào"""
        x = pos[0]
        y = pos[1]

        if 0<=x<=8 and 0<=y<=14:
            return 0
        elif 0<=x<=8 and 15<=y<=29:
            return 1
        elif 9<=x<=16 and 0<=y<=14:
            return 2
        elif 9<=x<=16 and 15<=y<=29:
            return 3
        else: return -1


    def __AI__(self, pos):

        player_pos= [pos[1],pos[0]]
        monster_pos= [self.rect.center[1],self.rect.center[0]]

        Monster_arena = self.toArena(self.toPos(monster_pos))
        Player_arena = self.toArena(self.toPos(player_pos))

        if Monster_arena == Player_arena:


            start = self.toPos(monster_pos)
            start[0]+=self.arenaDiff[Monster_arena][0]
            start[1]+=self.arenaDiff[Monster_arena][1]

            goal = self.toPos(player_pos)
            goal[0]+=self.arenaDiff[Monster_arena][0]
            goal[1]+=self.arenaDiff[Monster_arena][1]   

            Path = []
            Path = astar(self.arena[Monster_arena], tuple(start), tuple(goal))
            
            path = []
            if Path:
                for p in Path:
                    p = list(p)
                    p[0]=p[0]-self.arenaDiff[Monster_arena][0]
                    p[1]=p[1]-self.arenaDiff[Monster_arena][1]
                    path.append(p)

    
            self.path.clear()

            if path is []:
                return None

            path_pix = []
            for p in path:
                path_pix.append((self.toPixel(p)))
            return path_pix[1::]
        else:
            """Nếu monster nằm khác arena với player
            Thì monster sẽ di chuyển ngẫu nhiên hoặc đứng phục kích tại một địa điểm bất kì trong Arena đó"""

            if np.random.rand() > 0.1: 
                flag = True
                while flag:
                    x = random.randint(1,7)
                    y = random.randint(1,13)
                    x_arena= x - self.arenaDiff[Monster_arena][0]
                    y_arena= y - self.arenaDiff[Monster_arena][1]
                    if self.maze[x_arena][y_arena] == 0 and [x_arena,y_arena] != self.toPos(monster_pos) :
                        #Nểu random trúng vị trí block thì làm lại
                        flag = False

                destination = self.toPixel([x_arena,y_arena])

                return self.__AI__(destination) 

            else:
                return None

