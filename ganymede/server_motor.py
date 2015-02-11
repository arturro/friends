import tornado.web
import tornado.ioloop
import motor
import tornado.httpserver
from tornado.options import define, options

from ganymede.users.service_mongo import ServiceUserAddFriends, ServiceUserRemoveFriends, ServiceUserGetFriends


define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="Debug", type=bool)
define("mongodb_port", default=27017, help="MongoDB port", type=int)
define("mongo_server", default='localhost', help="MongoDB server", type=str)
define("mongo_collection", default='friends', help="MongoDB collection", type=str)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class FriendsApplication(tornado.web.Application):
    def __init__(self, db, debug=False):
        handlers = [
            (r'/', IndexHandler),
            (r'/friends/add/(\d+)/(\d+)', ServiceUserAddFriends),
            (r'/friends/remove/(\d+)/(\d+)', ServiceUserRemoveFriends),
            (r'/friends/get/(\d+)', ServiceUserGetFriends),

        ]
        tornado.web.Application.__init__(self, handlers, db=db,
                                         debug=debug)


def main():
    tornado.options.parse_command_line()
    db = motor.MotorClient(options.mongo_server, options.mongodb_port)[options.mongo_collection]
    http_server = tornado.httpserver.HTTPServer(FriendsApplication(db=db, debug=options.debug))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()