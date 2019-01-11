import stripe

from zope import interface

from hamburger.dataserver.provider.interfaces import IStripePayment


@interface.implementer(IStripePayment)
class StripePayment():

    def __init__(self, sk):
        self.sk = sk
        stripe.api_key = sk

    def charge(self, token, amount, description, email):
        return stripe.Charge.create(
            amount=amount,
            currency="usd",
            description=description,
            source=token,
            receipt_email=email
        )

    def refund(self, token, partial=None):
        return stripe.Refund.create(
            charge=token,
            amount=partial
        )
