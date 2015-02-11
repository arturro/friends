import json

import motor

from tornado.testing import AsyncHTTPTestCase
import tornado.web
from tornado import gen

from ganymede.users.service_mongo import ServiceUserAddFriends, ServiceUserRemoveFriends, ServiceUserGetFriends, \
    ServiceUserRemoveAllFriends


class FriendsApplication(tornado.web.Application):
    def __init__(self, db, debug=False):
        handlers = [
            (r'/friends/add/(\d+)/(\d+)', ServiceUserAddFriends),
            (r'/friends/remove/(\d+)/(\d+)', ServiceUserRemoveFriends),
            (r'/friends/get/(\d+)', ServiceUserGetFriends),
            (r'/friends/remove/all', ServiceUserRemoveAllFriends),
        ]
        tornado.web.Application.__init__(self, handlers, db=db,
                                         debug=debug)


class MotorAsyncHTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.db = motor.MotorClient()['AsyncHTTPTestCase']
        return FriendsApplication(db=self.db, debug=True)


class TestAddFriendsServerMotor(MotorAsyncHTTPTestCase):
    def test_add_friends_should_return_status_1(self):
        self.http_client.fetch(self.get_url('/friends/add/2/1'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, json.dumps({"status": 1}))

    def test_double_add_friends_should_return_status_1(self):
        self.http_client.fetch(self.get_url('/friends/add/2/1'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/add/2/1'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, json.dumps({"status": 1}))

    def test_add_friends_with_0_should_return_http_error_500(self):
        self.http_client.fetch(self.get_url('/friends/add/2/0'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 500)

    def test_add_friends_with_the_same_id_should_return_http_error_500(self):
        self.http_client.fetch(self.get_url('/friends/add/2/2'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 500)

    def test_add_friends_with_no_integer_should_return_http_error_404(self):
        self.http_client.fetch(self.get_url('/friends/add/2/A'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)


class TestAddFriendsServerMotor(MotorAsyncHTTPTestCase):
    def test_remove_friends_should_return_status_1(self):
        self.http_client.fetch(self.get_url('/friends/remove/2/1'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, json.dumps({"status": 1}))

    def test_double_remove_friends_should_return_status_1(self):
        self.http_client.fetch(self.get_url('/friends/remove/2/1'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/remove/2/1'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, json.dumps({"status": 1}))

    def test_remove_friends_with_0_should_return_http_error_500(self):
        self.http_client.fetch(self.get_url('/friends/remove/2/0'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 500)

    def test_remove_friends_with_the_same_id_should_return_http_error_500(self):
        self.http_client.fetch(self.get_url('/friends/remove/2/2'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 500)

    def test_remove_friends_with_no_integer_should_return_http_error_404(self):
        self.http_client.fetch(self.get_url('/friends/remove/2/A'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)

class TestGetFriendsServerMotor(MotorAsyncHTTPTestCase):
    def test_get_friends_should_return_status_1(self):
        self.http_client.fetch(self.get_url('/friends/get/2'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, json.dumps({"status": 1, "friends": []}))

    def test_add_get_friends_should_return_status_1_and_friends(self):
        # self.http_client.fetch(self.get_url('/friends/remove/all'), self.stop)
        # response = self.wait()
        self.http_client.fetch(self.get_url('/friends/add/30/31'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/add/30/33'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/get/30'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, json.dumps({"status": 1, "friends": ["31", "33"]}))

    def test_add_remove_get_friends_should_return_status_1_and_friends(self):
        # self.http_client.fetch(self.get_url('/friends/remove/all'), self.stop)
        # response = self.wait()
        self.http_client.fetch(self.get_url('/friends/add/40/41'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/add/40/43'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/add/40/43'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/add/40/44'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/remove/40/43'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/remove/40/43'), self.stop)
        response = self.wait()
        self.http_client.fetch(self.get_url('/friends/get/40'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, json.dumps({"status": 1, "friends": ["41", "44"]}))


    def test_get_friends_with_0_should_return_http_error_500(self):
        self.http_client.fetch(self.get_url('/friends/get/0'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 500)

    def test_get_friends_with_no_integer_should_return_http_error_404(self):
        self.http_client.fetch(self.get_url('/friends/get/A'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)
