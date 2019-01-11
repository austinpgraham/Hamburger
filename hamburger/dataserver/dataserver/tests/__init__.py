import os
import unittest

from zope.configuration import xmlconfig


class DataserverTestBase(unittest.TestCase):

    ZCML = os.path.join(os.path.dirname(__file__), "..", "configure.zcml")

    def setUp(self):
        xmlconfig.file(self.ZCML)

    def tearDown(self):
        pass
