import requests

RESP_LIMIT = 500


class SwiftStackAPIClient(object):
    def __init__(self, controller, apiuser, apikey):
        self.endpoint = "https://" + controller + "/api/v1/"
        self.apiuser = apiuser
        self.apikey = apikey
        self.session = requests.Session()
        headers = {'Authorization':
                       'apikey %s:%s' % (self.apiuser, self.apikey)}

        self.session.headers.update(headers)

    def request(self, method="", path="", params=None):
        VERB_MAP = {
            'GET': self.session.get,
            'PUT': self.session.put,
            'HEAD': self.session.head,
            'POST': self.session.post
        }
        params['limit'] = RESP_LIMIT
        r = VERB_MAP[method.upper()](self.endpoint + path, params=params)
        return r.json()

    def get(self, path="", params=None):
        return self.request(method='get', path=path, params=params)

    def paginated_get(self, path="", params=None):
        offset = 0
        params['offset'] = offset
        result = self.get(path=path, params=params)
        while result['meta']['next']:
            params['offset'] += + RESP_LIMIT
            next_result = self.get(path=path, params=params)
            result['meta'] = next_result['meta']
            result['objects'].extend(next_result['objects'])

        return result

    # TODO handle datetime objects properly here
    def get_accounts(self, cluster, start_time, end_time, policy):
        acct_path = "clusters/%s/utilization/storage/%s/" % (cluster, policy)
        params = {"start": start_time, "end": end_time}
        storage_util = self.paginated_get(path=acct_path, params=params)
        return [ item['account'] for item in storage_util['objects'] ]

    def get_acct_util(self, cluster, account, start_time, end_time, policy):
        util_detail_path = "clusters/%s/utilization/storage/%s/%s/detail/" % (cluster, policy, account)
        params = {'start': start_time, 'end': end_time}
        acct_hourly_util = self.paginated_get(path=util_detail_path, params=params)
        return [ item for item in acct_hourly_util['objects'] ]
