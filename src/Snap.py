import base64
import json
import urllib
import requests

from src.Authentication import Authentication


def check_token(func):
    def inner(self, *args, **kwargs):
        if self.get_token is None:
            raise ValueError
        else:
            return func(self, *args, **kwargs)

    return inner


class Snap(Authentication):

    def __init__(self, email="", password="", dev_id=""):
        if email and password is not None:
            Authentication.__init__(self, email, password, dev_id)
            self.login()
            self.__device_id = self.get_device_id()
            self.__token = "Bearer " + self.get_token()
            self.__id = self.get_user_id()
            self.__header_auth = {"Authorization": self.__token}
            self.gcs_products_url = "http://api-dev.dress-as.com:4460/gcsproducts"
            self.snaps_url = "http://api-dev.dress-as.com:4460/snaps"
        else:
            print("No email and password")

    def get_snaps(self, param_dict):
        print("Get Snaps")
        if type(param_dict) is dict:
            url_param = urllib.parse.urlencode(param_dict)
            r = requests.get(self.snaps_url + "?" + url_param, headers=self.__header_auth)
            self.print_result("get_snaps", r.status_code, r.content)
            return r

    def get_single_snap(self, snap_id):
        print("Get Single Snap")
        r = requests.get(self.snaps_url + "/" + snap_id, headers=self.__header_auth)
        self.print_result("get_single_snap", r.status_code, r.content)
        return r

    @check_token
    def create_snaps(self, query_dict):
        print("Create Snaps")
        data_get = {'snap': query_dict}
        if type(query_dict) is list:
            r = requests.post(self.snaps_url, headers=self.__header_auth, data=data_get)
            self.print_result("create_snaps", r.status_code, r.content)
            return r
        else:
            print("The type of query_dict is incorrect")
            return

    def remove_snap(self):
        print("Remove a snap")
        r = requests.delete(self.snaps_url + "/" + self.__id, headers=self.__header_auth)
        self.print_result("remove_snap", r.status_code, r.content)
        return r

    def get_products_of_a_snap(self):
        print("Get Products of a snap")
        r = requests.get(self.snaps_url + "/" + self.__id + "/products", headers=self.__header_auth)
        self.print_result("get_snap_products", r.status_code, r.content)
        return r

    def search_snaps(self, query_dict):
        print("Search Snaps")
        if query_dict is not dict:
            r = requests.delete(self.snaps_url + "?" + urllib.parse.urlencode(query_dict), headers=self.__header_auth)
            self.print_result("search_snaps", r.status_code, r.content)
            return r

    def get_snap_comment(self, query_dict):
        print("Get Commment of a Snap")
        r = requests.get(self.snaps_url + "/" + self.__id + "comment?" + urllib.parse.urlencode(query_dict),
                         headers=self.__header_auth)
        self.print_result("get_snap_comment", r.status_code, r.content)

    def post_comment(self, message):
        print("Post a Comment")
        data_get = {"message": message}
        r = requests.post(self.snaps_url + "/" + self.__id + "/comment", headers=self.__header_auth, data=data_get)
        self.print_result("post_comment", r.status_code, r.content)

    def collect_product_link_click(self, gcs_id, body_dict):
        print("Collect Product Link Click Info")
        if type(body_dict) is dict:
            r = requests.post(self.gcs_products_url + gcs_id + "/click", headers=self.__header_auth, data=body_dict)
            self.print_result("post_comment", r.status_code, r.content)
            return r


def main():
    # query = {
    #     "filter": "",
    #     "offset": "",
    #     "offset_id": "",
    #     "limit": "5",
    #     "order": "DESC",
    #     "orderby": "creation"
    # }
    # query2 = {
    #     "filter": "",
    #     "offset": "",
    #     "offset_id": "7516",
    #     "limit": "5",
    #     "order": "DESC",
    #     "orderby": "creation"
    # }
    # query3 = {
    #     "filter": "",
    #     "offset": "",
    #     "offset_id": "",
    #     "limit": "10",
    #     "order": "DESC",
    #     "orderby": "creation"
    # }
    # Snap().get_snaps(query)
    # snap.get_single_snap("7623")

    # with open(r"C:\Users\user\Downloads\768px-Python-logo-notext.svg.png", "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())
    snap = Snap("test3@gmail.com", "12345678", "12345")
    snap_cre = [{
        "title": "Logo",
        "description": "python Logo",
        "image_name": "python",
        "image_body": "encoded_string",
        "ref_id": "12345"
    }]
    snap.create_snaps(snap_cre)
    pass


main()
