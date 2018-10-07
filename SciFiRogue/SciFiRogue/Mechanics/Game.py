'''
Created on 6 Oct 2018

@author: bjoern
'''
from Mechanics.LevelGenerator import LevelGenerator
from Mechanics.Level          import LevelInfo 

class PlayerInfo(object):
    def __init__(self, player):
        self.archetype = player._archetype

class Game(object):
    def __init__(self, player):
        self._player = player 
        self._level_generator = LevelGenerator()  
        
    def get_player_info(self):
        return PlayerInfo(self._player)
    
    def start_first_level(self):
        self._current_level = self._level_generator.generate_for_depth(1)
        self._current_level.place((9,9), self._player)

    def get_map_info(self):
        return LevelInfo(self._current_level)