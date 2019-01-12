import json

from pyramid import testing

from hamburger.app.product.tests import ProductAppTestBase

from hamburger.dataserver.product.model import HamProduct


class TestViews(ProductAppTestBase):

    def test_donations(self):
        # Load a list
        _list = {
            'title': "MyTestList",
            'is_public': True
        }
        self.testapp.post("/users/pgreazy/wishlists", params=json.dumps(_list))
        # Load a product
        product = {
            'provider': 'ebay',
            'identifier': '190388062148'
        }
        self.testapp.post("/users/pgreazy/MyTestList", params=json.dumps(product))
        # Get product hamid
        resp = self.testapp.get("/users/pgreazy/MyTestList")
        data = json.loads(resp.body)
        item = list(data["items"].keys()).pop()
        # Test load of donation
        donation = {
            'token': 'tok_bypassPending',
            'amount': 999,
        }
        resp = self.testapp.post("/users/pgreazy/MyTestList/{}".format(item), params=json.dumps(donation))
        assert resp.status_code == 200
