# Copyright 2018 SwiftStack, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from datetime import datetime
from unittest import TestCase

import swiftstackapi.api
from swiftstackapi import cli


class TestTimestamp(TestCase):
    def test_good_timestamp(self):
        good_date_tz = '2013-08-29T19:24:44-0700'
        good_date_offset = '2013-08-29T12:24:44'
        good_date_naive = '2013-08-29T19:24:44'
        self.assertEquals(datetime.strptime(good_date_offset, swiftstackapi.api.DTF_ISO8601),
                          cli.timestamp(good_date_tz))
        self.assertEquals(datetime.strptime(good_date_naive, swiftstackapi.api.DTF_ISO8601),
                          cli.timestamp(good_date_naive))

    def test_bad_timestatmp(self):
        bad_date_tz = '2013-08-29T19:24:44 -0700'
        bad_date_naive = '213-08-29T19:24:44'
        garbage = 'floofloofloo'
        self.assertRaises(ValueError, cli.timestamp, bad_date_tz)
        self.assertRaises(ValueError, cli.timestamp, bad_date_naive)
        self.assertRaises(ValueError, cli.timestamp, garbage)

