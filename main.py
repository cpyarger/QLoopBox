# This Python file uses the following encoding: utf-8
import sys
import os

import logging
import json
import mido
import base64

from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

import sys
import signal
import sounddevice as sd

import configparser

class MidiHandler(QtCore.QObject):
    SendMessage=pyqtSignal(str,str,str,name="SendMessage")
    def __init__(self):
        super(MidiHandler, self).__init__()
        logging.debug("MIDI Handler Class Startup")
        self.listen_to_next_message=False
    def midi_callback(self,message):
        if (self.listen_to_next_message):
            
            if message.type == "note_on":
                self.SendMessage.emit( "Note", "on", str(message.note))
            elif message.type == "note_off":
                self.SendMessage.emit( "Note","off", str(message.note))
            elif message.type == "control_change":
                self.SendMessage.emit( "control_change","cc", str(message.control))
            


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
    def set_button_defaults(self):
        self.config['buttons']={"button1":"Record MIDI 1",
        "button2":"Record MIDI 2",
        "button3":"Record MIDI 3",
        "button4":"Record MIDI 4",
        "button5":"Record MIDI 5",
        "button6":"Record MIDI 6",
        "button7":"Record MIDI 7",
        "buttonbpm":"Record MIDI BPM"}
        with open('example.ini', 'w') as configfile:
                self.config.write(configfile)
    def save_config(self):
        with open('example.ini', 'w') as configfile:
            self.config.write(configfile)
    def load_config(self):
        self.config.read('example.ini')
    def save_midi_mappings(self):
        self.config['buttons']["button1"]=form.pb_record_midi_1.text()
        self.config['buttons']["button2"]=form.pb_record_midi_2.text()
        self.config['buttons']["button3"]=form.pb_record_midi_3.text()
        self.config['buttons']["button4"]=form.pb_record_midi_4.text()
        self.config['buttons']["button5"]=form.pb_record_midi_5.text()
        self.config['buttons']["button6"]=form.pb_record_midi_6.text()
        self.config['buttons']["button7"]=form.pb_record_midi_7.text()
        self.config['buttons']["buttonbpm"]=form.pb_record_midi_bpm.text()
        self.save_config()
        
    def load_midi_mappings(self):
        try:
            form.pb_record_midi_1.setText(self.config['buttons']["button1"])
            form.pb_record_midi_2.setText(self.config['buttons']["button2"])
            form.pb_record_midi_3.setText(self.config['buttons']["button3"])
            form.pb_record_midi_4.setText(self.config['buttons']["button4"])
            form.pb_record_midi_5.setText(self.config['buttons']["button5"])
            form.pb_record_midi_6.setText(self.config['buttons']["button6"])
            form.pb_record_midi_7.setText(self.config['buttons']["button7"])
            form.pb_record_midi_bpm.setText(self.config['buttons']["buttonbpm"])
        except:
            logging.debug("No Button Data Found")
            self.set_button_defaults()
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

class QtWindowThings(QMainWindow):
    activepb =None
    def __init__(self):
         super().__init__()
         self.initUI()
         self.activepb


    def initUI(self):
        rec_midi_1=form.pb_record_midi_1
        rec_midi_2=form.pb_record_midi_2
        rec_midi_3=form.pb_record_midi_3
        rec_midi_4=form.pb_record_midi_4
        rec_midi_5=form.pb_record_midi_5
        rec_midi_6=form.pb_record_midi_6
        rec_midi_7=form.pb_record_midi_7
        rec_midi_bpm=form.pb_record_midi_bpm
        #Connect Record Midi Buttons to Record Midi Button Action.
        rec_midi_1.clicked.connect(self.record_midi)
        rec_midi_2.clicked.connect(self.record_midi)
        rec_midi_3.clicked.connect(self.record_midi)
        rec_midi_4.clicked.connect(self.record_midi)
        rec_midi_5.clicked.connect(self.record_midi)
        rec_midi_6.clicked.connect(self.record_midi)
        rec_midi_7.clicked.connect(self.record_midi)
        rec_midi_bpm.clicked.connect(self.record_midi)

    def record_midi(self):
        sender = self.sender()
        logging.debug("Record MIDI Button clicked " + sender.text())
        self.activepb=sender
        mc.listen_to_next_message=True

    def print_midi_message(self,type, oo, norc):
        if (type == "Note"):
            print ("type: "+type+" "+oo+ " "+"norc: "+norc)
            self.activepb.setText(type+" "+norc)
            mc.listen_to_next_message=False
            sh.save_midi_mappings()



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # Create Main Window and application
    Form, Window = uic.loadUiType("form.ui")
    app = QApplication(sys.argv)
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    mc=MidiHandler()
    sh=SaveHandler()
    
    qtwt=QtWindowThings()
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
    mc.SendMessage.connect(qtwt.print_midi_message)
    sh.load_midi_mappings()
    logging.debug("Program Startup")

    sys.exit(app.exec_())
