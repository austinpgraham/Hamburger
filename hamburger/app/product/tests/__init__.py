import os

from pyramid import testing

from zope.configuration import xmlconfig

from hamburger.app.tests import AppTestBase


AUTHED_USER = {
    "username": "pgreazy",
    "password": "password",
    "first_name": "Austin",
    "last_name": "Graham",
    "email": "test@email.com"
}
NON_AUTHED_USER = {
    'username': "austinp",
    'password': 'password',
    'first_name': "Test",
    "last_name": "User",
    "email": "test@email.com"
}


class ProductAppTestBase(AppTestBase):

    ZCML = os.path.join(os.path.dirname(__file__), "..", "..", "configure.zcml")

    def setUp(self):
        super(ProductAppTestBase, self).setUp()
        xmlconfig.file(self.ZCML)
        self.setup_autheduser(**AUTHED_USER)

    def tearDown(self):
        super(ProductAppTestBase, self).tearDown()
