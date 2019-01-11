from hamcrest import is_
from hamcrest import is_not
from hamcrest import has_key
from hamcrest import has_length
from hamcrest import has_entries
from hamcrest import assert_that
does_not = is_not

from pyramid import testing

from zope import interface

from hamburger.dataserver.dataserver.tests import DataserverTestBase

from hamburger.dataserver.dataserver.interfaces import IExternalObject

from hamburger.dataserver.dataserver.adapters import to_external_object

from hamburger.dataserver.dataserver.external import AbstractExternal
from hamburger.dataserver.dataserver.external import ExternalPersistent
from hamburger.dataserver.dataserver.external import ExternalPersistentMapping


@interface.implementer(IExternalObject)
class FakeExternal(ExternalPersistent):
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


class FakeExternalMapping(ExternalPersistentMapping):
    pass


class TestExternal(DataserverTestBase):

    def test_external_objs(self):
        # Test externalization of object
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

        # Test object external update
        obj['test1'] = 7
        myobj.update_from_external(obj, request)
        assert_that(myobj.test1, is_(7))

        # New object from json:
        new_obj = FakeExternal.from_json(obj)
        assert_that(obj, has_entries({
            'test1': 7,
            'test2': 6
        }))

    def test_external_mapping(self):
        # Test externalization of persistent mapping
        mapping = FakeExternalMapping()
        request = testing.DummyRequest()
        mapping['test1'] = FakeExternal()
        mapping['test2'] = FakeExternal()
        obj = to_external_object(mapping, request)
        assert_that(obj, has_entries({
            'items': has_length(2)
        }))
        assert_that(obj['items'], has_key('test1'))
        assert_that(obj['items'], has_key('test2'))
