'''
Created on 6 Oct 2018

@author: bjoern
'''
import unittest
from Mechanics.Level import Level, Wall


class Test(unittest.TestCase):
    def setUp(self):
        self._level = Level(4,4)

    def tearDown(self):
        pass

    def test_placeWall(self):
        self._level.place((2,2), Wall(Wall.Types.METAL))
        things = self._level.get_things((2,2))
        self.assertEqual(len(things),1)
        self.assertEqual(things[0]._type, Wall.Types.METAL)
        self.assertTrue(self._level.is_passable((1,1)))
        self.assertFalse(self._level.is_passable((2,2)))
        
    def test_level_info(self):
        level_info = self._level.get_info()
        for _, cell in level_info.cells.items():
            self.assertTrue(cell.is_empty)
        self._level.place((2,2), Wall(Wall.Types.METAL))
        level_info = self._level.get_info()
        self.assertFalse(level_info.cells[(2,2)].is_empty)
        self.assertEqual(level_info.cells[(2,2)].things[0].wall_type, Wall.Types.METAL)
