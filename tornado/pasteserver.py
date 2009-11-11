# mrowl

"""Adds support for paste (and thus pylons) to the Tornado http server

It uses the wsgi module in tornado to wrap around the wsgi app that
would normally be passed through to the paste http server.  To do
this it defines the server_factory *or* server_runner factory 
functions defined in the paste API 
(see http://pythonpaste.org/deploy/#paste-server-factory)

To use this module just change the [server:main] section of your conf
file (e.g. development.ini) after rebuilding and installing the tornado
package.

Example conf entry:

[server:main]
paste.server_runner = tornado.pasteserver:server_runner
host = 127.0.0.1
port = 8000


You can replace "server_runner" with "server_factory" if you desire.

Run your server as you normally would with something like:
    paster serve --reload development.ini

"""

import tornado.httpserver
import tornado.ioloop
import tornado.wsgi

def server_factory(paste_conf, host, port):
    """
    Takes in host and port (paste_conf is superfluous) and returns a
    function that will start up the server given a wsgi application.
    """

    port = int(port)
    def serve(wsgi_app):
        container = tornado.wsgi.WSGIContainer(wsgi_app)
        http_server = tornado.httpserver.HTTPServer(container)
        http_server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    return serve
        
def server_runner(wsgi_app, *paste_conf, **server_conf):
    """ 
    wsgi_app - the wsgi app to put in the tornado container
    paste_conf - dict with some paste environment values
    server_conf - dict with host and port
    No returns, runs server.

    """
    container = tornado.wsgi.WSGIContainer(wsgi_app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(int(server_conf['port']))
    tornado.ioloop.IOLoop.instance().start()
