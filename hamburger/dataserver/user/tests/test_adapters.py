import fudge

from hamcrest import is_
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

    @fudge.patch("hamburger.dataserver.user.model.HamUser._simon_create")
    def test_permission_collection(self, _sc):
        # Test owning user has all permissions
        _sc.is_callable().returns((201, None))
        user = HamUser(
            username="pgreazy",
            first_name="Austin",
            last_name="Graham",
            email="austingraham731@gmail.com",
            password="password",
            birthday="21 May 1995"
        )
        pc = HamProductCollection(
            title="MyTestCollection",
            is_public=True
        )
        user["MyTestCollection"] = pc
        adapter = component.queryMultiAdapter((user, pc), IPermissionCollection)
        assert_that(adapter, is_not(None))
        assert_that(adapter, contains_inanyorder('edit', 'view'))

        # Test non-owner has only views if public.
        nonuser = HamUser(
            username="austin",
            first_name="Austin",
            last_name="Graham",
            email="austingraham",
            password="password",
            birthday="21 May 1995"
        )
        adapter = component.queryMultiAdapter((nonuser, pc))
        assert_that(adapter, contains_inanyorder('view'))
        assert_that(adapter, does_not(contains_inanyorder('edit')))
