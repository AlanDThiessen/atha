'''
Created on Oct 3, 2013

@author: athiessen
'''

import os


class AthaConfig(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.athaRoot       = os.path.dirname( os.path.abspath(__file__ + "/../" ) )
        self.controlPoint   = '/'.join( ( self.athaRoot, 'ControlPoint' ) )
        self.serverName     = 'Atha'
        self.webRoot        = '/'.join( ( self.controlPoint, 'html' ) )        
        self.templatePath   = '/'.join( ( self.controlPoint, 'templates' ) )
        self.host           = 'localhost'
        self.port           = 8080
        
        self.device         = '/dev/ttyUSB0'

        self.x10Devices     = ( { 'id':        'A1',
                                  'type':      'lamp',
                                  'name':      'Couch Lamp',
                                  'dimmable':  True,
                                  'room':      'Living Room'
                                },
                  
                                { 'id':        'A2',
                                  'type':      'lamp',
                                  'name':      'Chair Lamp',
                                  'dimmable':  True,
                                  'room':      'Living Room'
                                },
                        
                                { 'id':        'A3',
                                  'type':      'lamp',
                                  'name':      'Lamp',
                                  'dimmable':  True,
                                  'room':      "Alan's Room"
                                },
                        
                                { 'id':        'B1',
                                  'type':      'lamp',
                                  'name':      'Front Light',
                                  'dimmable':  True,
                                  'room':      'Basement'
                                },
  
                                { 'id':        'B2',
                                  'type':      'lamp',
                                  'name':      'Back Light',
                                  'dimmable':  True,
                                  'room':      'Basement'
                                },
                        
                                { 'id':        'B4',
                                  'type':      'lamp',
                                  'name':      'Front Light',
                                  'dimmable':  False,
                                  'room':      'Outside'
                                },
                  
                                { 'id':        'B5',
                                  'type':      'lamp',
                                  'name':      'Back Light',
                                  'dimmable':  False,
                                  'room':      'Outside'
                                }
                              )
