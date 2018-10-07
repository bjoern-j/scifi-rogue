'''
Created on 6 Oct 2018

@author: bjoern
'''
import unittest
from Creatures.Player import Player, Archetypes
from Mechanics.Game import Game
from Mechanics.Level import LevelInfo


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_player_info(self):
        self._assert_archetype_is_in_info(Archetypes.CITIZEN)
        self._assert_archetype_is_in_info(Archetypes.ZEALOT)
        self._assert_archetype_is_in_info(Archetypes.MUTANT)
        
    def test_map_info(self):
        game = Game(Player(Archetypes.CITIZEN))
        game.start_first_level()
        map_info = game.get_map_info()
        self.assertTrue(isinstance(map_info, LevelInfo))
        
    def _assert_archetype_is_in_info(self, archetype):
        player = Player(archetype)
        game = Game(player)
        player_info = game.get_player_info()
        self.assertEqual(player_info.archetype, archetype)

