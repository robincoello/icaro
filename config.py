#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  config.py
#
#  Copyright 2012 valentin <valentin@localhost.localdomain>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import sys
#import re
from gi.repository import Gtk
#from gi.repository import GObject


class CONFIG:

    """ Class doc """

    def __init__(self):
        """ Class initialiser """
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.window.connect('delete_event', self.close_application)
        #~ self.window.set_default_size(750, 500)
        conf = open(sys.path[0] + "/config.dat", "r")
        datos = conf.readlines()
        tupla = []
        for val in datos:
            val = val.strip("\n")
            tupla.append(val)
        conf.close()
        vbox = Gtk.VBox(False, spacing=5)
        vbox.set_border_width(5)

        # boton examinar
        hboxsdcc = Gtk.HBox(True, 0)
        self.SdccBoton = Gtk.Button()
        self.SdccBoton.set_label("examinar")
        self.SdccBoton.connect('clicked', self.exam, "sdcc")
        # texto de configuracion para sdcc
        self.SdccText = Gtk.Entry()
        self.SdccLabel = Gtk.Label()
        self.SdccLabel.set_text("Binario sdcc")
        try:
            self.SdccText.set_text(tupla[0])
        except Exception, ex:
            self.SdccText.set_text("")

        # empaqueto todo
        hboxsdcc.pack_start(self.SdccLabel, False, False)
        hboxsdcc.pack_start(self.SdccText, False, False)
        hboxsdcc.pack_start(self.SdccBoton, False, False)
        vbox.pack_start(hboxsdcc, False, False)

        # tortucaro
        # boton examinar
        hboxTurtle = Gtk.HBox(True, 0)

        self.TurtleBoton = Gtk.Button()
        self.TurtleBoton.set_label("examinar")
        self.TurtleBoton.connect('clicked', self.exam, "turtle")
        # texto de configuracion para sdcc
        self.TurtleText = Gtk.Entry()
        self.TurtleLabel = Gtk.Label()
        self.TurtleLabel.set_text("Ruta TurtleArt")
        try:
            self.TurtleText.set_text(tupla[1])
        except Exception, ex:
            self.TurtleText.set_text("")
        # empaqueto todo
        hboxTurtle.pack_start(self.TurtleLabel, False, False)
        hboxTurtle.pack_start(self.TurtleText, False, False)
        hboxTurtle.pack_start(self.TurtleBoton, False, False)
        vbox.pack_start(hboxTurtle, False, False)

        # boton aplicar y salir
        # Aplicar
        hboxbotones = Gtk.HBox(False, 0)
        self.AplicarBoton = Gtk.Button()
        self.AplicarBoton.set_label("Aplicar")
        self.AplicarBoton.connect('clicked', self.aplicar)

        # Salir
        self.SalirBoton = Gtk.Button()
        self.SalirBoton.set_label("Salir")
        self.SalirBoton.connect('clicked', self.close)

        hboxbotones.pack_start(self.AplicarBoton, False, False)
        hboxbotones.pack_start(self.SalirBoton, False, False)
        vbox.pack_start(hboxbotones, False, False)

        self.window.add(vbox)

    def aplicar(self, arg):
        #~ Gtk.main_quit()
        conf = open(sys.path[0] + "/config.dat", "w")
        conf.write(self.SdccText.get_text() + "\n")
        conf.write(self.TurtleText.get_text() + "\n")
        conf.close()

    def close(self, arg):
        #~ Gtk.main_quit()
        self.window.hide()

    def close_application(self, widget, event, data=None):
        #~ Gtk.main_quit()
        self.window.hide()

    def show(self):
        self.window.show_all()

    def exam(self, arg, valor):
        dialog = Gtk.FileChooserDialog(
            "Open..",
            None,
            Gtk.FileChooserAction.OPEN,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN,
                Gtk.ResponseType.OK
            )
        )
        dialog.set_default_response(Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cadena = dialog.get_filename()
            if valor == "sdcc":
                self.SdccText.set_text(cadena)
            if valor == "turtle":
                self.TurtleText.set_text(cadena)
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
