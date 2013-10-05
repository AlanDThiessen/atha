'''
Created on Oct 3, 2013

@author: athiessen
'''

import os

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
    def __init__(self, name):
        Resource.__init__(self, name )
        
    def get_render(self, uri, params):
        return self
    
    def GetPage(self, name, content):
        page = '\n'.join( ( "<!DOCTYPE html>",
                            "<html>",
                            "<head>",
                            "   <title>Atha</title>",
                            "   <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
                            "   <script src=\"jquery-1.10.2.min.js\"></script>",
                            "   <script src=\"jquery.mobile-1.3.2.min.js\"></script>",
                            "   <script src=\"atha.js\"></script>",
                            "</head>",
                            "<body>",
                            "<div data-role=\"page\" id=\"", name, "\">",
                            "   <div data-role=\"panel\" id=\"navPanel\">",
                            "      <ul data-role=\"listview\" data-ajax=\"false\" data-inset=\"true\">",
                            "         <li><a href=\"#scenes\">Scenes</a></li>",
                            "         <li><a href=\"getLights\">Lights</a></li>",
                            "         <li><a href=\"#media\">Media</a></li>",
                            "         <li><a href=\"#devices\">Devices</a></li>",
                            "         <li><a href=\"#settings\">Settings</a></li>",
                            "      </ul>",
                            "   </div>",
                            "   <div data-role=\"header\"><a href=\"#navPanel\" data-icon=\"bars\" data-iconpos=\"notext\" data-shadow=\"false\" data-iconshadow=\"false\">Menu</a><h1>", name, "</h1></div>",
                            "   <div data-role=\"content\">",
                            content,
                            "   </div>",
                            "</div>",
                            "</body>",
                            "</html>" ) )
        return page
    
    def GetLights(self):
        lights  = '\n'.join( ( "<label for='flip-1'>", 'Couch Lamp', "</label>",
                               "   <select name='flip-1' id='flip-1' data-role='slider'>",
                               "      <option value='off'>Off</option>",
                               "      <option value='on'>On</option>",
                               "   </select>",
                               "   <label for='slider-10'>Level:</label>",
                               "   <input name='slider-10' id='slider-10' data-highlight='true' value='100' min='0' max='100' step='5' type='range'>" ) )
        return self.GetPage( 'Atha - Lights', lights )
    
    def render(self, uri, request, response):
        return self.GetLights()

class GetLights2(Resource):
    def __init__(self, name, tempPath ):
        Resource.__init__(self, name)
        self.templatePath = tempPath
        
    def get_render(self, uri, params):
        return self
    
    def render(self, uri, request, response):
        return self.GetLights()

    def GetLights(self):
        lights = ( { 'id':          'A1',
                     'name':        'Couch Lamp',
                     'dimmable':    True
                   },
                  
                   { 'id':          'A2',
                     'name':        'Chair Lamp',
                     'dimmable':    True
                   }
                 )
        roomsVar = ( { 'id':          'livingRoom',
                       'name':         'Living Room',
                       'lights':       lights
                     },
                   )
        template = '/'.join( ( self.templatePath, 'page.html' ) )
        pageTemplate = Template( filename=template )
        return pageTemplate.render( rooms=roomsVar, pageId='getLights' )

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
            
            greeter = GetLights2( 'getLights', config.templatePath )
            self.webserver.add_resource( greeter )

            print 'Webserver listening on', self.webserver.get_listen_url()
        else:
            print 'Please specify a configuration'
        
    def start(self):
        self.webserver.start()
        
    def stop(self):
        self.webserver.stop()
