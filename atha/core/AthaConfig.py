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
        self.WEB_PATH   = "html"
        
        currentDir = os.path.dirname( os.path.abspath(__file__) )

        self.webRoot = '/'.join( ( currentDir, self.WEB_PATH ) )
