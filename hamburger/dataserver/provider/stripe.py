import stripe


class StripePayment():

    def __init__(self, sk):
        self.sk = sk

    def charge(self, id, amount):
        return stripe.Charge.create(api_key=self.sk,
                                    idempotency_key=id,
                                    stripe_account="Hamburger")
