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
import os
import sys
import creditos
import carga
import abrir
import nuevo
import guardar
import crear
import navegador
import visor
import tooltips
import config
import graficador
import cairo

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from motor import MotorCairo
from componente_inicial import *
from componente import *
from gettext import gettext as _
import util

# ========================================================================
# COMPONENTES
# ========================================================================


class Componentes():

    """
    variables globales para los componentes, aca se guardan las listas de
    objetos que representan a los componentes. esas lista es la que se usa para
    poder parsear los bloques conectados a inicio y obtener el codigo fuente
    para cargar en user.c

    """
    identificador = 1
    identificador_dat = 1
    identificador_dat2 = 1
    objetos = []
    tipo_obj = [0]
    lista_ordenada = []
    lista_fina = []
    objetos_datos = []
    tipo_obj_datos = []
    lista_valor_datos = []
    lista_valor_datos2 = []

    def __init__(self):
        """ Class initialiser """
        pass

# ========================================================================
# FONDO
# ========================================================================


class fondo(MotorCairo, Componentes):

    """
    representa los valores globales del background de la aplicacion.
    la clase MOTOR (pycairo) toma los valores de la instancia fondo para
    determinar el color inicial de la pantalla icaro y el color del texto
    Se encarga de cargar una imagen de fondo o un color en el drawing area
    de la ventana
    """
    FONDO = (00, 22, 55)
    color_texto = (255, 255, 255)
    poscion_botones = 0
    band = 0

    def __init__(self):
        self.lista_ordenada.append(0)
        self.img = ""
        self.ultimo = 1

    def carga_img(self, cadena):
        """
        carga una imagen de fondo
        """
        # band es una bandera para determinar si se dibuja una imagen (band=1)
        # o no (band=0)
        self.band = 1
        # img representa el nombre y la ruta del archivo que contiene la imagen
        self.img = cadena

    def update(self):
        """
        funcion que es llamada por (ventana_principal.timeout) para actualizar
        el fondo de la imagen y evitar qeu los bloques dejen un rastro en la
        pantalla, o para actualizar la imagen de fondo
        """
        if self.band == 1:
            if os.path.exists(self.img):
                cr2 = ventana_principal.area.window.cairo_create()
                respuesta = self.imagen(self.img, 0, 0, cr2)
                if respuesta == 1:
                    self.band = 0

# ========================================================================
# FUNCIONES PARA COMPILAR Y CARGAR EL FIRMWARE
# ========================================================================


class tool_compilador:
    def __init__():
        pass

    def carga(self):
        '''
        cargo template.pde para tener la planilla estandar dentro de
        cadena_pinguino
        la idea es poder separar estas funciones de icaro.py y trabajarlo
        directamente desde otro archivo, asi es mas facil armar bloques
        personalizados
        '''
        self.cadena_pinguino[:] = []
        dir_conf = os.path.expanduser('~') + "/.icaro/firmware/"
        archivo = open(dir_conf + "/source/template.pde", "r")
        for linea in archivo:
            self.cadena_pinguino.append(linea)

    def compilar(self, b):
        pagina = self.notebook2.get_current_page()
        if pagina == 0:
            self.carga()
            crear.crear_archivo(self.fondo, self)
            dir_conf = os.path.expanduser('~') + "/.icaro/firmware"
            i = util.compilar("main", self.cfg, dir_conf)
            # i = carga.compilar_pic("main", self.cfg)
            if i == 1:
                self.mensajes(0, ("no se encuentra el compilador sdcc en" +
                                  " la ruta " + self.config[0] +
                                  " . Pruebe configurar el archivo" +
                                  " config.ini y corregirlo"))
            elif i == 0:
                self.mensajes(3, "la compilacion fue exitosa")
            else:
                self.mensajes(0, "hubo un error de compilacion")
        if pagina == 1:
            self.ver.compilar(0)

    def upload(self, b):
        # dir_conf = os.path.expanduser('~') + "/.icaro/firmware"
        i = util.linker("main", self.cfg)
        # i = carga.upload_pic("main", self.cfg)
        if i == 0:
            cargador = carga.Cargador("main")
            cargador.start()
            return 0

    def comp_esp(self, b, datos):
        comp = 1
        dir_conf = os.path.expanduser('~') + "/.icaro/firmware"
        i = util.compilar(datos, self.cfg, dir_conf)
        # i = carga.compilar_pic(datos, self.cfg)
        if i == 0:
            self.mensajes(3, "la compilacion fue exitosa")
            comp = 0
        else:
            self.mensajes(0, "hubo un error de compilacion")
            comp = 1
        if comp == 0:
            i = util.linker(datos, self.cfg)
            # i = carga.upload_pic(datos, self.cfg)
            if i == 0:
                cargador = carga.Cargador(datos)
                cargador.start()
                return 0
###############################################################################


