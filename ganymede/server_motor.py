import logging

import motor
import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import define, options

from ganymede.users.service_mongo import ServiceUserAddFriends, ServiceUserRemoveFriends, ServiceUserGetFriends


"""
API to add/remove/get list of connections between users

requiments:

    python
    tornado
    MongoDB

run:
    server_motor.py
    use virtualenv and add path to PYTHON_PATH for example

    . /srv/backend/ganymede-friends/env/current/bin/activate
    export PYTHONPATH=/srv/backend/ganymede-friends/releases/current:/srv/backend/ganymede-friends/releases/current/ganymede:/srv/backend/ganymede-friends/env/current/lib/python2.7/site-packages
    python /srv/backend/ganymede-friends/releases/current/ganymede/server_motor.py

    options:
    see all option use: -h
    --debug                          Debug (default False)
    --mongo_collection               MongoDB collection (default friends)
    --mongo_server                   MongoDB server (default localhost)
    --mongodb_port                   MongoDB port (default 27017)
    --port                           run on the given port (default 8000)


API
    add friends
        url: /friends/add/UID_1/UID_2
        this function add connection between two users with UID_1 and UID_2
        UID_1 and UID_2 must be integer greater than 0 and different from each other
        returns json: {"status": 1}
        for UID dfferent than integer API return 404
        for UID_1 = UID_2 API return 500

    remove friends
        url: /friends/remove/UID_1/UID_2
        this funcion removes connection between two users with UID_1 and UID_2
        UID_1 and UID_2 must be integer greater than 0 and different from each other
        returns json: {"status": 1}
        for UID dfferent than integer API return 404
        for UID_1 = UID_2 API return 500

    get friends
        url: /friends/get/UID_1
        this function get all connection between for user with UID_1
        UID_1 must be integer greater than 0
        returns json with list of all friends, for example:  {"status": 1, "friends": ["1", "12", "15"]}
        for UID dfferent than integer API return 404

"""

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
    logging.info('Starting up')
    db = motor.MotorClient(options.mongo_server, options.mongodb_port)[options.mongo_collection]
    http_server = tornado.httpserver.HTTPServer(FriendsApplication(db=db, debug=options.debug))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()