# This Python file uses the following encoding: utf-8
import sys
import os

import logging
import json
import mido
import base64
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import sys
import signal
import sounddevice as sd


class MidiHandler():
    def __init__(self):
        logging.debug("MIDI Handler Class Startup")




if __name__ == "__main__":
    Form, Window = uic.loadUiType("form.ui");

    app = QApplication(sys.argv);
    window = Window();
    form = Form();
    form.setupUi(window);
    window.show();
    mc=MidiHandler();
    form.cb_midi_in.addItems(mido.get_input_names());
    form.cb_midi_out.addItems(mido.get_output_names());
    devices=sd.query_devices();
    for o in devices:

        if (o["max_input_channels"] > 0):
            print (o["name"])
            form.cb_audio_in.addItem(o["name"])
        if (o["max_output_channels"] > 0):
            print (o["name"])
            form.cb_audio_out.addItem(o["name"])
    logging.debug("Program Startup");

    sys.exit(app.exec_());
