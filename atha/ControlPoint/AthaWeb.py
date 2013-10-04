'''
Created on Oct 3, 2013

@author: athiessen
'''

from core.AthaConfig import AthaConfig

from brisa.core.webserver import WebServer, StaticFile
#from brisa.core.reactors import install_default_reactor
#reactor = install_default_reactor()


JQUERY              = "jquery-1.10.2.min.js"
JQUERY_MOBILE       = "jquery.mobile-1.3.2.min.js"
JQUERY_MOBILE_CSS   = "jquery.mobile-1.3.2.min.css"
ATHA_INDEX          = "atha.html"
ATHA_CSS            = "atha.css"


class AthaWeb(object):
    '''
    classdocs
    '''

    def __init__(self, config = None, athaAct = None ):
        '''
        Constructor
        '''
        if( config != None ):
            self.webserver = WebServer( 'atha', '192.168.1.21', 8080 )
    
            self.webserver.add_static_file( StaticFile( JQUERY, '/'.join( ( config.webRoot, JQUERY ) ) ) )
            self.webserver.add_static_file( StaticFile( JQUERY_MOBILE, '/'.join( ( config.webRoot, JQUERY_MOBILE ) ) ) )
            self.webserver.add_static_file( StaticFile( JQUERY_MOBILE_CSS, '/'.join( ( config.webRoot, JQUERY_MOBILE_CSS ) ) ) )
            self.webserver.add_static_file( StaticFile( 'index.html', '/'.join( ( config.webRoot, ATHA_INDEX ) ) ) )
            self.webserver.add_static_file( StaticFile( '', '/'.join( ( config.webRoot, ATHA_INDEX ) ) ) )
            self.webserver.add_static_file( StaticFile( ATHA_CSS, '/'.join( ( config.webRoot, ATHA_CSS ) ) ) )
            print 'Webserver listening on', self.webserver.get_listen_url()
        else:
            print 'Please specify a configuration'
        
    def start(self):
        self.webserver.start()
        
    def stop(self):
        self.webserver.stop()
