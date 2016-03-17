# -*- coding: UTF-8 -*-
import unittest
from billomat import base
from mock import Mock


FIXTURE_PARAMS_1 = {
    'foo': 'bar',
}
FIXTURE_PARAMS_2 = {
    'billo': 'mat',
}
FIXTURE_PARAMS = {
    'foo': 'bar',
    'billo': 'mat',
}


class TestQueryset(unittest.TestCase):
    def _get_object_manager(self):
        return base.ObjectManager(
            'resource',
            {},
            'foo',
            'bar',
        )

    def testFilter(self):
        objectmanager = self._get_object_manager()
        objectmanager.validate_kwargs = Mock(return_value=True)
        queryset = base.QuerySet(objectmanager)

        queryset = queryset.filter(**FIXTURE_PARAMS_1)
        self.assertEqual(queryset.params, FIXTURE_PARAMS_1)

        queryset = queryset.filter(**FIXTURE_PARAMS_2)
        self.assertEqual(queryset.params, FIXTURE_PARAMS)

    def testCount(self):
        objectmanager = self._get_object_manager()
        queryset = base.QuerySet(objectmanager)
        queryset._iterator.get_total = Mock(
            side_effect=[None, 1]
        )
        queryset._iterator.get_page = Mock()
        self.assertEqual(queryset.count(), 1)

        queryset._iterator.total = None
        queryset._iterator.get_total = Mock(return_value=2)
        self.assertEqual(queryset.count(), 2)
