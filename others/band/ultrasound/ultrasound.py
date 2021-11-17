#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import time
import json

import sys
import os
from TouchStyle import *
import ftrobopy
import smbus
#import struct, array, math

bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1


class TouchGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        w = TouchWindow("Ultra Sonido")

        # try to read TXT_IP environment variable
        txt_ip = os.environ.get('TXT_IP')
        try:
            # connect to TXT's IO controller
            self.txt = ftrobopy.ftrobopy("localhost", 65000)
        except:
            self.txt = None

        vbox = QVBoxLayout()

        if not self.txt:
            err_msg = QLabel("Error connecting IO server")
            err_msg.setWordWrap(True)
            err_msg.setAlignment(Qt.AlignCenter)
            vbox.addWidget(err_msg)
        else:
            button = QPushButton("Toggle O1")
            button.clicked.connect(self.on_button_clicked)
            vbox.addWidget(button)

            M = [self.txt.C_OUTPUT, self.txt.C_OUTPUT,
                 self.txt.C_OUTPUT, self.txt.C_OUTPUT]
            I = [(self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL),
                 (self.txt.C_SWITCH, self.txt.C_DIGITAL)]
            self.txt.setConfig(M, I)
            self.txt.updateConfig()

            # initialize ultrasound
            self.ultrasound = self.txt.ultrasonic(1)

            # assume initually the button is not pressed
            self.distance = 0
            self.light_on = False
            self.timer = QTimer(self)                        # create a timer
            # connect timer to on_timer slot
            self.timer.timeout.connect(self.on_timer)
            # fire timer every 100ms (10 hz)
            self.timer.start(100)


        w.centralWidget.setLayout(vbox)
        w.show()
        self.exec_()

    def toggle_light(self,value):
            self.txt.setPwm(0, value)                   # PWM=0 means off

    # an event handler for our button (called a "slot" in qt)
    # it will be called whenever the user clicks the button
    def on_button_clicked(self):
        self.toggle_light(128)

    # an event handler for the timer (also a qt slot)
    def on_timer(self):
        # change saved state to reflect input state
        self.distance = self.ultrasound.distance()
        print(self.distance)
        # toggle lamp state if button has been pressed
        if self.distance > 200 and not self.light_on:
            self.toggle_light(128)
        elif self.distance <= 200 and self.light_on:
            self.toggle_light(0)


if __name__ == "__main__":
    TouchGuiApplication(sys.argv)
