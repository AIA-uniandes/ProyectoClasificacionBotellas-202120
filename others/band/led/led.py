#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys
import ftrobopy                                              # Import the ftrobopy module
from TouchStyle import *

class FtcGuiApplication(TouchApplication):
    def __init__(self, args):
        TouchApplication.__init__(self, args)

        # create the empty main window
        w = TouchWindow("Tut_3_3")

        try:
            self.txt = ftrobopy.ftrobopy("localhost", 65000) # connect to TXT's IO controller
        except:
            self.txt = None                                  # set TXT to "None" of connection failed

        if not self.txt:
	        # display error of TXT could no be connected
            # error messages is centered and may span
            # over several lines
            err_msg = QLabel("Error connecting IO server")   # create the error message label
            err_msg.setWordWrap(True)                        # allow it to wrap over several lines
            err_msg.setAlignment(Qt.AlignCenter)             # center it horizontally
            w.setCentralWidget(err_msg)                      # attach it to the main output area
        else:
            # initialization went fine. So the main gui
            # is being drawn
            button = QPushButton("Toggle O1")                # create a button labeled "Toggle O1"
            button.clicked.connect(self.on_button_clicked)   # connect button to event handler
            w.setCentralWidget(button)                       # attach it to the main output area

	    # configure all TXT outputs to normal mode
            M = [ self.txt.C_OUTPUT, self.txt.C_OUTPUT, self.txt.C_OUTPUT, self.txt.C_OUTPUT ]
            I = [ (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ),
                  (self.txt.C_SWITCH, self.txt.C_DIGITAL ) ]
            self.txt.setConfig(M, I)
            self.txt.updateConfig()
            

	        # initially switch light on
            self.light_on = True

        w.show()
        self.exec_()

    # an event handler for our button (called a "slot" in qt)
    # it will be called whenever the user clicks the button
    def on_button_clicked(self):
        try:
            self.light_on = not self.light_on                  
            if self.light_on:                                  
                self.txt.i2c_write('0x8','0x0','0xff')         
            else:
                self.txt.i2c_write('0x8','0x0','0x00')         
        
        except:
            w = TouchWindow("Tut_3_4")
            err_msg = QLabel("Error connecting IO server") 
            err_msg.setWordWrap(True)                      
            err_msg.setAlignment(Qt.AlignCenter)           
            w.setCentralWidget(err_msg)     
            w.show()               

if __name__ == "__main__":
    FtcGuiApplication(sys.argv)
