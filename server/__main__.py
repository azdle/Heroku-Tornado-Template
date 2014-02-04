#!/usr/bin/python
import tornado.ioloop
import tornado.web
import os

################################################################################
#                                                                              #
#                          Web Handlers                                        #
#                                                                              #
################################################################################

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        pass

    def prepare(self):
        # Fix Stupid Browsers and not Sending Anything but "GET" and "POST"
        found_method = self.get_argument("_method", None)
        if found_method in ["GET", "HEAD", "POST", "PUT", "DELETE", "TRACE",
                            "OPTIONS", "CONNECT", "PATCH"]:
            self.request.method = found_method

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

################################################################################
#                                                                              #
#                          Main Web Application                                #
#                                                                              #
################################################################################

application = tornado.web.Application([
        (r"/",
            MainHandler),
        (r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {"path": "./server/static/"}),
    ],
    debug=True,
    cookie_secret=os.getenv('COOKIE_SECRET', "DEVELOPMENT_SECRET"))

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8888))
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
