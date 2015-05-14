'''
Created on Oct 3, 2013

@author: athiessen
'''

from core.AthaConfig import AthaConfig
from LightController.LightController import LightController
from ControlPoint.AthaWeb import AthaWeb

# Start up the reactor
from brisa.core.reactors import install_default_reactor

lightController = None
athaWeb = None

def Shutdown():
    athaWeb.stop
    lightController.Close()

if __name__ == '__main__':
    reactor = install_default_reactor()

    config  = AthaConfig()
    lightController = LightController( config )
    lightController.Open()
    
    athaWeb = AthaWeb(config, lightController)
    athaWeb.start()
    
    reactor.add_after_stop_func(Shutdown)
    reactor.main()
