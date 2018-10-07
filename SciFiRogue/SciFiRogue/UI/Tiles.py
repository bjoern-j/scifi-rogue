'''
Created on 7 Oct 2018

@author: bjoern
'''
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GdkPixbuf

import os

class TileProvider(object):
    def __init__(self):
        self._tiles = {}
        ui_dir = os.path.dirname(os.path.abspath(__file__))
        self._tiles["player"] = GdkPixbuf.Pixbuf.new_from_file(ui_dir+"/Tiles/player_at.png")
        self._tiles["metal_wall"] = GdkPixbuf.Pixbuf.new_from_file(ui_dir+"/Tiles/metal_wall.png")
        self._tiles["metal_floor"] = GdkPixbuf.Pixbuf.new_from_file(ui_dir+"/Tiles/metal_floor.png")
        
    def get_tile(self, id):
        return self._tiles[id]