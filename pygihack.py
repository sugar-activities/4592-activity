#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   pygi-hack.py por:
#   Flavio Danesse <fdanesse@activitycentral.com>
#   CeibalJAM - Uruguay - Activity Central
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

from sugar3.activity import activity

from Navegador import Navegador

BASE = os.path.dirname(__file__)

def get_separador(draw = False, ancho = 0, expand = False):
    """ Devuelve un separador generico."""
    
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador

def get_boton(archivo, flip = False, color = Gdk.Color(65000, 65000, 65000)):
    """ Devuelve un toolbarbutton generico."""
    
    boton = Gtk.ToolButton()
    imagen = Gtk.Image()
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, 32, 32)
    if flip: pixbuf = pixbuf.flip(True)
    imagen.set_from_pixbuf(pixbuf)
    imagen.modify_bg(0, color)
    boton.set_icon_widget(imagen)
    imagen.show()
    boton.show()
    return boton

class pygihack(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.set_border_width(3)
        
        self.connect("delete_event", self.delete_event)
        self.connect("destroy", self.destroy)
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.toolbar = Toolbar()
        self.toolbartry = ToolbarTry()
        self.navegador = Navegador()
        vbox.pack_start(self.toolbar, False, True, 0)
        vbox.pack_start(self.navegador, True, True, 0)
        vbox.pack_start(self.toolbartry, False, True, 3)
        self.set_canvas(vbox)
        self.show_all()
        
        self.navegador.connect('info', self.get_info)
    
    def get_info(self, widget, objeto):
        self.toolbartry.label.set_text( str(objeto) )
        
    def delete_event(self, widget, event, data=None):
        return False
    
    def destroy(self, widget, data=None):
        Gtk.main_quit()

class ToolbarTry(Gtk.Toolbar):
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_size_request(5, -1)
        separator.set_expand(False)
        self.insert(separator, -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_size_request(0, -1)
        separator.set_expand(True)
        self.insert(separator, -1)
       
        imagen = Gtk.Image()
        archivo = os.path.join(BASE, 'Iconos', 'ActivityCentral.png')
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(archivo)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.show_all()

class Toolbar(Gtk.Toolbar):
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.insert(get_separador(draw = False, ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(BASE, "Iconos","ceibaljam.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 32)
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False, ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(BASE, "Iconos","uruguay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 32)
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False, ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(BASE, "Iconos","licencia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 32)
        imagen.set_from_pixbuf(pixbuf)
        imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False, ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("fdanesse@activitycentral.com")
        self.label.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False, ancho = 0, expand = True), -1)
        
        archivo = os.path.join(BASE, "Iconos","salir.png")
        boton = get_boton(archivo, flip = False, color = Gdk.Color(0, 0, 0))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False, ancho = 3, expand = False), -1)
        
        self.show_all()
        
    def salir(self, widget):
        sys.exit(0)
        