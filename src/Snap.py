import json
import urllib
import requests

from src.Authentication import Authentication

class Snap(Authentication):

    def __init__(self, email, password, dev_id):
        Authentication.__init__(email, password, dev_id)
        self.login()
        self.__device_id = self.get_device_id()
        self.__token = self.get_token()
        self.__id = self.get_user_id()
        self.base_url = "http://api-dev.dress-as.com:4460/snaps"

    def get_snaps(self, param_dict):
        print("Get Snaps")
        header_get = {"Authorization": "Bearer " + self.__token}
        if type(param_dict) is not dict:
            url_param = urllib.parse.urlencode(param_dict)
            r = requests.get(self.base_url + "?" + url_param, headers=header_get)
            if r.content is not None:
                if r.status_code == 200:
                    return json.loads(r.content.decode('utf-8'))

    def get_single_snap(self, snap_id):
        print("Get Single Snap")
        header_get = {"Authorization": "Bearer " + self.__token}
        r = requests.get(self.base_url + "/" + snap_id, headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return result
            elif r.status_code >= 400:
                return result['error']

    def create_snaps(self, snap_dict):
        print("Create Snaps")
        header_get = {"Authorization": "Bearer " + self.__token}
        if type(snap_dict) is dict:
            r = requests.post(self.base_url, headers=header_get, data=snap_dict)
            if r.content is not None:
                result = json.load(r.content.decode('utf-8'))
                if r.status_code == 200:
                    return result
                elif r.status_code >= 400:
                    return result['error']

    def remove_snap(self):
        print("Remove a snap")
        header_get = {"Authorization": "Bearer " + self.__token}
        r = requests.delete(self.base_url + "/" + self.__id, headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return result
            elif r.status_code >= 400:
                return result['error']

    def get_products_snap(self):
        print("Get Products of a snap")
        header_get = {"Authorization": "Bearer " + self.__token}
        r = requests.get(self.base_url + "/" + self.__id + "/products", headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return result
            elif r.status_code >= 400:
                return result['error']

