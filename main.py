#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.options

import os

from tornado.options import define, options
define("port", default=5000, help="run on the given port", type=int)

from handlers import *

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainPageHandler),
            (r"/portfolio", PortfolioHandler)
        ]
        settings = {
            'template_path':
                os.path.join(os.path.dirname(__file__), "templates"),
            'static_path':
                os.path.join(os.path.dirname(__file__), "static"),
            'cookie_secret': 
                '5iA9R2OTTV+H5YuwjBkFSxgF9Kq+AEWimHQwQ3EDDzg=',
            'debug': True
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()