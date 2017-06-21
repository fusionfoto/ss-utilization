from datetime import datetime
from unittest import TestCase

from swiftstackapi import cli


class TestTimestamp(TestCase):
    def test_good_timestamp(self):
        good_date_tz = '2013-08-29T19:24:44-0700'
        good_date_offset = '2013-08-29T12:24:44'
        good_date_naive = '2013-08-29T19:24:44'
        self.assertEquals(datetime.strptime(good_date_offset, cli.DTF_ISO8601),
                          cli.timestamp(good_date_tz))
        self.assertEquals(datetime.strptime(good_date_naive, cli.DTF_ISO8601),
                          cli.timestamp(good_date_naive))

    def test_bad_timestatmp(self):
        bad_date_tz = '2013-08-29T19:24:44 -0700'
        bad_date_naive = '213-08-29T19:24:44'
        garbage = 'floofloofloo'
        self.assertRaises(ValueError, cli.timestamp, bad_date_tz)
        self.assertRaises(ValueError, cli.timestamp, bad_date_naive)
        self.assertRaises(ValueError, cli.timestamp, garbage)

