from obj.define import *
import pygame
from obj.map import *
from obj.player import *
from obj.monster import *
from obj.block import *
from obj.rand_map import *

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
        self.WORLD = pygame.display.set_mode((WORLD_X, WORLD_Y))    
        self.backdropbox = self.WORLD.get_rect()
    
    def endProcess(self):
        pygame.quit()

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
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
                self.PLAYER.attack()
                if self.admin_mode:
                    pos = (int(pygame.mouse.get_pos()[0]/BLOCK_SIZE[0]),int(pygame.mouse.get_pos()[1]/BLOCK_SIZE[1]))
                    self.MAP.BLOCKs.add(Block(pos))
                    addbox(pos)
        return True
     
    def update(self):
        #update map => background, link switch map
        backdrop = self.MAP.update()
        self.WORLD.blit(backdrop, self.backdropbox)

        self.update_Objects()
        self.draw_Objects()

        self.is_Endgame()

        #update new screen
        pygame.display.flip()
        self.clock.tick(FPS)

    def update_Objects(self):
        self.MAP.BLOCKs.update()
        self.PLAYERs.update(pygame.mouse.get_pos(), self.MAP.BLOCKs_position)
        self.MONSTERs.update(self.PLAYER, self.MAP.BLOCKs_position)
        self.PLAYER.bullets.update()

        # bullet hit monster
        for bullet in self.PLAYER.bullets:
            for monster in self.MONSTERs:
                if monster.rect.collidepoint(bullet.rect.topleft) or monster.rect.collidepoint(bullet.rect.bottomright):
                    self.MONSTERs.remove(monster)
                    self.PLAYER.bullets.remove(bullet)
                    break

    def draw_Objects(self):
        self.MAP.BLOCKs.draw(self.WORLD)
        self.PLAYERs.draw(self.WORLD)
        self.MONSTERs.draw(self.WORLD)
        self.PLAYER.bullets.draw(self.WORLD)

    def is_Endgame(self):
        # Check END GAME
        for monster in self.MONSTERs:
            if monster.hit_player:
                self.active = False
                break

    def create_newPlayer(self):
        self.PLAYER = Player(PLAYER_START_POS)
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
            string = f.read().split(".")
            f.close()

            # txt to tuple[tuple[int]]
            for i in range(0, len(string)):
                string[i] = string[i].split(" ")
                string[i][0] = int(string[i][0])
                string[i][1] = int(string[i][1])
            return string
        
        positions = __readMap__("map1")
        for position in positions:
            monster = Monster(position)
            self.MONSTERs.add(monster)

# import os
# print(os.listdir("./assets/img"))
process = Program()
process.startProcess()
process.main()
process.endProcess()