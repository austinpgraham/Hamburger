import os
import unittest

from pyramid.compat import configparser

from zope import component

from zope.component import getGlobalSiteManager

from zope.configuration import xmlconfig

from hamburger.dataserver.dataserver.interfaces import ISimonAPI

from hamburger.dataserver.dataserver.model import SimonAPI


# Path to testing.ini
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "conf")

class DataserverTestBase(unittest.TestCase):

    ZCML = os.path.join(os.path.dirname(__file__), "..", "configure.zcml")

    def setUp(self):
        xmlconfig.file(self.ZCML)
        config = configparser.ConfigParser()
        config.read(os.path.join(CONFIG_PATH, 'testing.ini'))
        settings = dict(config['app:main'])

        # Register Simon API
        sm = getGlobalSiteManager()
        api = SimonAPI(settings['simon.url'])
        sm.registerUtility(api, ISimonAPI)

    def tearDown(self):
        pass
