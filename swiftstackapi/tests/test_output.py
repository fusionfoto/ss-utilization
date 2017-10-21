import csv
from unittest import TestCase

import StringIO

from swiftstackapi import output


class TestCsvUtilizationWriter(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.test_data = {u'account1': {'1': [{'start': '2013-08-31 23:30:00Z',
                                               'end': "2013-09-01 00:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 500000000000,
                                               'pct_complete': 100.0},
                                              {'start': "2013-09-01 00:30:00Z",
                                               'end': "2013-09-01 01:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 1000000000000,
                                               'pct_complete': 100.0},
                                              {'start': '2013-09-01 01:30:00Z',
                                               'end': "2013-09-01 02:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 1500000000000,
                                               'pct_complete': 100.0},
                                              {'start': "2013-09-01 02:30:00Z",
                                               'end': "2013-09-01 03:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 2000000000000,
                                               'pct_complete': 100.0}],
                                        '2': [{'start': '2013-08-31 23:30:00Z',
                                               'end': "2013-09-01 00:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 500000000000,
                                               'pct_complete': 100.0},
                                              {'start': "2013-09-01 00:30:00Z",
                                               'end': "2013-09-01 01:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 1000000000000,
                                               'pct_complete': 100.0},
                                              {'start': '2013-09-01 01:30:00Z',
                                               'end': "2013-09-01 02:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 1500000000000,
                                               'pct_complete': 100.0},
                                              {'start': "2013-09-01 02:30:00Z",
                                               'end': "2013-09-01 03:30:00Z",
                                               'container_count': 5000,
                                               'object_count': 50000,
                                               'bytes_used': 2000000000000,
                                               'pct_complete': 100.0}]},
                          u'account2': {'1': [{'start': '2013-08-31 23:30:00Z',
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
            """account1,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000000000,100.0,1\r\n""" \
            """account1,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,1000000000000,100.0,1\r\n""" \
            """account1,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,1500000000000,100.0,1\r\n""" \
            """account1,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,2000000000000,100.0,1\r\n""" \
            """account1,2013-08-31 23:30:00Z,2013-09-01 00:30:00Z,5000,50000,500000000000,100.0,2\r\n""" \
            """account1,2013-09-01 00:30:00Z,2013-09-01 01:30:00Z,5000,50000,1000000000000,100.0,2\r\n""" \
            """account1,2013-09-01 01:30:00Z,2013-09-01 02:30:00Z,5000,50000,1500000000000,100.0,2\r\n""" \
            """account1,2013-09-01 02:30:00Z,2013-09-01 03:30:00Z,5000,50000,2000000000000,100.0,2\r\n"""

        self.expected_csv_filtered = \
            """account,end,bytes_used\r\n""" \
            """account2,2013-09-01 00:30:00Z,500000\r\n""" \
            """account2,2013-09-01 01:30:00Z,500000\r\n""" \
            """account2,2013-09-01 02:30:00Z,500000\r\n""" \
            """account2,2013-09-01 03:30:00Z,500000\r\n""" \
            """account2,2013-09-01 00:30:00Z,500000\r\n""" \
            """account2,2013-09-01 01:30:00Z,500000\r\n""" \
            """account2,2013-09-01 02:30:00Z,500000\r\n""" \
            """account2,2013-09-01 03:30:00Z,500000\r\n""" \
            """account1,2013-09-01 00:30:00Z,500000000000\r\n""" \
            """account1,2013-09-01 01:30:00Z,1000000000000\r\n""" \
            """account1,2013-09-01 02:30:00Z,1500000000000\r\n""" \
            """account1,2013-09-01 03:30:00Z,2000000000000\r\n""" \
            """account1,2013-09-01 00:30:00Z,500000000000\r\n""" \
            """account1,2013-09-01 01:30:00Z,1000000000000\r\n""" \
            """account1,2013-09-01 02:30:00Z,1500000000000\r\n""" \
            """account1,2013-09-01 03:30:00Z,2000000000000\r\n"""

        self.expected_summary = {'_TOTAL_BYTES': {'bytes_used': 2500001000000,
                                                  'end': '2013-09-01 03:30:00Z',
                                                  'start': '2013-08-31 23:30:00Z',
                                                  '1': 1250000500000,
                                                  '2': 1250000500000},
                                 '_TOTAL_GBYTES': {'bytes_used': 2500.001,
                                                   'end': '2013-09-01 03:30:00Z',
                                                   'start': '2013-08-31 23:30:00Z',
                                                   '1': 1250.000500000,
                                                   '2': 1250.000500000},
                                 '_TOTAL_TBYTES': {'bytes_used': 2.500001,
                                                   'end': '2013-09-01 03:30:00Z',
                                                   'start': '2013-08-31 23:30:00Z',
                                                   '1': 1.250000500000,
                                                   '2': 1.250000500000},
                                 'account2': {'start': '2013-08-31 23:30:00Z',
                                              'end': '2013-09-01 03:30:00Z',
                                              '1': 500000,
                                              '2': 500000,
                                              'bytes_used': 1000000},
                                 'account1': {'start': '2013-08-31 23:30:00Z',
                                              'end': '2013-09-01 03:30:00Z',
                                              '1': 1250000000000,
                                              '2': 1250000000000,
                                              'bytes_used': 2500000000000}}

        self.expected_summary_csv = \
            """account,start,end,1,2,bytes_used\r\n""" \
            """_TOTAL_BYTES,2013-08-31 23:30:00Z,2013-09-01 03:30:00Z,1250000500000,1250000500000,2500001000000\r\n""" \
            """_TOTAL_GBYTES,2013-08-31 23:30:00Z,2013-09-01 03:30:00Z,1250.0005,1250.0005,2500.001\r\n""" \
            """_TOTAL_TBYTES,2013-08-31 23:30:00Z,2013-09-01 03:30:00Z,1.2500005,1.2500005,2.500001\r\n""" \
            """account1,2013-08-31 23:30:00Z,2013-09-01 03:30:00Z,1250000000000,1250000000000,2500000000000\r\n""" \
            """account2,2013-08-31 23:30:00Z,2013-09-01 03:30:00Z,500000,500000,1000000\r\n"""

        self.expected_summary_csv_filtered = \
            """account,bytes_used\r\n""" \
            """_TOTAL_BYTES,2500001000000\r\n""" \
            """_TOTAL_GBYTES,2500.001\r\n""" \
            """_TOTAL_TBYTES,2.500001\r\n""" \
            """account1,2500000000000\r\n""" \
            """account2,1000000\r\n"""

    def test_get_fields(self):
        writer = output.CsvUtilizationWriter(self.test_data, "fakey", "fake_fields")
        fields = writer.get_fields(self.test_data)

        expected_fields = ['account', 'start', 'end',
                           'container_count', 'object_count',
                           'bytes_used', 'pct_complete', 'policy']

        self.assertItemsEqual(fields, expected_fields)

    def test_write_raw_csv(self):
        fake_csvfile = StringIO.StringIO()

        # try to force an order
        fields = ['account', 'start', 'end',
                  'container_count', 'object_count',
                  'bytes_used', 'pct_complete', 'policy']

        writer = output.CsvUtilizationWriter(self.test_data, fake_csvfile, fields)
        writer.write_raw_csv()

        self.assertMultiLineEqual(fake_csvfile.getvalue(), self.expected_csv)

    def test_write_raw_csv_filtered(self):
        fake_csvfile = StringIO.StringIO()

        # filter fields
        fields = ['account', 'end', 'bytes_used']

        writer = output.CsvUtilizationWriter(self.test_data, fake_csvfile,
                                             output_fields=fields)
        writer.write_raw_csv()

        self.assertMultiLineEqual(fake_csvfile.getvalue(), self.expected_csv_filtered)

    def test_summarize(self):
        writer = output.CsvUtilizationWriter(self.test_data, "fakey")

        writer.summarize()

        self.assertEqual(writer.summary, self.expected_summary)

    def test_write_summary_csv(self):
        fake_csvfile = StringIO.StringIO()

        writer = output.CsvUtilizationWriter(self.test_data, fake_csvfile)
        writer.write_summary_csv()

        self.assertMultiLineEqual(fake_csvfile.getvalue(), self.expected_summary_csv)

    def test_write_summary_csv_filtered(self):
        fake_csvfile = StringIO.StringIO()

        writer = output.CsvUtilizationWriter(self.test_data, fake_csvfile,
                                             output_fields=['account', 'bytes_used'])
        writer.write_summary_csv()

        self.assertMultiLineEqual(fake_csvfile.getvalue(), self.expected_summary_csv_filtered)