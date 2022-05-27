from obj.define import *
import pygame
from obj.map import *
from obj.player import *
from obj.monster import *
from obj.block import *

class Program: 
    def __init__(self):
        #active = true: chương trình hoạt động
        self.active = True
        self.MAP = map("HOME")
        self.clock = pygame.time.Clock()
        self.PLAYERs = pygame.sprite.Group()
        self.MONSTERs = pygame.sprite.Group()
        # Cờ quản lý số key đang nhấn 
        self.__key_manager__ = 0

        self.counter = 3000.00

        self.is_start = False

        # Cờ addmin
        self.admin_mode = False

    def main(self): 
        self.create_newPlayer()
        self.create_ListMonster()
        while self.active:
            self.active = self.checkEvent()
            self.update()
            
    def startProcess(self):
        pygame.init()
        self.myfont = pygame.font.Font("./assets/fonts/font.ttf", 15)
        self.WORLD = pygame.display.set_mode((WORLD_X, WORLD_Y))    
        self.backdropbox = self.WORLD.get_rect()
    
    def endProcess(self):
        myfont = pygame.font.Font("./assets/fonts/font.ttf", 100)
        label = myfont.render('YOU WIN', True, (GREEN))
        if self.counter > 0:
            label = myfont.render('GAME OVER', True, RED)
        label_rect = label.get_rect(center=(WORLD_X/2, WORLD_Y/2))
        count = 200
        while count > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    self.is_start = True
                    if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                        return False
            self.WORLD.fill(BLACK)
            self.WORLD.blit(label, (label_rect))
            pygame.display.flip()
            self.clock.tick(FPS)
            count -= 1


    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                self.is_start = True
                if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.PLAYER.control(-Player.steps, 0)
                    self.__key_manager__ += 1

                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.PLAYER.control(Player.steps, 0)
                    self.__key_manager__ += 1

                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.PLAYER.control(0, -Player.steps)
                    self.__key_manager__ += 1

                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.PLAYER.control(0, Player.steps)
                    self.__key_manager__ += 1
                

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.PLAYER.control(Player.steps, 0)
                    self.__key_manager__ -= 1

                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.PLAYER.control(-Player.steps, 0)
                    self.__key_manager__ -= 1

                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.PLAYER.control(0, Player.steps)
                    self.__key_manager__ -= 1

                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.PLAYER.control(0, -Player.steps)
                    self.__key_manager__ -= 1

            elif self.__key_manager__ == 0:
                self.PLAYER.movex = 0
                self.PLAYER.movey = 0
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.admin_mode:
                    pos = (int(pygame.mouse.get_pos()[0]/BLOCK_SIZE[0]),int(pygame.mouse.get_pos()[1]/BLOCK_SIZE[1]))
                    self.MAP.BLOCKs.add(Block(pos))
                    #addbox(pos)
                    
        return True
     
    def update(self):
        #update map => background, link switch map
        backdrop = self.MAP.update()
        self.WORLD.blit(backdrop, self.backdropbox)

        self.update_Objects()
        self.draw_Objects()

        self.is_Endgame()

        self.active = self.countDown()

        pygame.display.flip()
        self.clock.tick(FPS)

    def countDown(self):
        if self.counter <= 0: 
            return False
        if self.is_start:
            self.counter -= 1

        pygame.draw.rect(self.WORLD, '#FBDE44', (BLOCK_SIZE[0], 10*U, BLOCK_SIZE[0]*4, BLOCK_SIZE[1]-20*U))

        label = self.myfont.render(f'Time: {self.counter/100}', RED, RED)
        self.WORLD.blit(label, (BLOCK_SIZE[0]+16*U-5, BLOCK_SIZE[1]/4 + 8*U))
        return self.active

    def update_Objects(self):
        self.MAP.BLOCKs.update()
        self.PLAYERs.update(pygame.mouse.get_pos(), self.MAP.BLOCKs_position)
        self.MONSTERs.update(self.PLAYER, self.MAP.BLOCKs_position)

    def draw_Objects(self):
        self.MAP.BLOCKs.draw(self.WORLD)
        self.PLAYERs.draw(self.WORLD)
        self.MONSTERs.draw(self.WORLD)
        
        if self.admin_mode:
            for monster in self.MONSTERs:
                if len(monster.path) > 1:
                    pygame.draw.lines(self.WORLD, (0,0,255), False, monster.path, 3)
                    for point in monster.path:
                        pygame.draw.circle(self.WORLD, (0,0,0), point, 3)
        
            

    def is_Endgame(self):
        # Check END GAME
        for monster in self.MONSTERs:
            if monster.hit_player:
                self.active = False
                break

    def create_newPlayer(self):
        self.PLAYER = Player()
        self.PLAYERs.add(self.PLAYER)

    def isnotBlock(self, blocks, pos):
        for block in blocks:
            if block.collidepoint(pos):
                return False
        return True

    def create_ListMonster(self):
        def __readMap__(name:str):
            # read txt
            f = open("./assets/data/MONSTER/" + name + ".txt")
            string = f.read().split("\n")
            f.close()

            # txt to tuple[tuple[int]]d
            for i in range(0, len(string)):
                string[i] = string[i].split(" ")
                string[i][0] = int(string[i][0])
                string[i][1] = int(string[i][1])
            return string
        
        positions = __readMap__(MAP_NAME)
        for position in positions:
            monster = Monster(position,self.MAP)
            self.MONSTERs.add(monster)

