import csv
from unittest import TestCase

import StringIO

from swiftstackapi import output


class TestCsvUtilizationWriter(TestCase):
    def setUp(self):
        self.test_data = {'account1': {'1': [{'start': '2013-08-31 23:30:00Z',
                                              'end': "2013-09-01 00:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 500000,
                                              'pct_complete': 100.0},
                                             {'start': "2013-09-01 00:30:00Z",
                                              'end': "2013-09-01 01:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 1000000,
                                              'pct_complete': 100.0},
                                             {'start': '2013-09-01 01:30:00Z',
                                              'end': "2013-09-01 02:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 1500000,
                                              'pct_complete': 100.0},
                                             {'start': "2013-09-01 02:30:00Z",
                                              'end': "2013-09-01 03:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 2000000,
                                              'pct_complete': 100.0}],
                                       '2': [{'start': '2013-08-31 23:30:00Z',
                                              'end': "2013-09-01 00:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 500000,
                                              'pct_complete': 100.0},
                                             {'start': "2013-09-01 00:30:00Z",
                                              'end': "2013-09-01 01:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 1000000,
                                              'pct_complete': 100.0},
                                             {'start': '2013-09-01 01:30:00Z',
                                              'end': "2013-09-01 02:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 1500000,
                                              'pct_complete': 100.0},
                                             {'start': "2013-09-01 02:30:00Z",
                                              'end': "2013-09-01 03:30:00Z",
                                              'container_count': 5000,
                                              'object_count': 50000,
                                              'bytes_used': 2000000,
                                              'pct_complete': 100.0}]},
                          'account2': {'1': [{'start': '2013-08-31 23:30:00Z',
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
                                       '2': [{'start': '2013-08-31 23:30:00Z',
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
                                              'pct_complete': 100.0}]}}
        self.expected_csv = \
            """account,start,end,container_count,object_count,bytes_used,pct_complete,policy\r\n""" \
            """account2,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000,100.0,1\r\n""" \
            """account2,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,500000,100.0,1\r\n""" \
            """account2,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,500000,100.0,1\r\n""" \
            """account2,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,500000,100.0,1\r\n""" \
            """account2,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000,100.0,2\r\n""" \
            """account2,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,500000,100.0,2\r\n""" \
            """account2,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,500000,100.0,2\r\n""" \
            """account2,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,500000,100.0,2\r\n""" \
            """account1,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000,100.0,1\r\n""" \
            """account1,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,1000000,100.0,1\r\n""" \
            """account1,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,1500000,100.0,1\r\n""" \
            """account1,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,2000000,100.0,1\r\n""" \
            """account1,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000,100.0,2\r\n""" \
            """account1,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,1000000,100.0,2\r\n""" \
            """account1,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,1500000,100.0,2\r\n""" \
            """account1,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,2000000,100.0,2\r\n"""

        self.expected_summary = {'account2': {'start': '2013-08-31 23:30:00Z',
                                              'end': '2013-09-01 03:30:00Z',
                                              'bytes_used': 1000000},
                                 'account1': {'start': '2013-08-31 23:30:00Z',
                                              'end': '2013-09-01 03:30:00Z',
                                              'bytes_used': 2500000}}

        self.expected_summary_csv = \
            """account,start,end,bytes_used\r\n""" \
            """account2,2013-08-31 23:30:00Z,2013-09-01 03:30:00Z,1000000\r\n""" \
            """account1,2013-08-31 23:30:00Z,2013-09-01 03:30:00Z,2500000\r\n"""

    def test_get_fields(self):
        writer = output.CsvUtilizationWriter(self.test_data, "fakey", "fake_fields")
        fields = writer.get_fields(self.test_data)

        expected_fields = ['account', 'start', 'end',
                           'container_count', 'object_count',
                           'bytes_used', 'pct_complete', 'policy']

        self.assertItemsEqual(fields, expected_fields)

    def test_write_raw_csv(self):
        self.maxDiff = None
        fake_csvfile = StringIO.StringIO()

        # try to force an order
        fields = ['account', 'start', 'end',
                  'container_count', 'object_count',
                  'bytes_used', 'pct_complete', 'policy']

        writer = output.CsvUtilizationWriter(self.test_data, fake_csvfile, fields)
        writer.write_raw_csv()

        self.assertMultiLineEqual(fake_csvfile.getvalue(), self.expected_csv)

    def test_summarize(self):
        writer = output.CsvUtilizationWriter(self.test_data, "fakey")

        rval = writer.summarize()

        self.assertEqual(rval, self.expected_summary)

    def test_write_summary_csv(self):
        self.maxDiff = None
        fake_csvfile = StringIO.StringIO()

        writer = output.CsvUtilizationWriter(self.test_data, fake_csvfile)
        writer.write_summary_csv()

        self.assertMultiLineEqual(fake_csvfile.getvalue(), self.expected_summary_csv)