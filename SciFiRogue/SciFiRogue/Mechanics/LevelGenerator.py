'''
Created on 7 Oct 2018

@author: bjoern
'''
from Mechanics.Level import Level, Wall

class LevelGenerator(object):
    def __init__(self):
        pass 
    
    def generate_for_depth(self, depth):
        LEVEL_SIZE_X = 20
        LEVEL_SIZE_Y = 20
        level = Level(LEVEL_SIZE_X, LEVEL_SIZE_Y)
        level.place((8,8), Wall(Wall.Types.METAL))
        return level 
