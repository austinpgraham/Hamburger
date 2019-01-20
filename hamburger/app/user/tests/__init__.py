import os

from pyramid import testing

from zope.configuration import xmlconfig

from hamburger.app.tests import AppTestBase


AUTHED_USER = {
    "username": "pgreazy",
    "password": "password",
    "first_name": "Austin",
    "last_name": "Graham",
    "email": "test@email.com",
    "phone_number": "test",
    "profile_pic": ""
}
NON_AUTHED_USER = {
    'username': "austinp",
    'password': 'password',
    'first_name': "Test",
    "last_name": "User",
    "email": "test@email.com",
    "phone_number": "test",
    "profile_pic": ""
}


class UserAppTestBase(AppTestBase):

    ZCML = os.path.join(os.path.dirname(__file__), "..", "..", "configure.zcml")

    def setUp(self):
        super(UserAppTestBase, self).setUp()
        xmlconfig.file(self.ZCML)
        self.setup_autheduser(**AUTHED_USER)

    def tearDown(self):
        super(UserAppTestBase, self).tearDown()
