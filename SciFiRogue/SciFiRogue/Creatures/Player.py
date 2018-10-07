'''
Created on 6 Oct 2018

@author: bjoern
'''

class Archetypes(object):
    CITIZEN = 1
    MUTANT  = 2
    ZEALOT  = 3
    @staticmethod
    def to_string(archetype):
        if   archetype == Archetypes.CITIZEN:
            return "Citizen"
        elif archetype == Archetypes.MUTANT:
            return "Mutant"
        elif archetype == Archetypes.ZEALOT:
            return "Zealot"
        
class PlayerInfo(object):
    def __init__(self, player):
        self.archetype = player._archetype
    
class Player(object):
    def __init__(self, archetype):
        self._archetype = archetype
        
    def blocks_passage(self):
        return True
    
    def get_info(self):
        return PlayerInfo(self)
