import csv
from unittest import TestCase

import StringIO

from swiftstackapi import output


class TestCsvUtilizationWriter(TestCase):
    def setUp(self):
        self.test_data = {'account1': [{'start': '2013-08-31 23:30:00Z',
                                        'end': "2013-09-01 00:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0},
                                       {'start': "2013-09-01 00:30:00Z",
                                        'end': "2013-09-01 01:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0},
                                       {'start': '2013-09-01 01:30:00Z',
                                        'end': "2013-09-01 02:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0},
                                       {'start': "2013-09-01 02:30:00Z",
                                        'end': "2013-09-01 03:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0}],
                          'account2': [{'start': '2013-08-31 23:30:00Z',
                                        'end': "2013-09-01 00:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0},
                                       {'start': "2013-09-01 00:30:00Z",
                                        'end': "2013-09-01 01:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0},
                                       {'start': '2013-09-01 01:30:00Z',
                                        'end': "2013-09-01 02:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0},
                                       {'start': "2013-09-01 02:30:00Z",
                                        'end': "2013-09-01 03:30:00Z",
                                        'container_count': 5000,
                                        'object_count': 50000,
                                        'bytes_used': 500000,
                                        'pct_complete': 100.0}]}
        self.expected_csv = \
            """account,start,end,container_count,object_count,bytes_used,pct_complete\r\n""" \
            """account2,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000,100.0\r\n""" \
            """account2,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,500000,100.0\r\n""" \
            """account2,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,500000,100.0\r\n""" \
            """account2,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,500000,100.0\r\n""" \
            """account1,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000,100.0\r\n""" \
            """account1,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,500000,100.0\r\n""" \
            """account1,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,500000,100.0\r\n""" \
            """account1,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,500000,100.0\r\n"""

    def test_get_fields(self):
        writer = output.CsvUtilizationWriter(self.test_data, "fakey", "fake_fields")
        fields = writer.get_fields(self.test_data)

        expected_fields = ['account', 'start', 'end',
                           'container_count', 'object_count',
                           'bytes_used', 'pct_complete']

        self.assertItemsEqual(fields, expected_fields)

    def test_write_csv(self):
        self.maxDiff = None
        fake_csvfile = StringIO.StringIO()

        #try to force an order
        fields = ['account','start','end',
                  'container_count','object_count',
                  'bytes_used','pct_complete']

        writer = output.CsvUtilizationWriter(self.test_data, fake_csvfile, fields)
        writer.write_csv()

        self.assertMultiLineEqual(fake_csvfile.getvalue(), self.expected_csv)
