import pygame
from obj.define import *
from obj.monster import *
from obj.block import *

class map:
    MAP_IMAGE = {
        'HOME': pygame.transform.scale(pygame.image.load('./assets/img/MAP/map1.png'), (WORLD_X, WORLD_Y)),
    }

    def __init__(self, currentMap_string):
        self.maze = self.initialMaze()
        self.currentMap = self.MAP_IMAGE[currentMap_string]
        self.BLOCKs = pygame.sprite.Group()
        self.BLOCKs_position = []
        self.__readMap__(MAP_NAME)

    #Khánh
    def initialMaze(self):
        #Tao ma tran ke chua cac vi tri cac blocks
        mz = [] 
        list = []
        maxRow =  17
        maxCol =  30
        for i in range(0,maxCol):
            list.append(0)
        for j in range(0,maxRow):
            mz.append(list.copy())
        return mz

    def __readMap__(self, name:str):
        # read txt
        f = open("./assets/data/MAP/" + name + ".txt")
        self.BLOCKs_position = f.read().split("\n")
        f.close()

        # txt to tuple[tuple[int]]
        for i in range(0, len(self.BLOCKs_position)):
            self.BLOCKs_position[i] = self.BLOCKs_position[i].split(" ")
            self.BLOCKs_position[i][0] = int(self.BLOCKs_position[i][0])
            self.BLOCKs_position[i][1] = int(self.BLOCKs_position[i][1])
            self.BLOCKs_position[i][0],self.BLOCKs_position[i][1] = self.BLOCKs_position[i][1],self.BLOCKs_position[i][0]
            self.maze[self.BLOCKs_position[i][1]][self.BLOCKs_position[i][0]] = 1

            # add Block
            self.BLOCKs.add(Block(self.BLOCKs_position[i]))
        
        self.BLOCKs_position.clear()
        for block in self.BLOCKs:
            self.BLOCKs_position.append(block.rect)

    def update(self):
        return self.currentMap

