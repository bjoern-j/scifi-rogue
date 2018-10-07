'''
Created on 6 Oct 2018

@author: bjoern
'''
import gi
from Creatures.Player import Archetypes, Player, PlayerInfo
from Mechanics.Game import Game
from UI.Tiles import TileProvider
from Mechanics.Level import WallInfo
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class StyleProviders(object):
    _MAIN_STYLE_CSS = b"""
    window {
        background-color: #000;
        color:            #0F0;
        font-family:      "Telegrama";
    }
    """
    _ERROR_STYLE_CSS = b"""
    label {
        background-color: #000;
        color:            #F00;
        font-family:      "Telegrama";
    }
    """
    MAIN_STYLE  = Gtk.CssProvider()
    MAIN_STYLE.load_from_data(_MAIN_STYLE_CSS)
    ERROR_STYLE = Gtk.CssProvider()
    ERROR_STYLE.load_from_data(_ERROR_STYLE_CSS)
    
class MouseButtons(object):
    LEFT  = 1
    RIGHT = 1

class StartButton(Gtk.EventBox):
    def __init__(self, main_window):
        super(StartButton, self).__init__()
        self._main = main_window
        self.add(Gtk.Label("Start the Game!"))
        self.connect("button-release-event", self.start)
        
    def start(self, widget, event):
        if event.button == MouseButtons.LEFT:
            self._main.open_character_creator()
            
class CharacterCreator(Gtk.Grid):
    class ArchetypeChoice(Gtk.EventBox):
        def __init__(self, text, archetype, creator):
            super(CharacterCreator.ArchetypeChoice,self).__init__()   
            self._creator   = creator
            self._archetype = archetype
            self.add(Gtk.Label(text))
            self.connect("button-release-event", lambda w,e : self._creator.process_archetype_choice(self._archetype) )
            
    class ErrorLabel(Gtk.Label):
        def __init__(self, text):
            super(CharacterCreator.ErrorLabel,self).__init__(text)
            self.get_style_context().add_provider(StyleProviders.ERROR_STYLE, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION) 
    FULL_WIDTH = 10
    def __init__(self, main_window):
        super(CharacterCreator, self).__init__()
        self._main = main_window
        heading = Gtk.Label("Choose your archetype")
        heading.set_justify(Gtk.Justification.CENTER)
        self.attach(heading, top=1, left=1, width=CharacterCreator.FULL_WIDTH, height=1)
        self.keyboard_buttons = {}
        self.keyboard_buttons[Gdk.KEY_a] = CharacterCreator.ArchetypeChoice( "a - Citizen     ", Archetypes.CITIZEN, self)
        self.keyboard_buttons[Gdk.KEY_b] = CharacterCreator.ArchetypeChoice( "b - Zealot      ", Archetypes.ZEALOT , self)
        self.keyboard_buttons[Gdk.KEY_c] = CharacterCreator.ArchetypeChoice( "c - Mutant      ", Archetypes.MUTANT , self)
        self.attach(self.keyboard_buttons[Gdk.KEY_a], top=2, left=1, width=1, height=1 )
        self.attach(self.keyboard_buttons[Gdk.KEY_b] , top=2, left=3, width=1, height=1 )
        self.attach(self.keyboard_buttons[Gdk.KEY_c], top=2, left=5, width=1, height=1 )
        self.attach(CharacterCreator.ErrorLabel("d - Locked      "), top=3, left=1, width=1, height=1 )
        self.attach(CharacterCreator.ErrorLabel("e - Locked      "), top=3, left=3, width=1, height=1 )
        self.attach(CharacterCreator.ErrorLabel("f - Locked      "), top=3, left=5, width=1, height=1 )
        
    def process_archetype_choice(self, archetype):
        self._main.start_game(Player(archetype))
        
    def handle_key_press(self, widget, event):
        try:
            self.process_archetype_choice(self.keyboard_buttons[event.keyval]._archetype)
        except KeyError:
            pass
        
class GameUI(Gtk.Grid):
    def __init__(self, game):
        super(GameUI,self).__init__()
        self._game = game
        self._init_player_info()
        self._game.start_first_level()
        self._init_map()
        
    def _init_map(self):
        self.MAP_VIEW_SIZE_X = 30
        self.MAP_VIEW_SIZE_Y = 30
        map_info = self._game.get_map_info()
        self._map = Map(map_info)
        self.attach(self._map, top=1, left=1, width=self.MAP_VIEW_SIZE_X, height=self.MAP_VIEW_SIZE_Y)
    
    def _init_player_info(self):
        player_info = self._game.get_player_info()
        MAP_LEFT_END = 31
        self.attach(Gtk.Label("Archetype: "+Archetypes.to_string(player_info.archetype)), top=1, left=MAP_LEFT_END, width=1, height=1)
        
    def handle_key_press(self, widget, event):
        pass
        
class Map(Gtk.Grid): 
    def __init__(self, map_info):
        super(Map,self).__init__()
        self._tile_provider = TileProvider()
        for x in range(map_info.width_x):
            for y in range(map_info.width_y):
                map_cell = MapCell((x,y),map_info.cells[(x,y)], self._tile_provider)
                self.attach(map_cell, top=x, left=y, width=1, height=1 )
                
class MapCell(Gtk.EventBox):
    def __init__(self, position, cell_info, tile_provider):
        super(MapCell,self).__init__()
        self._position = position   
        if   cell_info.is_empty:
            self._image = Gtk.Image.new_from_pixbuf(tile_provider.get_tile("metal_floor"))
        elif isinstance(cell_info.things[0], WallInfo):
            self._image = Gtk.Image.new_from_pixbuf(tile_provider.get_tile("metal_wall"))
        elif isinstance(cell_info.things[0], PlayerInfo):
            self._image = Gtk.Image.new_from_pixbuf(tile_provider.get_tile("player"))     
        self.add(self._image)       
        
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), StyleProviders.MAIN_STYLE, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        super(MainWindow, self).__init__(title           ="Solar Winter",
                                         default_height  =800, 
                                         default_width   =800, 
                                         window_position =Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-release-event", self.handle_key_press)
        self._start_button        = StartButton(self)
        self._character_creator   = CharacterCreator(self)
        self.add(self._start_button)
        self.show_all()
        
    def open_character_creator(self):
        self.remove(self._start_button)
        self.add(self._character_creator)
        self.show_all()
        
    def start_game(self, player):
        self.remove(self._character_creator)
        self._game = Game(player)
        self._game_ui = GameUI(self._game)
        self.add(self._game_ui)
        self.show_all()
        
    def handle_key_press(self, widget, event):
        self.get_child().handle_key_press(widget, event)
