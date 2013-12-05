from serviceManager import ServiceManager
from config import PORT

import uuid
import os
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line

define("port", default=PORT, help="run on the given port", type=int)
#this a non-singleton
service_manager = ServiceManager()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
       self.render("index.html", service=service_manager.services,
                   messages=[])

class CustomerMessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
            "from":"customer",
        }
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message,
                               response=service_manager.process(message)))

        self.write(message)

class ServiceMessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        if self.get_argument("online")=="online":
            command = " online"
        else:
            command = " offline"
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body") + command,
            "from":"service",
        }
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message,
                               response=service_manager.process(message)))

        self.write(message)


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/zhihu", MainHandler),
            (r"/zhihu/a/customer/new", CustomerMessageNewHandler),
            (r"/zhihu/a/service/new", ServiceMessageNewHandler),
            ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "./templates"),
        static_path=os.path.join(os.path.dirname(__file__), "./static"),
        xsrf_cookies=True,
        )
    app.listen(options.port)
    print "visit host:%s/zhihu" % PORT
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
