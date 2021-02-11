# This Python file uses the following encoding: utf-8
import sys
import os

import logging
import json
import mido
import base64
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtCore import Signal, Slot, QObject
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import sys
import signal
import sounddevice as sd

import configparser
class MidiHandler():
    
    def __init__(self):
        logging.debug("MIDI Handler Class Startup")

    def midi_callback(self,message):
        print(message)
    def open_midi_port(self, port_name):
        try:
            self.port = mido.open_input(port_name, callback=self.midi_callback)
            logging.debug(u"opened port {}".format(port_name))
        except:
            logging.debug(u"\nCould not open {}".format(port_name))
    def close_midi_in_port(self):
        logging.debug(u"Closed port {} ".format(self.port.name))
        self.port.close()

    def open_midi_output_port(self, port_name):
        try:
            self.out_port = mido.open_output(port_name, callback=self.midi_callback)
            logging.debug(u"opened port {}".format(port_name))
        except:
            logging.debug(u"\nCould not open {}".format(port_name))
    def close_midi_output_port(self):
        logging.debug(u"Closed port {} ".format(self.out_port.name))
        self.out_port.close()

class SaveHandler():
    def __init__(self):
        logging.debug("Save Handler Loading")
        self.config = configparser.ConfigParser()
        try:
            self.config.read('example.ini')
        except:
            self.config['default']={"midi_in_device":'',
            "midi_out_device":'',
            "audio_in_device":'',
            "audio_out_device":''}
            with open('example.ini', 'w') as configfile:
                self.config.write(configfile)
    def save_config(self):
        with open('example.ini', 'w') as configfile:
            self.config.write(configfile)
    def load_config(self):
        self.config.read('example.ini')

def confchange(change):
    mc.close_midi_in_port()
    mc.close_midi_output_port()
    sh.config['default']["midi_in_device"]=form.cb_midi_in.currentText()
    sh.config['default']["midi_out_device"]=form.cb_midi_out.currentText()
    sh.config['default']["audio_in_device"]=form.cb_audio_in.currentText()
    sh.config['default']["audio_out_device"]=form.cb_audio_out.currentText()
    sh.save_config()
    mc.open_midi_port(form.cb_midi_in.currentText())
    mc.open_midi_output_port(form.cb_midi_out.currentText())

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Create Main Window and application
    Form, Window = uic.loadUiType("form.ui");
    app = QApplication(sys.argv)
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    mc=MidiHandler()
    sh=SaveHandler()
    

    # Populate Device Combo boxes
    # Populate Midi Device Combo Boxes
    form.cb_midi_in.addItems(mido.get_input_names())
    form.cb_midi_out.addItems(mido.get_output_names())
    # Populate Sound Device Combo boxes
    devices=sd.query_devices()
    for o in devices:
        if (o["max_input_channels"] > 0):
            form.cb_audio_in.addItem(o["name"])
        if (o["max_output_channels"] > 0):
            form.cb_audio_out.addItem(o["name"])
    # Load Config File, and Set Device Combo Boxes to their previous values
    sh.load_config()
    form.cb_midi_in.setCurrentText(sh.config['default']["midi_in_device"])
    form.cb_midi_out.setCurrentText(sh.config['default']["midi_out_device"])
    form.cb_audio_in.setCurrentText(sh.config['default']["audio_in_device"])
    form.cb_audio_out.setCurrentText(sh.config['default']["audio_out_device"])
    # Connect Signals/Slots
    # Save Device Combo Box Values to config
    form.cb_midi_in.currentTextChanged.connect(confchange)
    form.cb_midi_out.currentTextChanged.connect(confchange)
    form.cb_audio_in.currentTextChanged.connect(confchange)
    form.cb_audio_out.currentTextChanged.connect(confchange)
    #
    
    mc.open_midi_port(sh.config['default']["midi_in_device"])
    mc.open_midi_output_port(sh.config['default']["midi_out_device"])
    logging.debug("Program Startup")

    sys.exit(app.exec_())
