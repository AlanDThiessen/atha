'''
Created on Oct 4, 2013

@author: athiessen
'''

from brisa.core.network import parse_url
from brisa.core.threaded_call import run_async_function

from brisa.upnp.control_point.control_point import ControlPoint


service = ('u', 'urn:schemas-upnp-org:service:SwitchPower:1')
binary_light_type = 'urn:schemas-upnp-org:device:BinaryLight:1'


class AthaControlPoint(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        