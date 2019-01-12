import os
import stripe
import unittest

from zope.component import getGlobalSiteManager

from zope.configuration import xmlconfig

from hamburger.dataserver.provider.interfaces import IStripePayment

from hamburger.dataserver.provider.stripe import StripePayment


class ProviderTestBase(unittest.TestCase):

    ZCML = os.path.join(os.path.dirname(__file__), "..", "configure.zcml")

    def setUp(self):
        xmlconfig.file(self.ZCML)
        payment = StripePayment("sk_test_P413BkDG2R07lTOp5ERdyfli")
        gsm = getGlobalSiteManager()
        gsm.registerUtility(payment, IStripePayment)

    def tearDown(self):
        pass
