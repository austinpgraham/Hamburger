from hamcrest import is_
from hamcrest import is_not
from hamcrest import has_entries
from hamcrest import assert_that
does_not = is_not

from pyramid import testing

from zope import interface

from hamburger.dataserver.dataserver.tests import DataserverTestBase

from hamburger.dataserver.dataserver.interfaces import IExternalObject

from hamburger.dataserver.dataserver.adapters import to_external_object

from hamburger.dataserver.dataserver.external import AbstractExternal


@interface.implementer(IExternalObject)
class FakeExternal(AbstractExternal):
    KEYS = [
        'test1',
        'test2',
        'test3'
    ]

    EXCLUDE = [
        'test3'
    ]

    test1 = 5
    test2 = 6
    test3 = 7


class TestExternal(DataserverTestBase):

    def test_external_objs(self):
        request = testing.DummyRequest()
        myobj = FakeExternal()
        obj = to_external_object(myobj, request)
        assert_that(obj, has_entries({
            'test1': 5,
            'test2': 6
        }))
        assert_that(obj, does_not(has_entries({
            'test3': 7
        })))
        assert_that(myobj.is_complete(), is_(True))
