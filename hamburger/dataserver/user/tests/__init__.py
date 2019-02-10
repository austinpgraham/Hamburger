import os

from zope.configuration import xmlconfig

from hamburger.dataserver.dataserver.tests import DataserverTestBase


class UserTestBase(DataserverTestBase):

    IZCML = os.path.join(os.path.dirname(__file__), "..", "configure.zcml")

    def setUp(self):
        super(DataserverTestBase, self).setUp()
        xmlconfig.file(self.IZCML)

    def tearDown(self):
        super(DataserverTestBase, self).tearDown()
