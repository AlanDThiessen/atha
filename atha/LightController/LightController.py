'''
Created on Oct 5, 2013

@author: athiessen
'''
import sys
import os

sys.path.append(os.path.expanduser('~/git/python-x10'))
from x10.controllers.cm11 import CM11


class LightController(object):
    '''
    classdocs
    '''

    def __init__(self, config):
        '''
        Constructor
        '''
        self.serial = config.device;
        self.device = None
        
    def Open(self):
        # Open the device
        self.device = CM11( self.serial )
        self.device.open()

    def Close(self):
        self.device.close()

    def LightOn(self, light ):
        module = self.device.actuator( light )
        module.on()

    def LightOff(self, light ):
        module = self.device.actuator( light )
        module.off()

    def SetLevel( self, light, level ):
        newlevel = ( int( level ) * 20 / 100 ) + 2
        module = self.device.actuator( light )
        module.bright(22)
        module.dim( 22 - newlevel )
        
