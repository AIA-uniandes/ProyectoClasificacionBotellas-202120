#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import time
import json

import sys
import os
from TouchStyle import *

import smbus
#import struct, array, math

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1


class TouchGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        self.win = TouchWindow("Band Controller")
        self.vbox = QVBoxLayout()
        self.vbox.addStretch()

        buttonP = QPushButton("Prender bus")
        buttonP.clicked.connect(self.turn_on)
        self.vbox.addWidget(buttonP)
        buttonAV = QPushButton("Aumentar Velocidad")
        buttonAV.clicked.connect(self.up_v)
        self.vbox.addWidget(buttonAV)
        buttonDV = QPushButton("Disminuir Velocidad")
        buttonDV.clicked.connect(self.down_v)
        self.vbox.addWidget(buttonDV)
        buttonI = QPushButton("Invertir Direccion")
        buttonI.clicked.connect(self.revert)
        self.vbox.addWidget(buttonI)
        #set initial values
        self.band_on = False
        self.vel = 1
        self.dir = True
        #initialize interface
        self.vbox.addStretch()
        self.win.centralWidget.setLayout(self.vbox)
        self.win.show()
        self.exec_()

    def turn_on(self):
        self.band_on = not self.band_on
        if self.band_on:
            self.move_band()
        else:
            bus.write_byte(8, 0)
    def revert(self):
        self.dir = not self.dir
        self.move_band()
    def up_v(self):
        if self.vel<5:
            self.vel= self.vel +1
            self.move_band()

    def down_v(self):
        if self.vel >1:
            self.vel = self.vel - 1
            self.move_band()
    
    def move_band(self):
        print(self.vel)
        print(type(self.vel))
        if self.dir:
            bus.write_byte(8, 6-self.vel)
        else:
            bus.write_byte(8,5+self.vel)



if __name__ == "__main__":
    TouchGuiApplication(sys.argv)


