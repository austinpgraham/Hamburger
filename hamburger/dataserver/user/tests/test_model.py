from hamcrest import is_
from hamcrest import is_not
from hamcrest import has_entries
from hamcrest import assert_that
does_not = is_not

from pyramid import testing

from hamburger.dataserver.user.tests import UserTestBase

from hamburger.dataserver.user.model import HamUser
from hamburger.dataserver.user.model import HamGoogleUser
from hamburger.dataserver.user.model import HamFacebookUser
from hamburger.dataserver.user.model import HamUserCollection

from hamburger.dataserver.product.model import HamProductCollection


class TestUserModel(UserTestBase):

    def test_user(self):
        # Test that a user creates correctly
        user = HamUser(
            username="pgreazy",
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            password="password",
            phone_number="number"
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

    def test_user_collection(self):
        # Test user insert
        coll = HamUserCollection()
        user = HamUser(
            username="pgreazy",
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            password="password",
            phone_number="Number"
        )
        assert_that(coll.insert(user, check_member=True), is_(True))

    def test_oauth_users(self):
        access_token = {'name': "Test Token", 'exp_date': 1}
        # Test Google User
        user = HamGoogleUser(
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            phone_number="Number",
            access_token=access_token
        )
        assert_that(user.username, is_("austingraham731@gmail.com"))
        assert_that(user.access_token, is_(access_token))

        # Do the same for Facebook user, although in the future'
        # this test might need to change
        user = HamFacebookUser(
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            phone_number="Number",
            access_token=access_token
        )
        assert_that(user.username, is_("austingraham731@gmail.com"))
        assert_that(user.access_token, is_(access_token))

        # Test check auth
        assert_that(user.check_auth(), is_(None))
