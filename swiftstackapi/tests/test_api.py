from unittest import TestCase
from mock import Mock, patch

from swiftstackapi import cli
from swiftstackapi.api import SwiftStackAPIClient, RESP_LIMIT


class TestSwiftStackAPIClient(TestCase):
    def setUp(self):
        mock_session_patcher = patch('swiftstackapi.api.requests.Session')
        self.mock_session = mock_session_patcher.start()
        self.mock_session_obj = Mock()
        self.mock_response_obj = Mock()
        self.mock_session_obj.get.return_value = self.mock_response_obj
        self.mock_session.return_value = self.mock_session_obj

        self.client = SwiftStackAPIClient('controller', 'myuser', 'mykey')

    def tearDown(self):
        self.mock_session.stop()

    def test_request(self):
        get_response = {'thing': ['one', 'two'], 'otherthing': 'value'}
        self.mock_response_obj.json.return_value = get_response

        rval = self.client.request(method='gEt', path='a/fake/path', params={'zero': 0, 'one': 1})

        self.mock_session_obj.get.assert_called_with('https://controller/api/v1/a/fake/path',
                                                     params={'zero': 0, 'one': 1, 'limit': RESP_LIMIT})
        self.assertEqual(rval, get_response)

    def test_get(self):
        get_response = {'meta': ['one', 'two'], 'objects': [{'name': 'itemA',
                                                             'param': 'value',
                                                             'otherparam': 'value2'},
                                                            {'name': 'itemB',
                                                             'param': 'value',
                                                             'otherparam': 'value3'}]}
        self.mock_response_obj.json.return_value = get_response

        rval = self.client.get(path='a/fake/path', params={'zero': 0, 'one': 1})

        self.mock_session_obj.get.assert_called_with('https://controller/api/v1/a/fake/path',
                                                      params={'zero': 0, 'one': 1,
                                                              'limit': RESP_LIMIT})
        self.assertEqual(rval, get_response)

    def test_paginated_get(self):
        self.maxDiff = None
        get_response_1 = {'meta': {'next': 'some_url'},
                          'objects': [{'name': 'itemA',
                                       'param': 'value',
                                       'otherparam': 'value1'},
                                      {'name': 'itemB',
                                       'param': 'value',
                                       'otherparam': 'value2'}]}
        get_response_2 = {'meta': {'next': 'some_url'},
                          'objects': [{'name': 'itemC',
                                       'param': 'value',
                                       'otherparam': 'value3'},
                                      {'name': 'itemD',
                                       'param': 'value',
                                       'otherparam': 'value4'}]}
        get_response_3 = {'meta': {'next': None},
                          'objects': [{'name': 'itemE',
                                       'param': 'value',
                                       'otherparam': 'value5'},
                                      {'name': 'itemF',
                                       'param': 'value',
                                       'otherparam': 'value6'}]}
        response_list = [get_response_1, get_response_2, get_response_3]
        self.mock_response_obj.json.side_effect = response_list

        expected_rval = {'meta': {'next': None},
                         'objects': get_response_1['objects']
                                    + get_response_2['objects']
                                    + get_response_3['objects']}

        rval = self.client.paginated_get(path='a/fake/path', params={'zero': 0, 'one': 1})

        self.assertEqual(self.mock_session_obj.get.call_count, 3)
        self.assertEqual(rval, expected_rval)

    def test_get_accounts(self):
        self.maxDiff = None
        get_response_1 = {'meta': {'next': 'some_url'},
                          'objects': [{'account': 'accountA',
                                       'param': 'value',
                                       'otherparam': 'value3'},
                                      {'account': 'accountB',
                                       'param': 'value',
                                       'otherparam': 'value4'}]}
        get_response_2 = {'meta': {'next': None},
                          'objects': [{'account': 'accountC',
                                       'param': 'value',
                                       'otherparam': 'value5'},
                                      {'account': 'accountD',
                                       'param': 'value',
                                       'otherparam': 'value6'}]}

        response_list = [get_response_1, get_response_2]
        self.mock_response_obj.json.side_effect = response_list

        expected_rval = [item['account'] for item in get_response_1['objects']] + \
                        [item['account'] for item in get_response_2['objects']]
        expected_url = 'https://controller/api/v1/clusters/1234/utilization/storage/1/'

        date_a = cli.timestamp('2000-01-01T00:00:00')
        date_b = cli.timestamp('2000-01-02T00:00:00')
        rval = self.client.get_accounts(1234, date_a, date_b, 1)

        self.assertEqual(rval, expected_rval)
        self.mock_session_obj.get.assert_called_with(expected_url,
                                                     params={'start': '2000-01-01T00:00:00',
                                                             'end': '2000-01-02T00:00:00',
                                                             'limit': 1000,
                                                             'offset': 1000})
        self.assertEqual(self.mock_session_obj.get.call_count, 2)

    def test_get_acct_util(self):
        self.maxDiff = None

        get_response_1 = {'meta': {'next': 'some_url'},
                          'objects': [{'start': '2013-08-31 23:30:00Z',
                                       'end': "2013-09-01 00:30:00Z",
                                       'container_count': 5000,
                                       'object_count': 50000,
                                       'bytes_used': 500000,
                                       'pct_complete': 100.0},
                                      {'start': "2013-09-01 00:30:00Z",
                                       'end': "2013-09-01 01:30:00Z",
                                       'container_count': 5200,
                                       'object_count': 52000,
                                       'bytes_used': 520000,
                                       'pct_complete': 100.0}]}

        get_response_2 = {'meta': {'next': None},
                          'objects': [{'start': '2013-09-01 01:30:00Z',
                                       'end': "2013-09-01 02:30:00Z",
                                       'container_count': 5000,
                                       'object_count': 50000,
                                       'bytes_used': 500000,
                                       'pct_complete': 100.0},
                                      {'start': "2013-09-01 02:30:00Z",
                                       'end': "2013-09-01 03:30:00Z",
                                       'container_count': 5200,
                                       'object_count': 52000,
                                       'bytes_used': 520000,
                                       'pct_complete': 100.0}]}

        response_list = [get_response_1, get_response_2]
        self.mock_response_obj.json.side_effect = response_list

        expected_rval = get_response_1['objects'] + get_response_2['objects']
        expected_url = 'https://controller/api/v1/clusters/1234/utilization/storage/1/AUTH_bob/detail/'

        date_a = cli.timestamp('2000-01-01T00:00:00')
        date_b = cli.timestamp('2000-01-02T00:00:00')
        rval = self.client.get_acct_util(1234, 'AUTH_bob', date_a, date_b, 1)

        self.assertEqual(rval, expected_rval)
        self.mock_session_obj.get.assert_called_with(expected_url,
                                                     params={'start': '2000-01-01T00:00:00',
                                                             'end': '2000-01-02T00:00:00',
                                                             'limit': 1000,
                                                             'offset': 1000})
        self.assertEqual(self.mock_session_obj.get.call_count, 2)
