'''
Created on Oct 5, 2013

@author: athiessen
'''
import os
import logging

from x10.controllers.cm11 import CM11
from x10.devices.notifier import Notifier
from brisa.core.reactors import install_default_reactor
reactor = install_default_reactor()
from brisa.upnp.device import Device, Service

logger = logging.getLogger(__name__)
logging.basicConfig( level=logging.DEBUG,
                     format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
                     datefmt='%Y-%m-%d %H:%M:%S' )

class SwitchPower(Service, Notifier):
    def __init__(self, controller, x10Device ):
        Service.__init__( self,
                          'SwitchPower',
                          'urn:schemas-upnp-org:service:SwitchPower:1',
                          '',
                          os.getcwd() + '/SwitchPower-scpd.xml' )
        self.actuator   = controller.actuator( x10Device )
        self.x10Address = x10Device
        self.target     = False
        self.status     = False
        controller.AddNotifier( self )

    def soap_SetTarget(self, *args, **kwargs):
        #self.target = kwargs['NewTargetValue']
        #self.status = self.target

        newTarget = kwargs['NewTargetValue']
        
        if( newTarget == '1' ):
            self.actuator.on()
        else:
            self.actuator.off()
            
        return {}
    
    def soap_GetTarget(self, *args, **kwargs):
        return {'RetTargetValue': self.target}
    
    def soap_GetStatus(self, *args, **kwargs):
        return {'ResultStatus': self.status}
    
    def Notify(self, houseCode, functionCode, functionName, amount, units ):
        if self.x10Address in units:
            if( functionName == 'On' ):
                logger.debug( 'X10 Light Device: %s On', self.x10Address )
                self.target = '1'
            elif( functionName == 'Off' ):
                logger.debug( 'X10 Light Device: %s Off', self.x10Address )
                self.target = '0'
                
            self.status = self.target
    
class X10Light(object):
    def __init__(self, name, x10Device, dimmable, room ):
        self.name       = name
        self.x10Device  = x10Device
        self.dimmable   = dimmable;
        self.room       = room
        self.device     = None
        logger.debug( 'New X10Light: Name: %s, Device: %s', self.name, self.x10Device )
        
        
    def CreateDevice(self):
        projectPage = 'http://www.github.com/AlanDThiessen/atha'
        self.device = Device( 'urn:schemas-upnp-org:device:BinaryLight:1',
                              self.room + ': ' + self.name,
                              manufacturer='Alan Thiessen',
                              manufacturer_url=projectPage,
                              model_name='Atha X10 Light Device',
                              model_description='A UPnP Light Device Representing an X10 Light',
                              model_number='1.0',
                              model_url=projectPage )
    def AddServices(self, controller):
        switch = SwitchPower( controller, self.x10Device )
        self.device.add_service(switch)
        
    def start(self, controller):
        logger.debug( 'Starting Light: %s', self.name )
        self.CreateDevice()
        self.AddServices( controller )
        self.device.start()
        reactor.add_after_stop_func(self.device.stop)
        #reactor.main()


class LightController(object):
    '''
    classdocs
    '''

    def __init__(self, config):
        '''
        Constructor
        '''
        self.serial     = config.device
        self.lights = []

        # Create the light objects
        for light in config.x10Devices:
            if( light['type'] == 'lamp' ):
                self.lights.append( X10Light( light['name'],
                                              light['id'],
                                              light['dimmable'],
                                              light['room'] ) )
                
        self.device     = None
        
    def Open(self):
        # Open the device
        self.device = CM11( self.serial )
        self.device.open()
        
        # Create the light objects
        for light in self.lights:
            light.start( self.device )

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
        
