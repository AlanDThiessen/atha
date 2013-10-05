'''
Created on Oct 3, 2013

@author: athiessen
'''

from core.AthaConfig import AthaConfig
from ControlPoint.AthaWeb import AthaWeb

from brisa.core.reactors import install_default_reactor



if __name__ == '__main__':
    reactor = install_default_reactor()

    config  = AthaConfig()
    
    athaWeb = AthaWeb(config)
    
    athaWeb.start()
    
    reactor.add_after_stop_func(athaWeb.stop)
    reactor.main()
