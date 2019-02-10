import fudge

from hamcrest import is_
from hamcrest import is_not
from hamcrest import has_entries
from hamcrest import assert_that
does_not = is_not

from pyramid import testing

from hamburger.dataserver.user.tests import UserTestBase

from hamburger.dataserver.user.model import HamUser
from hamburger.dataserver.user.model import HamUserCollection

from hamburger.dataserver.product.model import HamProductCollection


class TestUserModel(UserTestBase):

    @fudge.patch("hamburger.dataserver.user.model.HamUser._simon_create")
    def test_user(self, _sc):
        _sc.is_callable().returns(201)
        # Test that a user creates correctly
        user = HamUser(
            username="pgreazy",
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            password="password",
            phone_number="number",
            birthday="21 May 1995"
        )
        # Create a fake collection
        pc = HamProductCollection(
            title="MyTestCollection",
            is_public=True
        )
        # Add the collection to the user
        user["MyTestCollection"] = pc
        # Verify tested user properties
        assert_that(user.username, is_("pgreazy"))
        assert_that(user.check_auth(), is_(user))
        assert_that(user.is_empty(), is_(False))
        assert_that("MyTestCollection" in user, is_(True))
        test_pc = user["MyTestCollection"]
        # Test get and set of product collections
        assert_that(test_pc, is_(pc))

        # Test conversion to JSON
        result = user.to_json(testing.DummyRequest(), authed_user=user)
        assert_that(result, has_entries({
            'username': 'pgreazy',
            'first_name': 'Austin',
            'last_name': 'Graham',
            'email': 'austingraham731@gmail.com'
        }))
        assert_that(result, does_not(has_entries({
            'password': 'password'
        })))

    @fudge.patch("hamburger.dataserver.user.model.HamUser._simon_create")
    def test_user_collection(self, _sc):
        _sc.is_callable().returns(201)
        # Test user insert
        coll = HamUserCollection()
        user = HamUser(
            username="pgreazy",
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            password="password",
            phone_number="Number",
            birthday="21 May 1995"
        )
        assert_that(coll.insert(user, check_member=True), is_(True))
