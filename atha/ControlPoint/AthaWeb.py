'''
Created on Oct 3, 2013

@author: athiessen
'''

from core.AthaConfig import AthaConfig

from brisa.core.webserver import WebServer, StaticFile, Resource
from mako.template import Template


JQUERY              = "jquery-1.10.2.min.js"
JQUERY_MOBILE       = "jquery.mobile-1.3.2.min.js"
JQUERY_MOBILE_CSS   = "jquery.mobile-1.3.2.min.css"
ATHA_INDEX          = "atha.html"
ATHA_CSS            = "atha.css"
ATHA_JS             = "atha.js"


class GetLights(Resource):
    def __init__(self, name, tempPath ):
        Resource.__init__(self, name)
        self.templatePath = tempPath
        
    def get_render(self, uri, params):
        return self
    
    def render(self, uri, request, response):
        roomsVar = ( { 'id':          'livingRoom',
                       'name':         'Living Room',
                       'lights':       ( { 'id':          'A1',
                                           'name':        'Couch Lamp',
                                           'dimmable':    True
                                         },
                  
                                         { 'id':          'A2',
                                           'name':        'Chair Lamp',
                                           'dimmable':    True
                                         }
                                       )
                     },
                     { 'id':          'alansRoom',
                       'name':         'Alan\'s Room',
                       'lights':       ( { 'id':          'A3',
                                           'name':        'Room Lamp',
                                           'dimmable':    True
                                         },
                                       )
                     },
                     { 'id':          'basement',
                       'name':         'Basement',
                       'lights':       ( { 'id':          'B1',
                                           'name':        'Front Light',
                                           'dimmable':    True
                                         },
                  
                                         { 'id':          'B2',
                                           'name':        'Back Light',
                                           'dimmable':    True
                                         }
                                       )
                     },
                     { 'id':          'outside',
                       'name':         'Outside',
                       'lights':       ( { 'id':          'B4',
                                           'name':        'Front Light',
                                           'dimmable':    True
                                         },
                  
                                         { 'id':          'B5',
                                           'name':        'Back Light',
                                           'dimmable':    True
                                         }
                                       )
                     },
                   )
        
        pageTemplate = Template( filename= '/'.join( ( self.templatePath, 'page.html' ) ) )
        lightsTemplate = Template( filename= '/'.join( ( self.templatePath, 'lights.html' ) ) )
        lightsContent = lightsTemplate.render( rooms=roomsVar )
        return pageTemplate.render( pageContent=lightsContent, pageId='getLights', pageName='Lights' )


class SetLights(Resource):
    def __init__(self, name, action ):
        Resource.__init__(self, name)
        self.action = action
        
    def get_render(self, uri, params):
        return self
    
    def render(self, uri, request, response):
        params = request.params
        
        if( ( 'id' in params ) and ( 'action' in params ) ):
            if( params['action'] == 'on' ):
                self.action.LightOn( params['id'] )
            elif( params['action'] == 'off' ):
                self.action.LightOff( params['id'] )
        return ""

class AthaWeb(object):
    '''
    classdocs
    '''

    def __init__(self, config = None, athaAct = None ):
        '''
        Constructor
        '''
        if( isinstance( config, AthaConfig ) ):
            self.webserver = WebServer( config.serverName, config.host, config.port )
    
            self.webserver.add_static_file( StaticFile( JQUERY, '/'.join( ( config.webRoot, JQUERY ) ) ) )
            self.webserver.add_static_file( StaticFile( JQUERY_MOBILE, '/'.join( ( config.webRoot, JQUERY_MOBILE ) ) ) )
            self.webserver.add_static_file( StaticFile( JQUERY_MOBILE_CSS, '/'.join( ( config.webRoot, JQUERY_MOBILE_CSS ) ) ) )
            self.webserver.add_static_file( StaticFile( 'index.html', '/'.join( ( config.webRoot, ATHA_INDEX ) ) ) )
            self.webserver.add_static_file( StaticFile( '', '/'.join( ( config.webRoot, ATHA_INDEX ) ) ) )
            self.webserver.add_static_file( StaticFile( ATHA_CSS, '/'.join( ( config.webRoot, ATHA_CSS ) ) ) )
            self.webserver.add_static_file( StaticFile( ATHA_JS, '/'.join( ( config.webRoot, ATHA_JS ) ) ) )
            
            self.webserver.add_resource( GetLights( 'getLights', config.templatePath ) )
            self.webserver.add_resource( SetLights( 'setLights', athaAct ) )

            print 'Webserver listening on', self.webserver.get_listen_url()
        else:
            print 'Please specify a configuration'
        
    def start(self):
        self.webserver.start()
        
    def stop(self):
        self.webserver.stop()
