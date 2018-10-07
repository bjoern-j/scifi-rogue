'''
Created on 6 Oct 2018

@author: bjoern
'''
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from UI.MainWindow import MainWindow

if __name__ == '__main__':
    main_window = MainWindow()
    Gtk.main()