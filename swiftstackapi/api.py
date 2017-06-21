import requests


class SwiftStackAPIClient(object):
    def __init__(self, controller, apiuser, apikey):
        self.endpoint = "https://" + controller + "/api/v1/"
        self.apiuser = apiuser
        self.apikey = apikey

    def request(self, method=requests.get, path=""):
        headers = {'Authorization':
                       'apikey %s:%s' % (self.apiuser, self.apikey)}
        r = method(self.endpoint + path, headers=headers)
        return r.json()

    def get(self, path=""):
        return self.request(method=requests.get, path=path)
