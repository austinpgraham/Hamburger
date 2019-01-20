from io import StringIO

from hamcrest import is_not
from hamcrest import assert_that

from zope import component

from zope.configuration.xmlconfig import xmlconfig

from hamburger.dataserver.provider.tests import ProviderTestBase

from hamburger.dataserver.provider.interfaces import IProvider


ZCML_STRING = """
<configure xmlns='http://namespaces.zope.org/zope'
           xmlns:ham='http://hamburger.com/provider'
           i18n_domain="zope">

    <include package="hamburger.dataserver.provider" file="meta.zcml" />

    <ham:registerProvider
            name="ebay"
            provider="hamburger.dataserver.provider.ebay.EbayProvider"
            fetcher="hamburger.dataserver.provider.ebay.EbayFetcher"
            parser="hamburger.dataserver.provider.ebay.EbayParser"
            appID="AustinGr-Hamburge-PRD-660b9b3c7-a4f8c441"/>

</configure>
"""


class TestZCML(ProviderTestBase):

    def test_registration(self):
        xmlconfig(StringIO(ZCML_STRING))
        provider = component.getUtility(IProvider, "ebay")
        assert_that(provider, is_not(None))
