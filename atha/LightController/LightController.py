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
    def __init__(self, controller, actuator, x10Device ):
        Service.__init__( self,
                          'SwitchPower',
                          'urn:schemas-upnp-org:service:SwitchPower:1',
                          '',
                          os.getcwd() + '/SwitchPower-scpd.xml' )
        self.actuator   = actuator
        self.x10Address = x10Device
        self.target     = False
        self.status     = False
        controller.AddNotifier( self )

    def soap_SetTarget(self, *args, **kwargs):
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


class Dimming(Service, Notifier):
    MAX_BRIGHT = 22     # Maximum brightness for X10 lamp
    MIN_BRIGHT = 2      # Minimum brightness for X10 lamp (it's really 0; but hey, this makes math easier)

    def __init__(self, controller, actuator, x10Device ):
        Service.__init__( self,
                          'Dimming',
                          'urn:schemas-upnp-org:service:Dimming:1',
                          '',
                          os.getcwd() + '/Dimming-scpd.xml' )
        self.actuator   = actuator
        self.x10Address = x10Device
        self.loadLevelTarget = self.MAX_BRIGHT
        self.loadLevelStatus = self.MAX_BRIGHT
        controller.AddNotifier( self )

    def soap_SetLoadLevelTarget(self, *args, **kwargs):
        percentage = kwargs['newLoadlevelTarget']

        newlevel = ( int( percentage ) * ( self.MAX_BRIGHT - self.MIN_BRIGHT ) / 100 ) + self.MIN_BRIGHT

        if( newlevel > self.loadLevelStatus ):
            self.actuator.bright( newlevel - self.loadLevelStatus )
        elif( newlevel < self.loadLevelStatus ):
            self.actuator.dim( self.loadLevelStatus - newlevel )

        return {}

    def soap_GetLoadLevelTarget(self, *args, **kwargs):
        return {'GetLoadlevelTarget': str( self.loadLevelTarget * 100 / self.MAX_BRIGHT ) }
    
    def soap_GetLoadLevelStatus(self, *args, **kwargs):
        return {'retLoadlevelStatus': str( self.loadLevelStatus * 100 / self.MAX_BRIGHT )}

    def Notify(self, houseCode, functionCode, functionName, amount, units ):
        if self.x10Address in units:
            if( functionName == 'Bright' ):
                logger.debug( 'X10 Light Device: %s Brighter by %d', self.x10Address, amount )
                self.loadLevelTarget += amount
                
                if( self.loadLevelTarget > self.MAX_BRIGHT ):
                    self.loadLevelTarget = self.MAX_BRIGHT
                    
            elif( functionName == 'Dim' ):
                logger.debug( 'X10 Light Device: %s Dimmer by %d', self.x10Address, amount )
                self.loadLevelTarget -= amount
                
                if( self.loadLevelTarget < self.MIN_BRIGHT ):
                    self.loadLevelTarget = self.MIN_BRIGHT
                
            self.loadLevelStatus = self.loadLevelTarget


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
        switch = SwitchPower( controller, self.actuator, self.x10Device )
        self.device.add_service(switch)
        
        if( self.dimmable ):
            dimmer = Dimming( controller, self.actuator, self.x10Device )
            self.device.add_service( dimmer )
        
    def start(self, controller):
        logger.debug( 'Starting Light: %s', self.name )
        self.actuator = controller.actuator( self.x10Device )
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
        
