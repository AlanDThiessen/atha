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