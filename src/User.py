import urllib

import requests
import json
import pytest
import datetime

from src.Authentication import Authentication


def check_token(func):
    def inner(self, *args, **kwargs):
        if self.get_token() is None:
            raise ValueError
        else:
            return func(self, *args, **kwargs)

    return inner


class User(Authentication):

    def __init__(self, email="", password="", dev_id=""):
        Authentication.__init__(self, email, password, dev_id)
        self.base_url = "http://api-dev.dress-as.com:4460/users/"
        if email and password is not None:
            self.login()
            self.__dev_id = self.get_device_id()
            self.__token = "Bearer " + self.get_token()
            self.__id = str(self.get_user_id())
            self.__header_auth = self.get_header_auth()
        else:
            print("No email and password")

    ###Users###
    @check_token
    def get_user_profile(self):
        print("Get User Profile")
        r = requests.get(self.base_url + self.__id + "/profile")
        self.print_result("get_user_profile", r.status_code, r.content)
        return r

    @check_token
    def change_password(self, curr, new):
        print("Change password")
        data_get = {
            "curr_password": curr,
            "new_password": new
        }
        r = requests.post(self.base_url + "/users/" + self.__id + "/password", headers=self.__header_auth,
                          data=data_get)
        self.print_result("change_password", r.status_code, r.content)
        return r

    @check_token
    def update_user_profile(self, edit_profile):
        print("Update User Profile")
        r = requests.patch(self.base_url + self.__id + "/profile", headers=self.__header_auth, data=edit_profile)
        self.print_result("update_user_profile", r.status_code, r.content)
        return r

    @check_token
    def upload_user_profile_pic(self, name, body):
        print("upload User Profile Pic")
        data_get = {
            "image_name": name,
            "image_body": body
        }
        r = requests.post(self.base_url + self.__id + "/propic", headers=self.__header_auth, data=data_get)
        self.print_result("upload_user_profile_pic", r.status_code, r.content)
        return r

    @check_token
    def delete_user_profile_pic(self):
        print("Delete User Profile Pic")
        r = requests.delete(self.base_url + self.__id + "/propic", headers=self.__header_auth)
        self.print_result("delete_user_profile_pic", r.status_code, r.content)
        return r

    @check_token
    def get_follower(self):
        print("Get Follower")
        r = requests.get(self.base_url + self.__id + "/follower", headers=self.__header_auth)
        self.print_result("get_follower", r.status_code, r.content)
        return r

    def get_following(self):
        print("Get Following")
        r = requests.get(self.base_url + self.__id + "/following", headers=self.__header_auth)
        self.print_result("get_following", r.status_code, r.content)
        return r

    def follow_user(self, blogger_id):
        print("Follow a User")
        r = requests.post(self.base_url + self.__id + "/follow/" + blogger_id, headers=self.__header_auth)
        self.print_result("follow_user", r.status_code, r.content)
        return r

    def unfollow_user(self, blogger_id):
        print("Unfollow a User")
        r = requests.delete(self.base_url + self.__id + "/follow/" + blogger_id, headers=self.__header_auth)
        self.print_result("follow_user", r.status_code, r.content)
        return r

    def get_favourite_snaps(self, param_dict):
        print("Get Favourite Snaps")
        if type(param_dict) is dict:
            url_param = urllib.parse.urlencode(param_dict)
            r = requests.get(self.base_url + self.__id + "/favourite/snap?" + url_param, headers=self.__header_auth)
            self.print_result("get_favourite_snaps", r.status_code, r.content)
            return r
        else:
            print("The type of param_dict is not a dictionary")

    def get_favourite_products(self):
        print("Get Favourite Products")
        r = requests.get(self.base_url + self.__id + "/favourite/product", headers=self.__header_auth)
        self.print_result("get_favourite_products", r.status_code, r.content)
        return r

    def add_snap_product_to_favourite(self, snap_id):
        print("Add a Snap to Favourite")
        r = requests.post(self.base_url + self.__id + "/favourite/snap/" + snap_id, headers=self.__header_auth)
        self.print_result("add_snap_product_to_favourite", r.status_code, r.content)

    def remove_snap_from_favourite(self, snap_id):
        print("Delete a Snap from Favourite")
        url = self.base_url + self.__id + "/favourite/snap/" + snap_id
        r = requests.delete(url, headers=self.__header_auth)
        self.print_result("remove_snap_from_favourite", r.status_code, r.content)

    def get_favourite_products(self):
        print("Get Favourite Products")
        r = requests.delete(self.base_url + self.__id + "/favourite/product", headers=self.__header_auth)
        self.print_result("get_favourite_products", r.status_code, r.content)

    def add_snap_product_to_favourite(self, prod_id):
        print("Add a Product to Favourite")
        r = requests.post(self.base_url + self.__id + "/favourite/product/" + prod_id, headers=self.__header_auth)
        self.print_result("add_snap_product_to_favourite", r.status_code, r.content)

    def remove_snap_product_to_favourite(self, prod_id):
        print("Add a Product to Favourite")
        r = requests.delete(self.base_url + self.__id + "/favourite/product/" + prod_id, headers=self.__header_auth)
        self.print_result("remove_snap_product_to_favourite", r.status_code, r.content)

    def get_user_snap(self, param_dict):
        print("Get Snaps of a user")
        if type(param_dict) is dict:
            url_param = urllib.parse.urlencode(param_dict)
            r = requests.get(self.base_url + self.__id + "snap?" + url_param, headers=self.__header_auth)
            self.print_result("get_user_snap", r.status_code, r.content)

    def search_user(self, keyword):
        print("Search User")
        r = requests.get(self.base_url + "search?" + keyword, headers=self.__header_auth)
        self.print_result("search_user", r.status_code, r.content)

    def forget_password(self, email):
        print("Forget Password")
        data_get = {"email": email}
        r = requests.post(self.base_url + "/recover", data=data_get)
        self.print_result("forget_password", r.status_code, r.content)

    def report_user(self, user_id, report_type, remark=""):
        print("Report a User")
        data_get = {
            "user_id": user_id,
            "report_type": report_type,
            "remark": remark
        }
        r = requests.post(self.base_url + "/report", data=data_get)
        self.print_result("report_user", r.status_code, r.content)

    def check_user_exist(self, username):
        print("Check User Exist or not")
        r = requests.post(self.base_url + "/username-exists/" + username, headers=self.__header_auth)
        self.print_result("check_user_exist", r.status_code, r.content)

    def get_following_user_snap(self, user_id):
        print("Get Following User Snap")
        r = requests.get(self.base_url + user_id + "/following/snaps", headers=self.__header_auth)
        # print(r.content.decode('utf-8'))
        self.print_result("check_user_exist", r.status_code, r.content)

    @staticmethod
    def print_output(time, success, name, task, code):
        if code == 200:
            print("[%s][%s][%s][%s]" % (time, success, task, name))
        else:
            print("[%s][%s][%s][%s] Expected return code is [200], but get [%s]" % (time, success, task, name, code))


def main():
    user = User("test3@gmail.com", "12345677", "12234")
    user.get_user_profile()
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


main()
