from gi.repository import Gtk
import os
import time
import socket               # Import socket module
from clemente.clemente import SERVIDOR
import threading

class GUI:
    def __init__(self,ip="localhost",port=9999):
        self.serv = socket.socket()
        self.ip=ip
        self.port=port
        ventana = Gtk.Window()
        hbox = Gtk.HBox(False,2)
        vbox = Gtk.VBox(False,2)
        ventana.add(hbox)
        self.label_socket = Gtk.Label("servidor socket: ")
        self.label_icr = Gtk.Label("placa icaro: ")
        frame = Gtk.Frame("Normal Label")
        self.conectar = Gtk.ToggleButton(label="conectar", use_underline=True)
        self.conectar.connect("clicked",self.con)
        boton_status =Gtk.Button("status")
        boton_status.connect("clicked",self.status)
        vbox.pack_start(self.label_socket,False,False,1)
        vbox.pack_start(self.label_icr,False,False,1)
        vbox.pack_start(self.conectar,False,False,1)
        vbox.pack_start(boton_status,False,False,1)
        frame.add(vbox)
        #vbox.pack_start(frame, False, False, 0)
        self.server = SERVIDOR(False)
        #self.hilo = threading.Thread(target=self.server.run)
        hbox.pack_start(frame, False, False, 0)
        hbox.show()
        ventana.show_all()

    def status(self,widget):
        #try:
        #    sock_status="servidor socket: "+ str(self.server.status)
        #    self.label_socket.set_label(sock_status)
        #except:
        #    self.label_socket.set_label("servidor socket: False")
        self.serv.send("status")
        pet = self.serv.recv(1024)
        print pet
    def con(self,widget):
        if widget.get_active():
            #os.system("python clemente/clemente.py&")
            self.server.start()
            time.sleep(1)
            self.serv.connect((self.ip,self.port))
            self.status(None)
            widget.set_label("conectado")
        else:
            self.serv.send("salir")
            widget.set_label("conectar")
            #self.hilo._Thread__stop()
            #print self.hilo.is_alive()

        #if widget.get_active():
        #    self.hilo.start()
        #else:
        #    self.server.cerrar()
        #self.status(None)

