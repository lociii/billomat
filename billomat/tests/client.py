# -*- coding: UTF-8 -*-
import json
import unittest
from httmock import all_requests, HTTMock, response
from billomat import base


FIXTURE_MESSAGE = 'ERRORMESSAGE'
FIXTURE_OBJECT = {'a': 'b'}


@all_requests
def billomat_mock_exception(url, request):
    raise BaseException('Failed')


@all_requests
def billomat_mock_return_empty(url, request):
    return response(200, '')


@all_requests
def billomat_mock_return_none(url, request):
    return response(200, json.dumps(None))


@all_requests
def billomat_mock_return_error(url, request):
    return response(200, json.dumps({
        'errors': {
            'error': FIXTURE_MESSAGE,
        }
    }))


@all_requests
def billomat_mock_return_malformed(url, request):
    return response(200, 'fdsf4{{D,dew')


@all_requests
def billomat_mock_ok(url, request):
    return response(200, json.dumps(FIXTURE_OBJECT))


class TestClient(unittest.TestCase):
    def testQueryThrowsException(self):
        with HTTMock(billomat_mock_exception):
            client = base.Client()
            self.assertRaisesRegexp(
                base.BillomatRequestException,
                'request failed.*',
                client.query,
                ('test', ),
            )

    def testQueryReturnsEmptyList(self):
        with HTTMock(billomat_mock_return_empty):
            client = base.Client()
            result = client.query('test')
            self.assertEqual(result, {})

    def testQueryThrowsExceptionOnNoneResponse(self):
        with HTTMock(billomat_mock_return_none):
            client = base.Client()
            self.assertRaisesRegexp(
                base.BillomatRequestException,
                'null.*',
                client.query,
                ('test', ),
            )

    def testQueryThrowsExceptionWithMessage(self):
        with HTTMock(billomat_mock_return_error):
            client = base.Client()
            self.assertRaisesRegexp(
                base.BillomatRequestException,
                FIXTURE_MESSAGE,
                client.query,
                ('test', ),
            )

    def testQueryThrowsExceptionOnInvalidResponse(self):
        with HTTMock(billomat_mock_return_malformed):
            client = base.Client()
            self.assertRaisesRegexp(
                base.BillomatRequestException,
                'malformed.*',
                client.query,
                ('test', ),
            )

    def testQueryOk(self):
        with HTTMock(billomat_mock_ok):
            client = base.Client()
            result = client.query('test')
            self.assertEqual(result, FIXTURE_OBJECT)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
