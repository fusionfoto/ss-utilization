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


import logging

import requests

RESP_LIMIT = 1000
DTF_ISO8601 = "%Y-%m-%dT%H:%M:%S"

logger = logging.getLogger(__name__)


class SwiftStackAPIClient(object):
    def __init__(self, controller, apiuser, apikey):
        self.endpoint = "https://" + controller + "/api/v1/"
        self.apiuser = apiuser
        self.apikey = apikey
        self.session = requests.Session()
        headers = {'Authorization': 'apikey %s:%s' % (self.apiuser, self.apikey)}

        self.session.headers.update(headers)
        logger.debug("Initialized SwiftStackAPIClient")

    def request(self, method, path="", params={}):
        quoted_path = requests.utils.quote(path)
        verb_map = {
            'GET': self.session.get,
            'PUT': self.session.put,
            'HEAD': self.session.head,
            'POST': self.session.post
        }
        params['limit'] = RESP_LIMIT
        logger.debug("request %s %s, (%s)" % (method, quoted_path, params))
        r = verb_map[method.upper()](self.endpoint + quoted_path, params=params)
        return r.json()

    def get(self, path="", params=None):
        return self.request(method='get', path=path, params=params)

    def paginated_get(self, path="", params=None):
        offset = 0
        params['offset'] = offset
        result = self.get(path=path, params=params)
        while result['meta']['next']:
            params['offset'] += RESP_LIMIT
            next_result = self.get(path=path, params=params)
            result['meta'] = next_result['meta']
            result['objects'].extend(next_result['objects'])

        return result

    def _datetime_str(self, datetimeobj):
        return datetimeobj.strftime(DTF_ISO8601)

    def get_accounts(self, cluster, start_time, end_time, policy):
        start_timestamp = self._datetime_str(start_time)
        end_timestamp = self._datetime_str(end_time)
        acct_path = "clusters/%s/utilization/storage/%s/" % (cluster, policy)
        params = {"start": start_timestamp, "end": end_timestamp}
        storage_util = self.paginated_get(path=acct_path, params=params)
        items = [item['account'] for item in storage_util['objects']]
        logger.debug("get_accounts: (%d) accounts - %s" % (len(items), items))
        return items

    def get_acct_util(self, cluster, account, start_time, end_time, policy):
        start_timestamp = self._datetime_str(start_time)
        end_timestamp = self._datetime_str(end_time)
        util_detail_path = "clusters/%s/utilization/storage/%s/%s/detail/" % (cluster,
                                                                              policy,
                                                                              account)
        params = {'start': start_timestamp, 'end': end_timestamp}
        acct_hourly_util = self.paginated_get(path=util_detail_path, params=params)
        records = [item for item in acct_hourly_util['objects']]
        logger.debug("get_acct_util: (%d) records" % len(records))
        return records
