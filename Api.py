#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Api.py por:
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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import Funciones as FUNC

class Api(Gtk.TreeView):
    """TreeView para mostrar:
    Clases, Funciones, Constantes y Otros items del modulo"""
        
    __gsignals__ = {"objeto":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "info":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_property("enable-grid-lines", True)
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        
        self.objetos = {}
        self.modulo = None
        self.objeto = None
        
        self.modelo = TreeStoreModel()
        self.construir_columnas()
        
        self.connect("row-activated", self.activar, None)
        
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
        Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.TOUCH_MASK)
        self.connect("key-press-event", self.keypress)
        
        self.set_model(self.modelo)
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.selecciones, self.modelo)
        self.show_all()
    
    def keypress(self, widget, event):
        """Cuando se presiona una tecla."""
        
        tecla = event.get_keycode()[1]
        model, iter = self.treeselection.get_selected()
        path = self.modelo.get_path(iter)
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        else:
            pass
        return False
    
    def activar (self, treeview, path, view_column, user_param1):
        """Cuando se hace doble click en "Clases", "Funciones", etc . . ."""
        
        iter = treeview.modelo.get_iter(path)
        valor = treeview.modelo.get_value(iter, 1)
        objeto = None
        try:
            objeto = self.objetos[valor]
        except:
            pass
        if treeview.row_expanded(path):
            treeview.collapse_row(path)
        elif not treeview.row_expanded(path):
            treeview.expand_to_path(path)

    def selecciones(self, treeselection, modelo, path, is_selected, treestore):
        """Cuando se selecciona una clase, funcion, etc . . ."""
        
        iter = modelo.get_iter(path)
        modulo =  modelo.get_value(iter, 2)
        valor = modelo.get_value(iter, 1)
        objeto = None
        if not is_selected and modulo != self.modulo:
            self.modulo = modulo
            self.emit('info', self.modulo )
        try:
            objeto = self.objetos[valor]
        except:
            pass
        if objeto and objeto != self.objeto and not is_selected:
            self.objeto = objeto
            self.emit('objeto', self.objeto)
        return True
    
    def llenar(self, paquetes):
        """Llena el treeview con los datos de un modulo."""
        
        self.modelo.clear()
        
        icono = os.path.join(os.path.dirname(__file__), "Iconos", "ver.png")
        pixbufver = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(os.path.dirname(__file__), "Iconos", "clase.png")
        pixbufclase = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(os.path.dirname(__file__), "Iconos", "funcion.png")
        pixbuffunc = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(os.path.dirname(__file__), "Iconos", "constante.png")
        pixbufconst = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(os.path.dirname(__file__), "Iconos", "otros.png")
        pixbufotros = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
            
        iter = self.modelo.get_iter_first()
        for paq in paquetes:
            modulo, CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS = FUNC.get_info(paq)
            
            if not modulo or not CLASES:
                self.emit('objeto', None)
                self.emit('info', "El Objeto %s no se ha Podido Localizar."  % (paq))
                return
                
            iteractual = self.modelo.append(iter,[ pixbufver, paq, str(modulo), ""])
            iterclass = self.modelo.append(iteractual,[ pixbufclase, 'Clases', str(modulo), ""])
            iterfunc = self.modelo.append(iteractual,[ pixbuffunc, 'Funciones', str(modulo), ""])
            iterconst = self.modelo.append(iteractual,[ pixbufconst, 'Constantes', str(modulo), ""])
            iterotros = self.modelo.append(iteractual,[ pixbufotros, 'Otros', str(modulo), ""])
            
            for clase in CLASES:
                self.modelo.append(iterclass,[ pixbufclase, clase[0], str(modulo), ""])
                self.objetos[clase[0]] = clase[1]
            for funcion in FUNCIONES:
                self.modelo.append(iterfunc,[ pixbuffunc, funcion[0], str(modulo), ""])
                self.objetos[funcion[0]] = funcion[1]
            for const in CONSTANTES:
                self.modelo.append(iterconst,[ pixbufconst, const[0], str(modulo), ""])
                self.objetos[const[0]] = const[1]
            for otros in DESCONOCIDOS:
                self.modelo.append(iterotros,[ pixbufotros, otros, str(modulo), ""])
                self.objetos[otros[0]] = otros[1]
                
            self.emit('info', "El Objeto %s se ha Cargado Correctamente."  % (paq))
                
    def construir_columnas(self):
        celda_de_imagen = Gtk.CellRendererPixbuf()
        columna = Gtk.TreeViewColumn(None, celda_de_imagen, pixbuf=0)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Objeto', celda_de_texto, text=1)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)

        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Modulo', celda_de_texto, text=2)
        columna.set_property('resizable', True)
        columna.set_property('visible', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Reserva2', celda_de_texto, text=3)
        columna.set_property('resizable', True)
        columna.set_property('visible', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
class TreeStoreModel(Gtk.TreeStore):
    def __init__(self):
        Gtk.TreeStore.__init__(self, GdkPixbuf.Pixbuf,
        GObject.TYPE_STRING, GObject.TYPE_STRING,
        GObject.TYPE_STRING)
        