class crear_comp:
    def __init__():
        pass

    def crear_componente(self, b, x, y):
        ay = 30
        ax = ay
        # siempre hay que tratar de que el foco quede en el drawing area
        self.area.grab_focus()

        if self.diccionario[b][1] == 1:
            c1 = componente(
                x,
                y,
                self.fondo.identificador + 1,
                self.diccionario[b][2],
                self.diccionario[b][3],
                self.diccionario[b][0],
                self.fondo,
                self
            )
            self.fondo.identificador += 1
            self.fondo.objetos.append(c1)
            self.fondo.tipo_obj.append(self.diccionario[b][1])
            self.fondo.lista_ordenada.append(0)
        if self.diccionario[b][1] == 4:

            self.fondo.identificador += 1
            c1 = componente_cero_arg(
                x,
                y,
                self.fondo.identificador,
                self.diccionario[b][3],
                self.diccionario[b][0],
                self.fondo,
                self
            )

            self.fondo.objetos.append(c1)
            self.fondo.tipo_obj.append(self.diccionario[b][1])
            self.fondo.lista_ordenada.append(0)

        if self.diccionario[b][1] == 5:
            self.fondo.identificador += 1
            c1 = componente_bloque_uno(
                x,
                y,
                self.fondo.identificador,
                self.diccionario[b][3],
                self.diccionario[b][0],
                self.fondo,
                self,
            )
            self.fondo.objetos.append(c1)
            self.fondo.identificador += 1
            self.fondo.lista_ordenada.append(0)

            c1 = componente_bloque_dos(
                x,
                y + 80,
                self.fondo.identificador,
                self.diccionario[b][3],
                self.diccionario[b][4],
                self.fondo,
                self
            )
            self.fondo.objetos.append(c1)
            self.fondo.tipo_obj.append(self.diccionario[b][1])
            self.fondo.tipo_obj.append(0)
            self.fondo.lista_ordenada.append(0)

        if self.diccionario[b][1] == 6:
            c1 = comp_dat_arg(
                x,
                y,
                self.fondo.identificador_dat,
                self.diccionario[b][2],
                self.diccionario[b][4],
                self.diccionario[b][3],
                self.diccionario[b][5],
                self.diccionario[b][0].strip(" ") + ".png",
                6,
                self.fondo,
                self,
            )
            self.fondo.identificador_dat += 1
            self.fondo.objetos_datos.append(c1)
            self.fondo.tipo_obj_datos.append(self.diccionario[b][1])
        if self.diccionario[b][1] == 7:
            c1 = comp_dat_arg(
                x,
                y,
                self.fondo.identificador_dat,
                self.diccionario[b][2],
                self.diccionario[b][4],
                self.diccionario[b][3],
                self.diccionario[b][5],
                self.diccionario[b][0].strip(" ") + ".png",
                7,
                self.fondo,
                self,
            )
            self.fondo.identificador_dat += 1
            self.fondo.objetos_datos.append(c1)
            self.fondo.tipo_obj_datos.append(self.diccionario[b][1])


# ========================================================================
# VENTANA
# ========================================================================


