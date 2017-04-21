#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Navegador.py por:
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

# http://www.roojs.org/index.php/projects/gnome/introspection-docs.html
# http://www.roojs.org/seed/gir-1.1-gtk-2.0/
# http://www.roojs.com/seed/gir-1.2-gtk-3.0/seed/
# https://github.com/roojs/gir-1.2-gtk-2.0
# https://github.com/roojs/gir-1.2-gtk-3.0
# https://github.com/roojs/gir-1.2-gtk-3.4

import os
import pydoc
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import WebKit

from Api import Api

BASE = os.path.dirname(__file__)
DATOS = os.path.join(os.environ["HOME"], "Datos-pygi-hack")
if not os.path.exists(DATOS):
    os.mkdir(DATOS)
    os.chmod(DATOS, 0755)
    
# http://www.roojs.org/seed/gir-1.1-gtk-2.0/
PaquetesObjetos1 = ['Atk', 'Avahi', 'Clutter', 'ClutterJson',
'DBusGLib', 'Epiphany', 'Everything', 'GConf',
'GIMarshallingTests' 'GIRepository', 'GLib', 'GObject',
'GSSDP', 'GUPnP', 'Gda', 'Gdaui', 'Gdk', 'GdkPixbuf',
'Gio', 'Gladeui', 'GnomeVFS', 'GooCanvas', 'Gsf', 'Gst',
'GstApp', 'GstAudio', 'GstBase', 'GstController',
'GstInterfaces', 'GstNet', 'GstRtp', 'GstTag', 'GstVideo',
'Gtk', 'GtkClutter', 'GtkSource', 'Midgard', 'Notify',
'PanelApplet', 'Pango', 'PangoCairo', 'PangoFT2',
'PangoXft', 'Peas', 'PeasUI', 'Polkit', 'Poppler',
'Soup', 'SoupGNOME', 'TelepathyGLib', 'Unique',
'Vte', 'WebKit']
PaquetesNoObjetos1 = ['AvahiCore', 'Babl', 'Cogl', 'DBus',
'GL', 'GMenu', 'GModule', 'GnomeKeyring', 'GstCheck',
'GstFft', 'GstNetbuffer', 'GstPbutils', 'GstRiff',
'GstRtsp', 'GstSdp', 'Gtop', 'JSCore', 'PangoX', 'cairo',
'fontconfig', 'freetype2', 'libbonobo', 'libc',
'libxml2', 'sqlite3', 'xfixes', 'xft', 'xlib', 'xrandr']

# http://www.roojs.com/seed/gir-1.2-gtk-3.0/seed/
PaquetesObjetos2 = [
'AccountsService', 'Atk', 'Cally', 'Champlain', 'Clutter',
'ClutterX11', 'DBusGLib', 'Dbusmenu', 'Dee', 'EvinceDocument',
'EvinceView', 'GConf', 'GIRepository', 'GLib', 'GObject',
'GWeather', 'Gdk', 'GdkPixbuf', 'GdkX11', 'Gio', 'Gkbd',
'GnomeBluetooth', 'Gtk', 'GtkChamplain', 'GtkClutter',
'GtkSource', 'Gucharmap', 'Json', 'MPID', 'Nautilus',
'Notify', 'Pango', 'PangoCairo', 'PangoFT2', 'PangoXft',
'Peas', 'PeasGtk', 'Polkit', 'PolkitAgent', 'Soup',
'SoupGNOME', 'TelepathyGLib', 'TelepathyLogger',
'UPowerGlib', 'Vte', 'WebKit']
PaquetesNoObjetos2 = [
'Cogl', 'DBus', 'GL', 'GMenu', 'GModule',
'JSCore', 'cairo', 'fontconfig', 'freetype2',
'libxml2', 'xfixes', 'xft', 'xlib', 'xrandr']

class Navegador(Gtk.HPaned):
    __gsignals__ = {"info":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    def __init__(self):
        Gtk.HPaned.__init__(self)
        self.api = None
        self.descriptor = None
        self.pack1(self.area_izquierda_del_panel(), resize=False, shrink=True)
        self.pack2(self.area_derecha_del_panel(), resize=True, shrink=True)
        self.show_all()

        self.api.connect('objeto', self.ver_objeto)
        self.api.connect('info', self.re_emit_info)
    
    def re_emit_info(self, widget, objeto):
        self.emit('info', objeto)
        
    def ver_objeto(self, widget, objeto):
        os.chdir(DATOS)
        try:
            if objeto:
                pydoc.writedoc(objeto)
                archivo = os.path.join(DATOS, '%s.html' % (objeto.__name__))
                self.descriptor.open(archivo)
            else:
                self.descriptor.open('')
        except:
            self.descriptor.open('')
        
    def area_izquierda_del_panel(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # gtk 2
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        frame = Gtk.Frame()
        frame.set_label("Objects")
        frame.set_label_align(0.5, 0.5)
        combo = Gtk.ComboBoxText()
        for item in PaquetesObjetos1:
            combo.append_text(item)
        combo.connect('changed', self.get_item)
        frame.add(combo)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("No Objects")
        frame.set_label_align(0.5, 0.5)
        combo2 = Gtk.ComboBoxText()
        for item in PaquetesNoObjetos1:
            combo2.append_text(item)
        combo2.connect('changed', self.get_item)
        frame.add(combo2)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("gir-1.1-gtk-2.0")
        frame.set_label_align(0.5, 0.5)
        frame.add(hbox)
        vbox.pack_start(frame, False, False, 0)
        
        # gtk 3
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        frame = Gtk.Frame()
        frame.set_label("Objects")
        frame.set_label_align(0.5, 0.5)
        combo = Gtk.ComboBoxText()
        for item in PaquetesObjetos2:
            combo.append_text(item)
        combo.connect('changed', self.get_item)
        frame.add(combo)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("No Objects")
        frame.set_label_align(0.5, 0.5)
        combo2 = Gtk.ComboBoxText()
        for item in PaquetesNoObjetos2:
            combo2.append_text(item)
        combo2.connect('changed', self.get_item)
        frame.add(combo2)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("gir-1.2-gtk-3.0")
        frame.set_label_align(0.5, 0.5)
        frame.add(hbox)
        vbox.pack_start(frame, False, False, 0)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        self.api = Api()
        scrolled_window.add_with_viewport (self.api)
        vbox.pack_start(scrolled_window, True, True, 0)
        
        combo.set_active(0)
        
        return vbox

    def area_derecha_del_panel(self):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        self.descriptor = WebKit.WebView()
        scrolled_window.add_with_viewport (self.descriptor)
        return scrolled_window
    
    def get_item(self, widget):
        self.api.llenar( [widget.get_active_text()] )
    