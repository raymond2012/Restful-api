import urllib

import requests
import json
import pytest
import datetime

from src.Authentication import Authentication


class User(Authentication):

    def __init__(self, email, password, dev_id):
        Authentication.__init__(email, password, dev_id)
        self.login()
        self.__dev_id = self.get_device_id()
        self.__token = "Bearer " + self.get_token()
        self.__id = self.get_user_id()
        self.base_url = "http://api-dev.dress-as.com:4460/users/"

    ###Users###
    def get_user_profile(self):
        print("Get User Profile")
        url = self.base_url + self.__id + "/profile"
        r = requests.get(url)
        print(r.status_code)
        print(url)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return result
            elif r.status_code >= 400:
                return "Code: " + str(r.status_code) + " Error:" + result['error']

    def change_password(self, curr, new):
        print("Change password")
        headers_get = {'Authorization': self.__token}
        data_get = {
            "curr_password": curr,
            "new_password": new
        }
        r = requests.post(self.base_url + "/users/" + self.__id + "/password", headers=headers_get, data=data_get)
        print(r.status_code)
        if r.status_code == 200:
            print("Change password Successfully")
            return
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error

    def update_user_profile(self, edit_profile):
        print("Update User Profile")
        data_get = edit_profile
        header_get = {"Authorization": self.__token}
        r = requests.patch(self.base_url + self.__id + "/profile", headers=header_get, data=data_get)
        if r.status_code == 200:
            print("Update Successful")
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error


    def upload_user_profile_pic(self, name, body):
        print("upload User Profile Pic")
        header_get = {"Authorization": self.__token}
        data_get = {
            "image_name": name,
            "image_body": body
        }
        r = requests.post(self.base_url + self.__id + "/propic", headers=header_get, data=data_get)
        if r.status_code == 200:
            print("Upload Successful")
            return
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error


    def delete_user_profile_pic(self):
        print("Delete User Profile Pic")
        header_get = {"Authorization": self.__token}
        r = requests.delete(self.base_url + self.__id + "/propic", headers=header_get)
        if r.status_code == 200:
            print("Delete Profile Picture Successful")
            return
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error


    def get_follower(self):
        print("Get Follower")
        header_get = {"Authorization": self.__token}
        r = requests.get(self.base_url + self.__id + "/follower", headers=header_get)
        if r.status_code == 200:
            return json.loads(r.content.decode('utf-8'))
        else:
            print("Unexpected error")

    def get_following(self):
        print("Get Following")
        header_get = {"Authorization": self.__token}
        r = requests.get(self.base_url + self.__id + "/following", headers=header_get)
        if r.status_code == 200:
            return json.loads(r.content.decode('utf-8'))
        else:
            print("Unexpected error")

    def follow_user(self, blogger_id):
        print("Follow a User")
        header_get = {"Authorization": self.__token}
        r = requests.post(self.base_url + self.__id + "/follow/" + blogger_id, headers=header_get)
        print(r.status_code)
        if r.status_code == 201:
            print("Follow a user successfully")
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error
            else:
                print("Unexpected error")

    def unfollow_user(self, blogger_id):
        print("Unfollow a User")
        header_get = {"Authorization": self.__token}
        r = requests.delete(self.base_url + self.__id + "/follow/" + blogger_id, headers=header_get)
        if r.status_code == 201:
            print("Unfollow a user successfully")
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error
            else:
                print("Unexpected error")

    def get_favourite_snaps(self, param_dict):
        print("Get Favourite Snaps")
        header_get = {"Authorization": self.__token}
        if type(param_dict) is dict:
            url_param = urllib.parse.urlencode(param_dict)
            url = self.base_url + self.__id + "/favourite/snap?" + url_param
            r = requests.get(url, headers=header_get)
            if r.content is not None:
                result = json.loads(r.content.decode('utf-8'))
                if r.status_code == 200:
                    return result
                elif r.status_code >= 400:
                    return "Code: " + str(r.status_code) + " Error:" + result['error']

    def get_favourite_products(self):
        print("Get Favourite Products")
        header_get = {"Authorization": self.__token}
        r = requests.get(self.base_url + self.__id + "/favourite/product", headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return result
            elif r.status_code >= 400:
                return "Code: " + str(r.status_code) + " Error:" + result['error']

    def add_snap_product_to_favourite(self, snap_id):
        print("Add a Snap to Favourite")
        header_get = {"Authorization": self.__token}
        url = self.base_url + self.__id + "/favourite/snap/" + snap_id
        r = requests.post(url, headers=header_get)
        if r.status_code == 201:
            return "Code: " + str(r.status_code) + "Message: Add a Snap to Favourite Successfully"
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error

    def remove_snap_from_favourite(self, snap_id):
        print("Delete a Snap from Favourite")
        header_get = {"Authorization": self.__token}
        url = self.base_url + self.__id + "/favourite/snap/" + snap_id
        r = requests.delete(url, headers=header_get)
        if r.status_code == 204:
            return "Code: " + str(r.status_code) + "Message: Add a Snap to Favourite Successfully"
        elif r.status_code >= 400:
            if r.content is not None:
                error = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + error

    def get_favourite_products(self):
        print("Get Favourite Products")
        header_get = {"Authorization": self.__token}
        r = requests.delete(self.base_url + self.__id + "/favourite/product", headers=header_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                return "Code: " + str(r.status_code) + "Message: Get Favourite Products Successfully"
            elif r.status_code >= 400:
                result = json.loads(r.content.decode('utf-8'))['error']
                return "Code: " + str(r.status_code) + " Error:" + result['error']

    def add_snap_product_to_favourite(self, prod_id):
        print("Add a Product to Favourite")
        header_get = {"Authorization": self.__token}
        url = self.base_url + self.__id + "/favourite/product/" + prod_id
        r = requests.post(url, headers=header_get)
        if r.status_code == 200:
            return "Code: " + str(r.status_code) + "Message: Add a Product to Favourite Successfully"
        elif r.status_code >= 400:
            result = json.loads(r.content.decode('utf-8'))['error']
            return "Code: " + str(r.status_code) + " Error:" + result['error']

    def remove_snap_product_to_favourite(self, prod_id):
        print("Add a Product to Favourite")
        header_get = {"Authorization": self.__token}
        url = self.base_url + self.__id + "/favourite/product/" + prod_id
        r = requests.delete(url, headers=header_get)
        if r.status_code == 204:
            return "Code: " + str(r.status_code) + "Message: Remove a Product to Favourite Successfully"
        elif r.status_code >= 400:
            result = json.loads(r.content.decode('utf-8'))['error']
            return "Code: " + str(r.status_code) + " Error:" + result['error']

    @staticmethod
    def print_output(time, success, name, task, code):
        if code == 200:
            print("[%s][%s][%s][%s]" % (time, success, task, name))
        else:
            print("[%s][%s][%s][%s] Expected return code is [200], but get [%s]" % (time, success, task, name, code))


def main():
    # result = login("test3@gmail.com", "12345677", "12345")

    # update_user_profile(id, token, {"firstname": "HO", "lastname": "Raymond"})
    # get_user_profile(id)
    user = User("test3@gmail.com", "12345677", "12345")
    user.get_user_profile()
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