class Ventana:

    """
    Clase ventana contiene el constructor de la ventana GTK y las funciones
    basicas del sistema.
    diagrama de los widget anidados:

        ###############################################

             ventana
                |
                 ->box1
                   |
                    -> menu_bar
                   |
                    -> box2
                       |
                        -> scrolled_window3
                       |            |
                       |             -> toolbar
                       |
                        -> hp
                           |
                            -> self.notebook2
                           |         |
                           |          -> scrolled_window
                           |         |       |
                           |         |        -> area
                           |         |
                           |          -> visor
                           |
                            -> scrolled_window2
                                    |
                                     -> notebook


        ################################################
    esta clase controla todos los eventos del programa, mouse, teclado,
    interaccion entre los componentes. A su ves es la encargada d actualizar
    el estado de los bloques icaro y redibujar la pantalla mediante la funcion
    ventana_principal.timeout


    """
    # variables globales para manejar posicion del mouse, clicks y pulsaciones
    # de teclas dentro de la ventana
    archivo = ""
    mousexy = (0, 0)
    boton_mouse = [0, 0, 0, 0]
    seleccionado = 0
    seleccionado_datos = 0
    seleccionado_datos_ed = 0
    tecla = 0
    valor_tecla = ""
    tecla_enter = 0
    processor = "18f4550"
    cadena_pinguino = []
    seleccion_menu = 1
    tipo_componente = 1
    diccionario = {}
    tooltip = {}
    lista = []
    config = []
    edicion = 0
    z = 1
    cursores = [0]
    dicc_accesos_directos = {
        65470: "f1",
        65471: "f2",
        65472: "f3",
        65473: "f4",
        65474: "f5",
        65475: "f6",
        65476: "f7",
        65477: "f8",
        65478: "f9",
        65479: "f10",
        65480: "f11",
        65481: "f12",

    }
    valor_datos_comp = {"fin ": "}"}

    def __init__(self):

        # esta es la lista de donde se sacan los valores para los botones
        # icaro
        arch = open(sys.path[0] + "/version", "r")
        version = arch.readline()
        creditos.Info.version = version
        self.carga_dicc()
        self.tooltip = tooltips.dicc
        self.lista = self.diccionario.keys()
        self.lista.sort()
        self.carga_paleta()
        conf_ini = os.path.expanduser('~') + "/.icaro/conf/config.ini"
        if os.path.exists(conf_ini):
            self.cfg = util.carga_conf(conf_ini)
        else:
            self.recarga_conf(False)
        # configuraciones generales de ICARO (guardadas en config.ini)
        self.z = float(self.cfg.get("icaro_config", "zoom"))
        # declaro la ventana principal
        # esta es la toolbar donde van los botones para cargar los datos
        # y compilar
        # declaro la tabla  donde van los botones para el menu de bloques
        # box1 es el contenedor principal despues de la ventana
        self.window1 = Gtk.Window()
        toolbar = Gtk.Toolbar()
        toolbar.set_show_arrow(False)
        self.area = Gtk.DrawingArea()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window2 = Gtk.ScrolledWindow()
        scrolled_window3 = Gtk.ScrolledWindow()
        table = Gtk.VBox(False, len(self.lista))
        notebook = Gtk.Notebook()
        self.notebook2 = Gtk.Notebook()
        hp = Gtk.HPaned()
        box2 = Gtk.HBox(False, 3)
        box1 = Gtk.VBox(False, 3)
        menu_bar = Gtk.MenuBar()

        # empaqueto todo
        # esta es la idea de usar un hpaned para poder achicar la pantalla
        # en las netbook no entra todo
        self.window1.add(box1)
        box1.pack_start(menu_bar, False, True, 1)
        box1.pack_start(box2, True, True, 1)
        scrolled_window.add_with_viewport(self.area)
        scrolled_window3.add_with_viewport(toolbar)
        scrolled_window2.add_with_viewport(notebook)

        self.notebook2.append_page(scrolled_window,
                                   Gtk.Label(label=_("Bloques")))
        box2.pack_start(scrolled_window3, False, False, 1)
        box2.pack_start(hp, True, True, 1)
        hp.pack1(self.notebook2, True, True)
        hp.pack2(scrolled_window2, True, True)
        # Add source code viewer tab
        self.ver = visor.visor_codigo(self, self.notebook2)

        hp.set_position(500)
        self.window1.connect('delete-event', Gtk.main_quit)
        self.window1.set_icon_from_file(
            sys.path[0] +
            "/imagenes/icaro.png"
        )
        self.area.set_app_paintable(True)
        self.area.set_size_request(800, 1800)
        menu1 = [_("File"), _("Edit"), _("Tools")]
        menu_general = [
            (_("New"), _("Open"), _("Save"), _("Save as"),
             _("Save as function"), _("Examples"), _("Exit")),
            (_("Background"), _("Color"), _("About"), _("Config")),
            (_("Graphic"), _("Calc"), _("Log"), _("Firmware"))
        ]
        menu_bar.show()
        # declaro los botones del menu 'menu'5 y 'edicion'
        for a in range(len(menu_general)):
            menu = Gtk.Menu()
        # buf es donde se cargan todos los botones del menu
            for i in menu_general[a]:
                menu_items = Gtk.MenuItem(i)
                menu.append(menu_items)
                menu_items.connect("activate", self.menuitem_response, i)
                menu_items.show()
            root_menu = Gtk.MenuItem(menu1[a])
            root_menu.show()
            root_menu.set_submenu(menu)
            menu_bar.append(root_menu)

        # toolbar.append_item
        toolbar.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)
        toolbar.set_orientation(Gtk.Orientation.VERTICAL)
        toolbar.show()

        # creo los botones de la toolbar
        botones_toolbar = [
            [1, toolbar, Gtk.STOCK_NEW, "New",
             self.tooltip["nuevo"], self.nuevo, None],
            [1, toolbar, Gtk.STOCK_OPEN, "Open",
             self.tooltip["abrir"], self.abrir, None],
            [1, toolbar, Gtk.STOCK_SAVE, "Save",
             self.tooltip["guardar"], self.guardar, None],
            [1, toolbar, Gtk.STOCK_QUIT, "Quit",
             self.tooltip["salir"], self.salir, None],
            [3],
            [2, toolbar, sys.path[0] + "/imagenes/icaro.png",
             "Compile", self.tooltip["compilar"], self.compilar, None],
            [2, toolbar, sys.path[0] + "/imagenes/compilar.png",
             "Load", self.tooltip["cargar"], self.upload, None],
            [2, toolbar, sys.path[0] + "/imagenes/tortucaro.png",
             "Tortucaro", self.tooltip["tortucaro"],
             self.comp_esp, "tortucaro/tortucaro"],
            [2, toolbar, sys.path[0] + "/imagenes/pilas.png",
             "Pilas", self.tooltip["tortucaro"],
             self.comp_esp, "pilas/pilas-engine"],
            [3],
            [1, toolbar, Gtk.STOCK_HELP, "Help",
             self.tooltip["ayuda"], self.ayuda, None],
            [3],
            [1, toolbar, Gtk.STOCK_ADD, "Pen",
             self.tooltip["lapiz"], self.dibujo, 1],
            [1, toolbar, Gtk.STOCK_SELECT_COLOR, "Move",
             self.tooltip["mover"], self.dibujo, 2],
            [1, toolbar, Gtk.STOCK_DELETE, "Erase",
             self.tooltip["borrar"], self.dibujo, 3],
            [1, toolbar, Gtk.STOCK_EDIT,
             "Edit", "", self.dibujo, 4],
            [3],
            [1, toolbar, Gtk.STOCK_ZOOM_IN, "Agrandar",
             "", self.menuitem_response, "zoomas"],
            [1, toolbar, Gtk.STOCK_ZOOM_OUT, "Achicar",
             "", self.menuitem_response, "zoomenos"],
            [1, toolbar, Gtk.STOCK_ZOOM_100, "Zoom 1:1",
             "", self.menuitem_response, "zoomcero"],
            ]

        # creo los botones de la toolbar en funcion de la tupla botonas_toolbar
        for dat in botones_toolbar:
            if dat[0] == 3:
                sep = Gtk.SeparatorToolItem.new()
                toolbar.insert(sep, -1)
            if dat[0] == 1 or dat[0] == 2:
                self.crear_toolbuttons(
                    dat[0], dat[1], dat[2], dat[3], dat[4], dat[5], dat[6])

        scrolled_window.set_size_request(300, 300)
        scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
        scrolled_window.show()
        scrolled_window2.set_border_width(1)
        scrolled_window2.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        scrolled_window2.show()
        scrolled_window3.set_border_width(1)
        scrolled_window3.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
        scrolled_window3.show()
        notebook.set_tab_pos(Gtk.PositionType.RIGHT)
        label = Gtk.Label(label=self.diccionario[self.lista[0]][1])
        notebook.append_page(table, label)
        buffer = self.diccionario[self.lista[1]][0]
        caja = self.imagen_boton(
            self.diccionario[self.lista[1]][0],
            self.diccionario[self.lista[1]][0]
        )
        button = Gtk.RadioButton()
        if self.tooltip.has_key(self.diccionario[self.lista[1]][0]):
            val = self.tooltip[self.diccionario[self.lista[1]][0]]
            button.set_tooltip_text(val)
        # bucle principal donde se cargan los RAdioButton donde se cargan
        # los componentes del diccionario
        button.add(caja)
        button.connect("clicked", self.botones, self.lista[1])  # buffer
        button.show()
        table.pack_start(button, False, True, 0)
        for i in range(2, len(self.lista)):
            if self.diccionario[self.lista[i]][0] == "notebook":
                table = Gtk.VBox(False, len(self.lista))
                label = Gtk.Label(label=self.diccionario[self.lista[i]][1])
                notebook.append_page(table, label)
            else:
                buffer = self.diccionario[self.lista[i]][0]
                caja = self.imagen_boton(
                    self.diccionario[self.lista[i]][0],
                    self.diccionario[self.lista[i]][0]
                )
                button = Gtk.RadioButton.new_from_widget(button)
                if self.tooltip.has_key(
                    self.diccionario[self.lista[i]][0]
                ):
                    tool = self.tooltip[
                        self.diccionario[self.lista[i]][0]
                    ]
                    button.set_tooltip_text(tool)
                button.add(caja)
                button.connect("clicked", self.botones, self.lista[i])
                table.pack_start(button, False, True, 0)
                button.show()

        # capturo los eventos del drawing area
        # menos el teclado que lo capturo desde la ventana principal
        self.area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.area.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.area.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.window1.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.window1.add_events(Gdk.EventMask.KEY_RELEASE_MASK)
        self.area.connect("button-press-event", self.buttonpress_cb)
        self.area.connect("button-release-event", self.buttonrelease_cb)
        self.area.connect("motion-notify-event", self.move_cb)
        self.area.connect("draw", self.expose)
        self.window1.connect("key_press_event", self.keypress_cb)
        self.window1.connect("key_release_event", self.keyrelease_cb)
        self.area.realize()
        display = self.area.get_window().get_display()
        pixbuf = cairo.ImageSurface.create_from_png(
            os.path.abspath(os.path.dirname(__file__)) + "/imagenes/mouse/lapiz.png")
        lapiz = Gdk.Cursor.new_from_surface(display, pixbuf, 6, 18)
        self.cursores.append(lapiz)
        pixbuf = cairo.ImageSurface.create_from_png(
            os.path.abspath(os.path.dirname(__file__)) + "/imagenes/mouse/puntero.png")
        puntero = Gdk.Cursor.new_from_surface(display, pixbuf, 6, 18)
        self.cursores.append(puntero)
        pixbuf = cairo.ImageSurface.create_from_png(
            os.path.abspath(os.path.dirname(__file__)) + "/imagenes/mouse/borrar.png")
        borrar = Gdk.Cursor.new_from_surface(display, pixbuf, 6, 18)
        self.cursores.append(borrar)
        pixbuf = cairo.ImageSurface.create_from_png(
            os.path.abspath(os.path.dirname(__file__)) + "/imagenes/mouse/edicion.png")
        edicion = Gdk.Cursor.new_from_surface(display, pixbuf, 6, 18)
        self.cursores.append(edicion)
        self.definir_cursor(1)

    def crear_toolbuttons(self, tipo, toolbar, img, nombre, tooltip, func, metodos):
        '''
        Crear los botones de la toolbar
        '''
        if tipo == 1:
            iconw = Gtk.Image()
            iconw.set_from_stock(img, 30)

        if tipo == 2:
            iconw = Gtk.Image()
            iconw.set_from_file(img)

        tool_icon = Gtk.ToolButton.new(iconw, _(nombre))
        if metodos is not None:
            tool_icon.connect('clicked', func, metodos)
        else:
            tool_icon.connect('clicked', func)
        tool_button = toolbar.insert(tool_icon, -1)

    def definir_cursor(self, b):
        self.area.get_window().set_cursor(self.cursores[b])

