'''
Created on 6 Oct 2018

@author: bjoern
'''
class WallInfo(object):
    def __init__(self, wall):
        self.wall_type = wall._type

class Wall(object):
    class Types(object):
        METAL = 1
    def __init__(self, _type):
        self._type = _type 
        
    def blocks_passage(self):
        return True 
    
    def get_info(self):
        return WallInfo(self)

class Cell(object):
    def __init__(self):
        self._things      = []
        self._is_passable = True
    
    def add_thing(self, thing):
        self._things.append(thing)
        if self._is_passable:
            self._is_passable = not thing.blocks_passage()
        
    def get_things(self):
        return self._things
    
    def is_passable(self):
        return self._is_passable
    
class CellInfo(object):
    def __init__(self, cell):
        self.is_empty = (len(cell._things) == 0)
        self.things = []
        for thing in cell._things:
            self.things.append(thing.get_info())
    
class LevelInfo(object):
    def __init__(self, level):
        self.width_x = level._width_x
        self.width_y = level._width_y
        self.cells = {}
        for x in range(level._width_x):
            for y in range(level._width_y):
                self.cells[(x,y)] = CellInfo(level._cells[(x,y)])
             

class Level(object):
    def __init__(self, width_x, width_y):
        self._width_x = width_x 
        self._width_y = width_y
        self._cells   = {}
        for x in range(width_x):
            for y in range(width_y):
                self._cells[(x,y)] = Cell() 

    def place(self, position, thing):
        self._cells[position].add_thing(thing)
    
    def get_things(self, position):
        return self._cells[position].get_things()
    
    def is_passable(self, position):
        return self._cells[position].is_passable()
    
    def get_info(self):
        return LevelInfo(self)