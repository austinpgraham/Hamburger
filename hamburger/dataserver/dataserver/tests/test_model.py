from hamcrest import is_
from hamcrest import assert_that
from hamcrest import has_property

from hamburger.dataserver.dataserver.tests import DataserverTestBase

from hamburger.dataserver.dataserver.model import Contained
from hamburger.dataserver.dataserver.model import Collection


class FakeContained(Contained):
    __key__ = 'test'

    def __init__(self, val):
        self.test = val


class FakeCollection(Collection):
    pass


class TestModel(DataserverTestBase):

    def test_model(self):
        # Test contained object
        first_obj = FakeContained(7)
        assert_that(first_obj.get_key(), is_(7))
        # Test Collection
        mycoll = FakeCollection()
        assert_that(mycoll.insert(first_obj, check_member=True), is_(True))
        assert_that(mycoll.insert(first_obj, check_member=True, update_on_found=False), is_(False))
        first_obj.new_val = 'new_val'
        assert_that(mycoll.insert(first_obj, check_member=True), is_(True))
        assert_that(mycoll[7], has_property('new_val'))