# ========================================================================
# ABRIR LA VENTANA DE VISOR DE CODIGO
# ========================================================================

    def graf(self):
        graf = graficador.VENTANA()
        graf.window.show_all()
# ========================================================================
# VENTANA DE AYUDA (NAVEGADOR)
# ========================================================================

    def ayuda(self, b):
        self.visor('http://roboticaro.org/documentacion/index.html')

    def dibujo(self, event, b):
        self.seleccion_menu = b
        self.definir_cursor(b)

# ========================================================================
# ESTO ES PARA GREGAR IMAGENES AL BOTON DE LA TOOLBAR
# ========================================================================
    def imagen_boton(self, xpm_filename, label_text):
        box1 = Gtk.HBox(False, 0)
        box1.set_border_width(0)
        image = Gtk.Image()
        xpm_filename = xpm_filename.strip(" ")
        buf = sys.path[0] + "/imagenes/componentes/" + xpm_filename + ".png"
        image.set_from_file(buf)
        label = Gtk.Label(label=label_text)
        box1.pack_start(image, False, True, 1)
        box1.pack_start(label, False, True, 1)
        image.show()
        label.show()
        return box1

# ========================================================================
# GENERADOR DE MENSAJES
# ========================================================================

    def mensajes(self, num, mensa):

        tipo = (
            Gtk.MessageType.WARNING,
            Gtk.MessageType.QUESTION,
            Gtk.MessageType.ERROR,
            Gtk.MessageType.INFO
            )
        botones = (
            Gtk.ButtonsType.OK,
            Gtk.ButtonsType.OK_CANCEL,
            Gtk.ButtonsType.OK,
            Gtk.ButtonsType.CANCEL
            )
        md = Gtk.MessageDialog(
            None,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            tipo[num],
            botones[num],
            mensa
            )
        resp = md.run()
        md.destroy()
        if resp == Gtk.ResponseType.OK:
            return True
        elif resp == Gtk.ResponseType.CANCEL:
            return False

    def botones(self, event, b):
        '''
        Esta funcion captura el evento de presionar un boton de la toolbar
        table y lo manda tipo_componentes
        '''
        self.tipo_componente = b
        self.seleccion_menu = 1
        self.definir_cursor(1)

        return True

