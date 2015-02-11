import tornado.web
import tornado.ioloop
from tornado import gen

from ganymede.users.exceptions import IncorrectUID

def _check_valid_uid(uid):
    try:
        uid = int(uid)
    except ValueError:
        raise IncorrectUID("uid is not integer")
    if uid < 1:
        raise IncorrectUID("uid is less than 1: %s" % uid)

def _check_valid_uids(uid_1, uid_2):
    _check_valid_uid(uid_1)
    _check_valid_uid(uid_2)
    if uid_1 == uid_2:
        raise IncorrectUID("uid_1 are the same as uid_2:  %s, %s" % (uid_1, uid_2))


class ServiceUserAddFriends(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, uid_1, uid_2):
        try:
            _check_valid_uids(uid_1, uid_2)
        except IncorrectUID as error:
            raise tornado.web.HTTPError(500, str(error))
        cnt = yield self.settings['db'].friends.find({'uid_1': uid_1, 'uid_2': uid_2}).count()
        if cnt == 0:
            yield self.settings['db'].friends.insert(
                ({'uid_1': uid_1, 'uid_2': uid_2},
                 {'uid_1': uid_2, 'uid_2': uid_1})
            )
        self.write({'status': 1})
        self.finish()


class ServiceUserRemoveFriends(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, uid_1, uid_2):
        try:
            _check_valid_uids(uid_1, uid_2)
        except IncorrectUID as error:
            raise tornado.web.HTTPError(500, str(error))
        cnt = yield self.settings['db'].friends.find({'uid_1': uid_1, 'uid_2': uid_2}).count()
        if cnt != 0:
            #yield self.settings['db'].friends.remove(({'uid_1': uid_1, 'uid_2': uid_2}, {'uid_1': uid_2, 'uid_2': uid_1}))
            yield self.settings['db'].friends.remove({'uid_1': uid_1, 'uid_2': uid_2})
            yield self.settings['db'].friends.remove({'uid_1': uid_2, 'uid_2': uid_1})
        self.write({'status': 1})
        self.finish()

class ServiceUserGetFriends(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, uid_1):
        try:
            _check_valid_uid(uid_1)
        except IncorrectUID as error:
            raise tornado.web.HTTPError(500, str(error))
        friends = []
        cursor = self.settings['db'].friends.find({'uid_1': uid_1})
        while (yield cursor.fetch_next):
            friend = cursor.next_object()
            friends.append(friend['uid_2'])
        self.write({'status': 1, 'friends': friends})
        self.finish()

class ServiceUserRemoveAllFriends(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        yield self.settings['db'].friends.remove()
        self.write({'status': 1})
        self.finish()