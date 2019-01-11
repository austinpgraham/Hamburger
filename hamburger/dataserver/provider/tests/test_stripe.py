from hamcrest import is_
from hamcrest import is_not
from hamcrest import assert_that

from zope import component

from hamburger.dataserver.provider.tests import ProviderTestBase

from hamburger.dataserver.provider.interfaces import IStripePayment


class TestStripe(ProviderTestBase):

    def test_utility(self):
        sp = component.getUtility(IStripePayment)
        assert_that(sp, is_not(None))

    def test_stripe(self):
        sp = component.getUtility(IStripePayment)
        # Test charges
        test_success_token = 'tok_bypassPending'
        result = sp.charge(test_success_token, 999, "Test desc", "austingraham731@gmail.com")
        assert_that(result.failure_code, is_(None))
        # Test refund
        result = sp.refund(result.id)
        assert_that(result.amount, is_(999))