# ========================================================================
# FUNCIONES PARA COMPILAR Y CARGAR EL FIRMWARE
# ========================================================================
    def carga(self):
        '''
        Cargar template.pde para tener la planilla estandar dentro de
        cadena_pinguino
        '''
        self.cadena_pinguino[:] = []
        dir_conf = os.path.expanduser('~') + "/.icaro/firmware/"
        archivo = open(dir_conf + "/source/template.pde", "r")
        for linea in archivo:
            self.cadena_pinguino.append(linea)

    def compilar(self, b):
        pagina = self.notebook2.get_current_page()
        if pagina == 0:
            self.carga()
            crear.crear_archivo(self.fondo, self)
            i = carga.compilar_pic("main", self.cfg)
            if i == 1:
                self.mensajes(0, ("no se encuentra el compilador sdcc en" +
                                  " la ruta " + self.config[0] +
                                  " . Pruebe configurar el archivo" +
                                  " config.dat y corregirlo"))
            if i == 0:
                self.mensajes(3, "la compilacion fue exitosa")
            else:
                self.mensajes(0, "hubo un error de compilacion")
        if pagina == 1:
            self.ver.compilar(0)

    def upload(self, b):
        i = carga.upload_pic("main", self.cfg)
        if i == 0:
            cargador = carga.Cargador("main")
            cargador.start()
            return 0

        # if i==1:
            #self.mensajes(0,"no se a detectado ningun dispositivo conectada. ¿esta conectado y encendido el PIC?")
            # return 1
        # if i==2:
            #self.mensajes(0,"Se detecto el dispositivo, pero no se puede cargar el firmware, hay que cargar el firmware antes de que se prenda el led rojo del dispositivo")
            # return 2
        # if i==2:
            #self.mensajes(0,"no se genero el archivo .hex para cargar")
            # return 3
        # if i==2:
            #self.mensajes(0,"error al compilar y generar el archivo .hex")
            # return 4
    def comp_esp(self, b, datos):
        comp = 1
        i = carga.compilar_pic(datos, self.cfg)
        if i == 0:
            self.mensajes(3, "la compilacion fue exitosa")
            comp = 0
        else:
            self.mensajes(0, "hubo un error de compilacion")
            comp = 1
        if comp == 0:
            i = carga.upload_pic(datos, self.cfg)
            if i == 0:
                cargador = carga.Cargador(datos)
                cargador.start()
                return 0

    def crear_componente(self, b, x, y):
        ax = ay = 30
        # siempre hay que tratar de que el foco quede en el drawing area
        self.area.grab_focus()

        if self.diccionario[b][1] == 1:
            c1 = componente(
                x - ax,
                y - ay,
                self.fondo.identificador + 1,
                self.diccionario[b][2],
                self.diccionario[b][3],
                self.diccionario[b][0],
                self.fondo,
                self
            )
            self.fondo.identificador += 1
            self.fondo.objetos.append(c1)
            self.fondo.tipo_obj.append(self.diccionario[b][1])
            self.fondo.lista_ordenada.append(0)
        if self.diccionario[b][1] == 4:

            self.fondo.identificador += 1
            c1 = componente_cero_arg(
                x - ax,
                y - ay,
                self.fondo.identificador,
                self.diccionario[b][3],
                self.diccionario[b][0],
                self.fondo,
                self
            )

            self.fondo.objetos.append(c1)
            self.fondo.tipo_obj.append(self.diccionario[b][1])
            self.fondo.lista_ordenada.append(0)

        if self.diccionario[b][1] == 5:
            self.fondo.identificador += 1
            c1 = componente_bloque_uno(
                                            x - ax,
                                            y - ay,
                                            self.fondo.identificador,
                                            self.diccionario[b][3],
                                            self.diccionario[b][0],
                                            self.fondo,
                                            self,
                                            )
            self.fondo.objetos.append(c1)
            self.fondo.identificador += 1
            self.fondo.lista_ordenada.append(0)

            c1 = componente_bloque_dos(
                                        x - ax,
                                        y + 80 - ay,
                                        self.fondo.identificador,
                                        self.diccionario[b][3],
                                        self.diccionario[b][4],
                                        self.fondo,
                                        self
                                        )
            self.fondo.objetos.append(c1)
            self.fondo.tipo_obj.append(self.diccionario[b][1])
            self.fondo.tipo_obj.append(0)
            self.fondo.lista_ordenada.append(0)

        if self.diccionario[b][1] == 6:
            c1 = comp_dat_arg(
                            x - ax,
                            y - ay + 15,
                            self.fondo.identificador_dat,
                            self.diccionario[b][2],
                            self.diccionario[b][4],
                            self.diccionario[b][3],
                            self.diccionario[b][5],
                            self.diccionario[b][0].strip(" ") + ".png",
                            6,
                            self.fondo,
                            self,
                            )
            self.fondo.identificador_dat += 1
            self.fondo.objetos_datos.append(c1)
            self.fondo.tipo_obj_datos.append(self.diccionario[b][1])
        if self.diccionario[b][1] == 7:
            c1 = comp_dat_arg(
                            x,
                            y - ay + 15,
                            self.fondo.identificador_dat,
                            self.diccionario[b][2],
                            self.diccionario[b][4],
                            self.diccionario[b][3],
                            self.diccionario[b][5],
                            self.diccionario[b][0].strip(" ") + ".png",
                            7,
                            self.fondo,
                            self,
                            )
            self.fondo.identificador_dat += 1
            self.fondo.objetos_datos.append(c1)
            self.fondo.tipo_obj_datos.append(self.diccionario[b][1])

    def guardar(self, dato):
        pagina = self.notebook2.get_current_page()
        dialog = Gtk.FileChooserDialog("save..",
                                        None,
                                        Gtk.FileChooserAction.SAVE,
                                            (
                                            Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE,
                                            Gtk.ResponseType.OK
                                            )
                                        )
        dialog.set_default_response(Gtk.ResponseType.OK)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cadena = dialog.get_filename()
            # separo la cadena para sacar la extension del archivo
            # si el tamaño de cadena2 es 1, el nombre del archivo no
            # tiene extension, entonces le agrego  - .icr -
            cadena2 = cadena.split(".")
            if len(cadena2) == 1:
                cadena = cadena + ".icr"
            if os.path.isfile(cadena):
                resp = self.mensajes(
                            1,
                            "Ya existe un archivo con el nombre " +
                            cadena + "¿Quiere reemplazarlo?"
                                    )
            else:
                resp = False
            if resp == True or os.path.isfile(cadena) == False:
                if pagina == 0:
                    guardar.guardar(
                                    self.fondo.objetos,
                                    cadena,
                                    self.fondo
                                    )
                    self.archivo = cadena
                if pagina == 1:
                    self.ver.save_file(cadena)
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def abrir(self, dato):
        pagina = self.notebook2.get_current_page()
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
        try:
            dialog.set_current_folder(dato)
        except Exception, ex:
            dialog.set_current_folder(sys.path[0])

        if pagina == 0:
            filter = Gtk.FileFilter()
            filter.set_name("icaro")
            filter.add_pattern("*.icr")
            dialog.add_filter(filter)
        if pagina == 1:
            filter = Gtk.FileFilter()
            filter.set_name("C")
            filter.add_pattern("*.c")
            dialog.add_filter(filter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if pagina == 0:
                nuevo.nuevo(self.fondo)
                inicial = componente_inicial(
                                            20, 50, 1,
                                            self.fondo,
                                            self
                                            )

                self.fondo.objetos.append(inicial)
                cadena = dialog.get_filename()
                self.update()
                abrir.abrir(
                            self.diccionario,
                            cadena,
                            self.fondo,
                            self
                            )
                self.archivo = cadena
            if pagina == 1:
                cadena = dialog.get_filename()

                self.ver.open_file(self.ver.buffer, cadena)

        elif response == Gtk.ResponseType.CANCEL:
            print 'Closed, no files selected'
        dialog.destroy()

    def nuevo(self, dato):
        self.archivo = ""
        nuevo.nuevo(self.fondo)
        self.fondo.band = 0
        R = self.cfg.get("icaro_config", "colorR")
        G = self.cfg.get("icaro_config", "colorG")
        B = self.cfg.get("icaro_config", "colorB")
        self.fondo.FONDO = (int(R), int(G), int(B))
        self.fondo.ultimo = 1
        inicial = componente_inicial(
                                    20,
                                    50,
                                    1,
                                    self.fondo,
                                    self
                                    )
        self.fondo.objetos.append(inicial)
# ========================================================================
# FUNCIONES DE LOS EVENTOS DEL MOUSE Y TECLADO
# ========================================================================

    def timeout(self):
        # self.area.queue_draw_area(0,0,int(self.mousexy[0]),int(self.mousexy[1]))
        self.area.queue_draw()
        # self.area.queue_clear()
        return True

    def update(self, ff):
        '''
        ff es un Cairo Context
        '''
        rgb = fon.color(fon.FONDO)
        ff.set_source_rgb(rgb[0], rgb[1], rgb[2])
        ff.paint()
        self.cr = ff
        self.fondo.zoom(self.z, self.cr)
        self.fondo.update()
        if fon.objetos_datos > 0:
            for dat in fon.objetos_datos:
                dat.update()
        for obj in fon.objetos:
            obj.update()
        return True

    def expose(self, event, b):
        self.update(b)

    def move_cb(self, win, event):
        mouse = event.get_coords()
        self.mousexy = (mouse[0] / self.z, mouse[1] / self.z)

    def buttonpress_cb(self, win, event):
        '''
        Cada vez que el cursor hace click sobre el Drawarea
        '''
        self.boton_mouse[event.button] = 1
        # aca llamo a update porque si no, me tira un error en tiempo
        # de ejecucion
        cairo_context = win.get_window().cairo_create()
        self.update(cairo_context)
        self.boton_mouse[event.button] = 1
        if event.button == 3:
            self.boton_mouse[event.button] = 0
            self.menu(event)
            return
        if self.seleccion_menu == 1:
            self.crear_componente(
                self.tipo_componente, self.mousexy[0], self.mousexy[1])

    def buttonrelease_cb(self, win, event):
        self.boton_mouse[event.button] = 0

    def menu(self, event):
        menu = Gtk.Menu()
        dibujar = Gtk.MenuItem(_("Pen"))
        mover = Gtk.MenuItem(_("Move"))
        editar = Gtk.MenuItem(_("Edit"))
        eliminar = Gtk.MenuItem(_("Erase"))
        # Agregar los items al menu
        menu.append(dibujar)
        menu.append(mover)
        menu.append(editar)
        menu.append(eliminar)
        # Se conectan las funciones de retrollamada a la senal "activate"
        dibujar.connect_object("activate", self.MenuRespuesta, 1)
        mover.connect_object("activate", self.MenuRespuesta, 2)
        eliminar.connect_object("activate", self.MenuRespuesta, 3)
        editar.connect_object("activate", self.MenuRespuesta, 4)
        menu.show_all()
        menu.popup(None, None, None, event.button, event.time)

    def MenuRespuesta(self, b):
        self.seleccion_menu = b
        self.definir_cursor(b)

    def keypress_cb(self, win, event):
        self.tecla = 1
        self.valor_tecla = event.string
        if event.keyval == 65293:
            self.tecla_enter = 1
        if self.dicc_accesos_directos.has_key(event.keyval):
            self.AccesosDirectos(self.dicc_accesos_directos[event.keyval])

    def AccesosDirectos(self, evento):
        if evento == "f1":
            self.MenuRespuesta(1)
        if evento == "f2":
            self.MenuRespuesta(2)
        if evento == "f3":
            self.MenuRespuesta(3)
        if evento == "f4":
            self.MenuRespuesta(4)
        if evento == "f5":
            print "creo archivo"

    def keyrelease_cb(self, win, event):
        self.tecla = 0
        self.tecla_enter = 0
        self.valor_tecla = ""

    def salir(self, dato):
        cartel = self.mensajes(1, "¿esta seguro que desea salir del sistema?")
        if cartel == 1:
            exit()

# ========================================================================
# LAS RESPUESTAS DEL MENU
# ========================================================================
    def menuitem_response(self, widget, string):
        if string == _("Open"):
            # tengo que madar un -dato- para mantener compatibilidad con
            # los botones de la barra de herramienta que generan un dato
            # -b- que envian a la funcion.
            self.abrir(sys.path[0])
        if string == _("Exit"):
            self.salir(0)
        if string == _("New"):
            self.nuevo(0)
        if string == _("Save"):
            self.guardar(0)
        if string == _("Save as function"):
            dialog = Gtk.FileChooserDialog("save..",
                                           None,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE,
                                            Gtk.ResponseType.OK))
            dialog.set_default_response(Gtk.ResponseType.OK)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                crear.funcion(self.fondo, self, dialog.get_filename(),)
            elif response == Gtk.ResponseType.CANCEL:
                # print 'Closed, no files selected'
                dialog.destroy()
        if string == _("Examples"):
            self.abrir(sys.path[0] + "/ejemplos")
        if string == _("Background"):
            dialog = Gtk.FileChooserDialog("Open..",
                                           None,
                                           Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN,
                                            Gtk.ResponseType.OK))
            dialog.set_default_response(Gtk.ResponseType.OK)
            response = dialog.run()
            cadena = dialog.get_filename()
            if response == Gtk.ResponseType.OK:
                # ~ #print "imagen", cadena
                try:
                    self.fondo.carga_img(cadena)
                except Exception, ex:
                    self.mensajes(2, "archivo no valido")

            elif response == Gtk.ResponseType.CANCEL:
                # print 'Closed, no files selected'
                dialog.destroy()
        if string == _("Color"):

            colorseldlg = Gtk.ColorChooserDialog.new("selección de color", None)
            colorseldlg.show()
            # colorsel = colorseldlg.colorsel
            # response = colorseldlg.run()
            #if response - - Gtk.ResponseType.OK:
                ##color = colorsel.get_current_color()
                #color = colorseldlg.get_color_selection()
                ## color devuelve un Gdk.color
                ## pero el RGB es un integer de 65535 valores
                ## con una regla de tres simple lo adapto a los
                ## 255 valores que soporta pygame
                #self.fondo.FONDO = (
                            #(color.red * 255) / 65535,
                            #(color.green * 255) / 65535,
                            #(color.blue * 255) / 65535
                            #)
            #else:
                #colorseldlg.hide()

            #colorseldlg.hide()
        if string == _("About"):

            about = Gtk.AboutDialog()
            logo = GdkPixbuf.Pixbuf.new_from_file(
                sys.path[0] + "/imagenes/icaro.png")
            about.set_logo(logo)
            about.set_name(creditos.Info.name)
            about.set_authors(creditos.Info.authors)
            about.set_documenters(creditos.Info.documenters)
            about.set_artists(creditos.Info.artists)
            about.set_translator_credits(creditos.Info.translator)
            about.set_version(creditos.Info.version)
            about.set_comments(creditos.Info.description)
            about.set_copyright(creditos.Info.copyright)
            about.set_website(creditos.Info.website)
            about.set_license(creditos.Info.license)
            about.set_wrap_license(True)
            about.run()
            about.destroy()
        if string == _("Config"):
            # print " menu de congifuracion"
            conf = config.CONFIG()
            conf.show()
        if string == _("Log"):
            dir_conf = os.path.expanduser(
                '~') + "/.icaro/firmware/temporal/log.dat"
            self.visor(dir_conf)
        if string == "graficador":
            self.graf()
        if string == "zoomas":
            self.z = self.z + 0.1
        if string == "zoomenos":
            self.z = self.z - 0.1
        if string == "zoomcero":
            self.z = 1
        if string == "firmware":
            self.recarga_conf(True)

    def recarga_conf(self, visual):
        dir_firm = os.path.expanduser('~') + "/.icaro/firmware/"
        dir_conf = os.path.expanduser('~') + "/.icaro/conf/"
        np05 = "/usr/share/icaro/pic16/np05"
        conf = "/usr/share/icaro/pic16/conf"
        if visual is True:
            resp = self.mensajes(1, "se volvera a la versión por defecto del firmware y la configuracion general, desea continuar")
        else:
            resp = True
        if resp is True:
            try:
                os.system("rm -rf " + dir_conf)
                os.system("cp -R " + np05 + " " + dir_firm)
                os.system("cp -R " + conf + " " + dir_conf)
                if visual is True:
                    self.mensajes(3, "se actualizo el firmware y la conf general")
                else:
                    print "se actualizo el firmware y la configuración general"
            except:
                if visual is True:
                    self.mensajes(0, "no se pudo actualizar el firmware")
                else:
                    print "hubo un error copiando el firmware y la configuración general"

    def visor(self, dir):
        browser = navegador.SimpleBrowser()
        browser.open(dir)
        browser.show()

    def carga_dicc(self):
        """
        funcion para cargar los componentes bloques,
        los valores del Gtk.notebook estan determinados
        por el nombre del archivo, leyendo el archivo saco el valor
        y tipo de los bloques que cargo en el dic
        """
        import carga_componentes
        q = 0

        carga = carga_componentes.DICC()
        comp, grupo = carga.buscar_bloques()
        for a in range(len(grupo)):
            self.diccionario[q] = ["notebook", grupo[a]]
            q += 1
            for cmp in comp[a]:

                tupla = []
                tupla.append(cmp.dicc["nombre"])
                tupla.append(cmp.dicc["componente"])
                tupla.append(cmp.dicc["cant_puertos"])
                tupla.append(cmp.dicc["color"])
                tupla.append(str(cmp.dicc["dato"]))
                tupla.append(str(cmp.dicc["dato2"]))
                self.valor_datos_comp[cmp.dicc["nombre"]] = cmp.valor
                self.diccionario[q] = tupla
                q += 1

    def carga_paleta(self):
        R = G = B = ""
        archivo = open(
            os.path.abspath(os.path.dirname(__file__)) + "/colores.dat", "r")
        tupla = []
        cadena = archivo.readlines()
        for n in cadena:
            tupla.append(n.strip("()\n"))
        for a in range(len(self.lista)):
            if self.diccionario[self.lista[a]][0] <> "notebook":
                R, G, B = tupla[a].split(",")
                self.diccionario[self.lista[a]][3] = (
                                                   int(R),
                                                   int(G),
                                                   int(B)
                                                   )


# Inicio todas las clases
ventana_principal = Ventana()
fon = fondo()
ventana_principal.fondo = fon
inicial = componente_inicial(20, 50, 1, fon, ventana_principal)
fon.objetos.append(inicial)
ventana_principal.window1.show_all()
R=ventana_principal.cfg.get("icaro_config","colorR")
G=ventana_principal.cfg.get("icaro_config","colorG")
B=ventana_principal.cfg.get("icaro_config","colorB")
ventana_principal.fondo.FONDO = (int(R), int(G), int(B))

GObject.timeout_add(50, ventana_principal.timeout)
# gobject.idle_add(ventana_principal.timeout)
# gobject.PRIORITY_DEFAULT=-1
Gtk.main()
