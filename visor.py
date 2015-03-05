#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

#######################################################
#This file contains the code for the source code viewer
#######################################################

import os
import os.path
#import sys
import gi
import carga
from gi.repository import Gtk
from gi.repository import GtkSource
from gi.repository import Pango
from gettext import gettext as _


class visor_codigo():

    def __init__(self, ventana, notebook):
        # create buffer
        lm = GtkSource.LanguageManager()
        lang = lm.get_language('c')
        self.buffer = GtkSource.Buffer()
        self.buffer.set_language(lang)
        view = GtkSource.View.new_with_buffer(self.buffer)
        self.ventana = ventana

        vbox = Gtk.VBox(0, True)
        # self.window.add(vbox)
        notebook.append_page(vbox, Gtk.Label(label=_("Código fuente")))
        tool1 = Gtk.Toolbar()
        tool1.show()

        iconw = Gtk.Image()
        iconw.set_from_stock(Gtk.STOCK_EXECUTE, 15)

        vbox.pack_start(tool1, False, False, False)
        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.IN)
        sw.add(view)
        vbox.pack_start(sw, True, True, False)

        vbox.show_all()
        # main loop
        dir_conf = os.path.expanduser('~') + "/.icaro/firmware/"
        self.cadena_user_c = dir_conf + "source/user.c"
        # COMENTADO POR MIGRACION
        # self.buf = self.open_file(self.buffer, self.cadena_user_c)
        iconw = Gtk.Image()
        iconw.set_from_stock(Gtk.STOCK_NEW, 15)
        # COMENTADO EN MIGRACION
        # tool_button = tool1.append_item(
        #    "recargar",
        #    "",
        #    "Private",
        #    iconw,
        #    self.recargar)

    def open_file(self, buffer, filename):
        # get the new language for the file mimetype
        #COMENTADO POR MIGRACION
        #manager = buffer.get_data('languages-manager')

        if os.path.isabs(filename):
            path = filename
        else:
            path = os.path.abspath(filename)

        language = manager.guess_language(filename)
        if language:
            buffer.set_highlight_syntax(True)
            buffer.set_language(language)
        else:
            print 'No language found for file "%s"' % filename
            buffer.set_highlight_syntax(False)

        # remove_all_marks(buffer)
        self.load_file(buffer, path)  # TODO: check return
        return buffer

    def load_file(self, buffer, path):
        buffer.begin_not_undoable_action()
        try:
            txt = open(path).read()
        except:
            return False
        buffer.set_text(txt)
        buffer.set_data('filename', path)
        buffer.end_not_undoable_action()
        buffer.set_modified(False)
        buffer.place_cursor(buffer.get_start_iter())
        return True

    def save_file(self, filename):
        """ save buffer to the current file """
        cadena = self.buf.props.text
        a = self.ventana.mensajes(
            1, "Las modificaciones echas en el editor no se mantendran, y seran eliminadas cuando se compile de vuelta desde icaro-bloques. ¿Desea continuar?")
        if a == True:
            file = open(filename, "w")
            file.writelines(cadena)
            file.close()

    def recargar(self, b):
        pass
        #MIGRACION
        #self.buf = self.open_file(self.buffer, self.cadena_user_c)

        # self.buf=self.open_file(arg[0],arg[1])
        #~ Gtk.main_quit()
        # self.window.hide()

    def compilar(self, arg):
        dir_conf = os.path.expanduser('~') + "/.icaro/firmware/"
        cadena = dir_conf + "source/user.c"
        #MIGRACION
        cadena2 = self.buf.props.text
        a = self.ventana.mensajes(
            1, "Las modificaciones echas en el editor no se mantendran, y seran eliminadas cuando se compile de vuelta desde icaro-bloques. ¿Desea continuar?")
        if a == True:
            file = open(cadena, "w")
            file.writelines(cadena2)
            file.close()
            i = carga.compilar_pic("main", self.ventana.cfg)
            if i == 0:
                self.ventana.mensajes(3, "la compilacion fue exitosa")
            else:
                self.ventana.mensajes(0, "hubo un error de compilacion")
