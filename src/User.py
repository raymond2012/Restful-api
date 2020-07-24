import base64
import imghdr
import urllib

import requests
import json
import pytest
import datetime

from src.Authentication import Authentication
from src.Miscellaneous import Miscellaneous
from src.Snap import Snap


def check_token(func):
    def inner(self, *args, **kwargs):
        if self.get_token() is None:
            raise ValueError
        else:
            return func(self, *args, **kwargs)

    return inner


class User(Snap, Miscellaneous):

    def __init__(self, email="", password="", dev_id=""):
        Snap.__init__(self, email, password, dev_id)
        Miscellaneous.__init__(self)
        self.user_url = "http://api-dev.dress-as.com:4460/users/"

    ###Users###
    def get_user(self, user_id):
        # print("Get User Profile")
        r = requests.get(self.user_url + user_id + "/profile")
        self.print_result("get_user_profile", r.status_code, r.content)
        return r

    def change_password(self, curr, new, user_id):
        # print("Change password")
        data_get = {
            "curr_password": curr,
            "new_password": new,
            "device_id": self.get_device_id()
        }
        r = requests.post(self.user_url + user_id + "/password", headers=self.get_header_auth(),
                          data=data_get)
        self.print_result("change_password", r.status_code, r.content)
        return r

    def update_user(self, user_id, edit_profile):
        # print("Update User Profile")
        r = requests.patch(self.user_url + user_id + "/profile", headers=self.get_header_auth(), data=edit_profile)
        self.print_result("update_user_profile", r.status_code, r.content)
        return r

    def upload_user_profile_pic(self, user_id, name, body):
        # print("upload User Profile Pic")
        data_get = {
            "image_name": name,
            "image_body": body
        }
        r = requests.post(self.user_url + user_id + "/propic", headers=self.get_header_auth(), data=data_get)
        self.print_result("upload_user_profile_pic", r.status_code, r.content)
        return r

    def remove_user_profile_pic(self, user_id):
        # print("Delete User Profile Pic")
        r = requests.delete(self.user_url + user_id + "/propic", headers=self.get_header_auth())
        self.print_result("delete_user_profile_pic", r.status_code, r.content)
        return r

    def count_user_follower_and_following(self):
        r = requests.get(self.user_url + self.get_user_id() + "/follow/count")
        self.print_result("count_user_follower_and_following", r.status_code, r.content)
        return r

    def get_follower(self, user_id):
        # print("Get Follower")
        url = self.user_url + user_id + "/follower"
        print(url)
        r = requests.get(url, headers=self.get_header_auth())
        self.print_result("get_follower", r.status_code, r.content)
        return r

    def get_following(self,user_id):
        # print("Get Following")
        url = self.user_url + user_id + "/following"
        print(url)
        r = requests.get(url, headers=self.get_header_auth())
        self.print_result("get_following", r.status_code, r.content)
        return r

    def follow_user(self, user_id, target_user_id):
        # print("Follow a User")
        url = self.user_url + user_id + "/follow/" + target_user_id
        print(url)
        r = requests.post(url, headers=self.get_header_auth())
        self.print_result("follow_user", r.status_code, r.content)
        return r

    def unfollow_user(self, user_id, target_user_id):
        # print("Unfollow a User")
        url = self.user_url + user_id + "/follow/" + target_user_id
        r = requests.delete(url, headers=self.get_header_auth())
        self.print_result("unfollow_user", r.status_code, r.content)
        return r

    def get_favourite_snaps(self, user_id, param_dict={}):
        # print("Get Favourite Snaps")
        if type(param_dict) is dict:
            url_param = urllib.parse.urlencode(param_dict)
            r = requests.get(self.user_url + user_id + "/favourite/snap?" + url_param, headers=self.get_header_auth())
            self.print_result("get_favourite_snaps", r.status_code, r.content)
            if r.status_code == 200:
                result_list = list(map(lambda x: x["snap_id"], json.loads(r.content.decode('utf-8'))))
                return {"response": r, "snap_id_list": result_list}
            else:
                return {'response': r, "snap_id_list": []}

    def add_snap_to_favourite(self, user_id, snap_id):
        # print("Add a Snap to Favourite")
        url = self.user_url + user_id + "/favourite/snap/" + snap_id
        print(url)
        r = requests.post(url, headers=self.get_header_auth())
        self.print_result("add_snap_to_favourite", r.status_code, r.content)
        return r

    def remove_snap_from_favourite(self, user_id, snap_id):
        # print("Delete a Snap from Favourite")
        url = self.user_url + user_id + "/favourite/snap/" + snap_id
        r = requests.delete(url, headers=self.get_header_auth())
        self.print_result("remove_snap_from_favourite", r.status_code, r.content)
        return r

    def get_favourite_products(self, user_id, param_dict={}):
        # print("Get Favourite Products")
        if type(param_dict) is dict:
            r = requests.get(self.user_url + user_id + "/favourite/product?" + urllib.parse.urlencode(param_dict), headers=self.get_header_auth())
            self.print_result("get_favourite_products", r.status_code, r.content)
            if r.status_code == 200:
                result_list = list(map(lambda x: x["snap_product_id"], json.loads(r.content.decode('utf-8'))))
                return {"response": r, "snap_product_id_list": result_list}
            else:
                return {'response': r, "snap_product_id_list": []}

    def add_snap_product_to_favourite(self, user_id, prod_id):
        # print("Add a Product to Favourite")
        r = requests.post(self.user_url + user_id + "/favourite/product/" + prod_id, headers=self.get_header_auth())
        self.print_result("add_snap_product_to_favourite", r.status_code, r.content)
        return r

    def remove_snap_product_to_favourite(self, user_id, prod_id):
        # print("Add a Product to Favourite")
        r = requests.delete(self.user_url + user_id + "/favourite/product/" + prod_id, headers=self.get_header_auth())
        self.print_result("remove_snap_product_to_favourite", r.status_code, r.content)
        return r

    def get_user_snaps_of_a_user(self, user_id, param_dict={}):
        # print("Get Snaps of a user")
        if type(param_dict) is dict:
            url = self.user_url + user_id + "/snaps?" + urllib.parse.urlencode(param_dict)
            r = requests.get(url, headers=self.get_header_auth())
            # self.print_result("get_user_snap", r.status_code, r.content)
            if r.status_code == 200:
                result_list_user_id = list(map(lambda x: x["user_id"], json.loads(r.content.decode('utf-8'))))
                result_list_snap_id = list(map(lambda x: x["snap_id"], json.loads(r.content.decode('utf-8'))))
                return {"response": r, "list_user_id": result_list_user_id, "list_snap_id": result_list_snap_id}
            else:
                return {"response": r, "list_user_id": [], "list_snap_id": []}

    def search_user(self, keyword):
        # print("Search User")
        r = requests.get(self.user_url + "search?q=" + keyword, headers=self.get_header_auth())
        self.print_result("search_user", r.status_code, r.content)
        if r.status_code == 200:
            result_list = list(map(lambda x: x["username"], json.loads(r.content.decode('utf-8'))))
            return {"response": r, "username_list": result_list}
        else:
            return {"response": r, "username_list": []}

    def forget_password(self, email):
        # print("Forget Password")
        data_get = {"email": email}
        r = requests.post(self.user_url + "/recover", data=data_get)
        self.print_result("forget_password", r.status_code, r.content)
        return r

    def get_number_of_likes_of_a_user(self, user_id):
        r = requests.get(self.user_url + user_id + "/likes")
        self.print_result("forget_password", r.status_code, r.content)
        return r

    def report_user(self, param_dict={}):
        # print("Report a User")
        if type(param_dict) is dict:
            r = requests.post(self.user_url + "/report", data=param_dict)
            self.print_result("report_user", r.status_code, r.content)
            return r

    def check_user_valid(self, username):
        # print("Check User Exist or not")
        r = requests.get(self.user_url + "username-valid/" + username, headers=self.get_header_auth())
        self.print_result("check_user_valid", r.status_code, r.content)
        return r

    def get_following_users_snaps(self):
        r = requests.get(self.user_url + "following/snaps", headers=self.get_header_auth())
        self.print_result("get_following_users_snaps", r.status_code, r.content)
        return r

    def get_encode_base64_image(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = "data:image/" + imghdr.what(image_path) + ";base64," + base64.b64encode(
                image_file.read()).decode('utf-8')
        return encoded_string

def main():
    user = User("test3@gmail.com", "12345678", "12234")
    user.login()
    # user.add_snap_to_favourite('7584')
    # user.count_user_follower_and_following('5118')
    # user.get_following_users_snaps()
    # user.get_following()
    # user.get_following_user_snap('5117')
    # user.get_user_profile()
    # user.get_follower()
    # user.get_following(user.get_user_id())
    user.get_snaps()
    # user.follow_user("5118")
    # user.unfollow_user(user.get_user_id()"5117")
    # user.get_favourite_snaps()
    # user.get_user_profile()
    # user.get_follower()
    # auth = Authentication('test4@gmail.com', "12345677", "12235")
    # auth.register("Hong Kong")
    # result = login("test3@gmail.com", "12345677", "12345")

    # update_user_profile(id, token, {"firstname": "HO", "lastname": "Raymond"})
    # get_user_profile(id)
    # user = User("test3@gmail.com", "12345677", "12345")
    # user.get_following_user_snap('5117')
    # user.get_following_user_snap("5117")
    # follow_user('5116', id, token)
    # unfollow_user('5116', id, token)
    # get_following(id, token)
    # login("", "12345677", "12345")
    # login("test3@gmail.com", "", "12345")
    # login("test3@gmail.com", "12345677", "")
    # login("", "", "12345")
    # login("test3@gmail.com", "", "")
    # login("", "12345677", "")
    # login("test@gmail.com", "12345677", "12345")
    # login("test3@gmail.com", "1234567", "12345")

    # change_password(token, '12345678', '12345677')
    # logout(token)
    # register("test3@gmail.com", "12345678", "12345", "Hong Kong")
    pass


main()
