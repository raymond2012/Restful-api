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
        Authentication.__init__(self, email, password, dev_id)
        self.gcs_products_url = self.get_base_url() + "gcsproducts"
        self.snaps_url = self.get_base_url() + "snaps"

    def get_snaps(self, param_dict={}):
        # print("Get Snaps")
        # URL: ```/snaps?filter={filter}offset={offset}&offset_id={offset_id}&limit={limit}&order={ASC|DESC}&orderby={creation|popularity}```
        if type(param_dict) is dict:
            url_param = urllib.parse.urlencode(param_dict)
            r = requests.get(self.snaps_url + "?" + url_param, headers=self.get_header_auth())
            self.print_result("get_snaps", r.status_code, r.content)
            if r.status_code == 200:
                result_list = list(map(lambda x: x["snap_id"], json.loads(r.content.decode('utf-8'))))
                return {"response": r, "list_snap_id": result_list}
            else:
                return {"response": r, "list_snap_id": []}

    def get_single_snap(self, snap_id):
        # print("Get Single Snap")
        r = requests.get(self.snaps_url + "/" + snap_id, headers=self.get_header_auth())
        self.print_result("get_single_snap", r.status_code, r.content)
        return r

    def create_snaps(self, query_dict):
        # print("Create Snaps")
        data_get = {
            "snaps": query_dict
        }
        print(self.get_header_auth_json())
        r = requests.post(self.snaps_url, headers=self.get_header_auth_json(), data=json.dumps(data_get))
        self.print_result("create_snaps", r.status_code, r.content)
        return r

    def remove_snap(self, snap_id):
        # print("Remove a snap")
        r = requests.delete(self.snaps_url + "/" + snap_id, headers=self.get_header_auth())
        self.print_result("remove_snap", r.status_code, r.content)
        return r

    def get_products_of_a_snap(self, snap_id, query_dict={}):
        # print("Get Products of a snap")
        # URL: ```/snaps/{id}/products?offset={offset}&offset_id={offset_id}&limit={limit}```
        url = self.snaps_url + "/" + snap_id + "/products?" + urllib.parse.urlencode(query_dict)
        print(url)
        if type(query_dict) is dict:
            r = requests.get(url, headers=self.get_header_auth())
            self.print_result("get_snap_products", r.status_code, r.content)
            if r.status_code == 200:
                result_list_snap_id = list(map(lambda x: x["snap_id"], json.loads(r.content.decode('utf-8'))['products']))
                result_list_snap_product_id = list(map(lambda x: x["snap_product_id"], json.loads(r.content.decode('utf-8'))['products']))
                return {"response": r, "list_snap_id": result_list_snap_id, "list_product_id": result_list_snap_product_id}
            else:
                return {"response": r, "list_snap_id": [], "list_product_id": []}

    def search_snaps(self, query_dict):
        # print("Search Snaps")
        # URL: ```/snaps/search?q={keyword}&offset={offset}&offset_id={offset_id}&limit={limit}&order={ASC|DESC}&orderby={creation|popularity}```
        if query_dict is not dict:
            url = self.snaps_url + "?" + urllib.parse.urlencode(query_dict)
            print(url)
            r = requests.get(url, headers=self.get_header_auth())
            # self.print_result("search_snaps", r.status_code, r.content)
            if r.status_code == 200:
                result_list_snap_id = list(map(lambda x: x["snap_id"], json.loads(r.content.decode('utf-8'))))
                return {"response": r, "list_snap_id": result_list_snap_id}
            else:
                return {"response": r, "list_snap_id": []}

    def get_snap_comment(self, snap_id, query_dict={}):
        # print("Get Commment of a Snap")
        # URL: ```/snaps/{id}/comment?offset={offset}&offset_id={offset_id}&limit={limit}```
        url = self.snaps_url + "/" + snap_id + "/comment?" + urllib.parse.urlencode(query_dict)
        print(url)
        r = requests.get(url, headers=self.get_header_auth())
        self.print_result("get_snap_comment", r.status_code, r.content)
        result_json = json.loads(r.content.decode('utf-8'))
        return {"response": r, "json": result_json}

    def post_comment(self, snap_id,  message):
        # print("Post a Comment")
        data_get = {"message": message}
        r = requests.post(self.snaps_url + "/" + snap_id + "/comment", headers=self.get_header_auth(),
                          data=data_get)
        self.print_result("post_comment", r.status_code, r.content)
        return r

    def collect_product_link_click(self, body_dict):
        # print("Collect Product Link Click Info")
        if type(body_dict) is dict:
            r = requests.post(self.gcs_products_url + "/click", headers=self.get_header_auth(), data=body_dict)
            self.print_result("collect_product_link_click", r.status_code, r.content)
            return r

    def get_snap_info_after_login(self, query_dict):
        # URL: /snaps/info-after-login?
        # home=snap_id:{snap_id},order:{DESC|ASC},orderby:{creation|popularity}&search=snap_id:{snap_id},order:{DESC|ASC},orderby:{creation|popularity},q:{keyword}
        if type(query_dict) is dict:
            home_url = "home=" + self.dict_query_to_string(query_dict['home']) if 'home' in query_dict.keys() is not None else ""
            search_url = "search=" + self.dict_query_to_string(query_dict['search']) if 'search' in query_dict.keys() is not None else ""
            product_url = "product=q:" + query_dict['product']['snap_id_product'] if 'product' in query_dict.keys() is not None else ""
            url = self.snaps_url + "/info-after-login?" + home_url + "&" + search_url + "&" + product_url
            print(url)
            r = requests.get(url, headers=self.get_header_auth())
            self.print_result("get_snap_info_after_login", r.status_code, r.content)
            return r

    def remove_a_snap_product(self, snap_product_id):
        r = requests.delete(self.snaps_url + "/product/" + snap_product_id, headers=self.get_header_auth())
        self.print_result("remove_a_snap_product", r.status_code, r.content)
        return r

    def get_snaps_by_snap_product_id(self, snap_product_id, query_dict={}):
        # URL: ```/snaps/product/{snap_product_id}/relatedsnaps?offset={offset}&offset_id={offset_id}&limit={limit}&order={ASC|DESC}&orderby={creation|popularity}```
        if type(query_dict) is dict:
            url = self.snaps_url + "/product/" + snap_product_id + "/relatedsnaps?" + urllib.parse.urlencode(query_dict)
            print(url)
            r = requests.get(url, headers=self.get_header_auth())
            self.print_result("get_snap_info_after_login", r.status_code, r.content)
            return r

    @staticmethod
    def dict_query_to_string(param_dict={}):
        return ",".join([f'{key}:{value}' for key, value in param_dict.items() if value])

def main():

    # snap = Snap("test3@gmail.com", "12345677", "12345")
    # snap.login()
    # snap.get_snap_info_after_login({"home=snap_id": '7623'})
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

    # with open(image_path, "rb") as image_file:
    #     encoded_string = "data:img/" + imghdr.what(image_path) + ";base64," + base64.b64encode(image_file.read()).decode('utf-8')
    # print(encoded_string)
    # print(encoded_string.decode('utf-8'))
    # snap_cre = [{
    #     "title": "Logo",
    #     "description": "python Logo",
    #     "image_name": "python",
    #     "image_body": encoded_string,
    #     "ref_id": "12345"
    # }]
    # snap.create_snaps(snap_cre)

    # snap.get_snaps()
    # search_query = {"search": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
    #                 "orderby": "creation"}
    # result = snap.search_snaps(search_query)
    # print(list(map(lambda x: x['snap_id'], json.loads(result.content.decode('utf-8')))))
    pass


main()
