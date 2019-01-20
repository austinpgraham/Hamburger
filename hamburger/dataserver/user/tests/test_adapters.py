import fudge

from hamcrest import is_not
from hamcrest import equal_to
from hamcrest import assert_that
from hamcrest import contains_inanyorder
does_not = is_not

from pyramid import testing

from pyramid.interfaces import IRequest

from zope import interface
from zope import component

from hamburger.dataserver.user.tests import UserTestBase

from hamburger.dataserver.user.model import HamUser

from hamburger.dataserver.user.interfaces import IAuthedUser
from hamburger.dataserver.user.interfaces import IPermissionCollection

from hamburger.dataserver.product.model import HamProductCollection


class TestAdapters(UserTestBase):

    def test_permission_collection(self):
        # Test owning user has all permissions
        user = HamUser(
            username="pgreazy",
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            password="password"
        )
        pc = HamProductCollection(
            title="MyTestCollection",
            is_public=True
        )
        user["MyTestCollection"] = pc
        adapter = component.queryMultiAdapter((user, pc))
        assert_that(adapter, is_not(None))
        assert_that(adapter, contains_inanyorder('edit', 'view'))

        # Test non-owner has only views if public.
        nonuser = HamUser(
            username="austin",
            first_name="Austin",
            last_name="Graham",
            email="austingraham@gmail.com",
            password="password"
        )
        adapter = component.queryMultiAdapter((nonuser, pc))
        assert_that(adapter, contains_inanyorder('view'))
        assert_that(adapter, does_not(contains_inanyorder('edit')))
