import base64
import json
import urllib
import requests

from src.Authentication import Authentication


class Snap(Authentication):

    def __init__(self, email, password, dev_id):
        Authentication.__init__(self, email, password, dev_id)
        self.login()
        self.__device_id = self.get_device_id()
        self.__token = "Bearer " + self.get_token()
        self.__id = self.get_user_id()
        self.gcsproducts_url = "http://api-dev.dress-as.com:4460/gcsproducts"
        self.snaps_url = "http://api-dev.dress-as.com:4460/snaps"

    def get_snaps(self, param_dict):
        print("Get Snaps")
        header_get = {"Authorization": self.__token}
        if type(param_dict) is dict:
            url_param = urllib.parse.urlencode(param_dict)
            url = self.snaps_url + "?" + url_param
            r = requests.get(url, headers=header_get)
            if r.content is not None:
                if r.status_code == 200:
                    response = json.loads(r.content.decode('utf-8'))
                    # for i in response:
                    #     print(i['snap_id'])
                    return response

    def get_single_snap(self, snap_id):
        print("Get Single Snap")
        header_get = {"Authorization": self.__token}
        r = requests.get(self.snaps_url + "/" + snap_id, headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                print(result)
            elif r.status_code >= 400:
                print(result['error'])

    def create_snaps(self, query_dict):
        print("Create Snaps")
        header_get = {"Authorization": self.__token}
        data_get = {'snap': query_dict}
        print(data_get)
        if type(query_dict) is list:
            r = requests.post(self.snaps_url, headers=header_get, data=data_get)
            if r.content is not None:
                result = json.loads(r.content.decode('utf-8'))
                if r.status_code == 201:
                    print(result)
                elif r.status_code >= 400:
                    print(result['error'])

    def remove_snap(self):
        print("Remove a snap")
        header_get = {"Authorization": self.__token}
        r = requests.delete(self.snaps_url + "/" + self.__id, headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                print(result)
            elif r.status_code >= 400:
                print(result['error'])

    def get_snap_products(self):
        print("Get Products of a snap")
        header_get = {"Authorization": self.__token}
        r = requests.get(self.snaps_url + "/" + self.__id + "/products", headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return result
            elif r.status_code >= 400:
                return result['error']

    def search_snaps(self, query_dict):
        print("Search Snaps")
        header_get = {"Authorization": self.__token}
        r = requests.delete(self.snaps_url + "?" + urllib.parse.urlencode(query_dict), headers=header_get)
        if r.content is not None:
            if r.status_code == 200:
                return json.loads(r.content.decode('utf-8'))

    def get_snap_comment(self, query_dict):
        print("Get Commment of a Snap")
        header_get = {"Authorization": self.__token}
        r = requests.get(self.snaps_url + "/" + self.__id + "comment?" + urllib.parse.urlencode(query_dict),
                         headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return result
            elif r.status_code >= 400:
                return result['error']

    def post_comment(self, message):
        print("Post a Comment")
        header_get = {"Authorization": self.__token}
        data_get = {"message": message}
        r = requests.post(self.snaps_url + "/" + self.__id + "/comment", headers=header_get, data=data_get)
        if r.content is not None:
            if r.status_code == 201:
                print("Post Comment Successfully")
            elif r.status_code >= 400:
                return json.loads(r.content.decode('utf-8'))


    def collect_product_link_click(self, gcs_id, body_dict):
        print("Collect Product Link Click Info")
        header_get = {"Authorization": self.__token}
        if type(body_dict) is dict:
            r = requests.post(self.gcsproducts_url + gcs_id + "/click", headers=header_get, data=body_dict)




def main():
    snap = Snap("test3@gmail.com", "12345677", "12345")

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
    # print(snap.get_snaps(query))
    # print("--------")
    # print(snap.get_snaps(query2))
    # print("--------")
    # print(snap.get_snaps(query3))

    # snap.get_single_snap("7623")


    # with open(r"C:\Users\user\Downloads\768px-Python-logo-notext.svg.png", "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())
    # snap_cre = [{
    #     "title": "Logo",
    #     "description": "python Logo",
    #     "image_name": "python",
    #     "image_body": "encoded_string",
    #     "ref_id": "12345"
    # }]
    # snap.create_snaps(snap_cre)

main()
