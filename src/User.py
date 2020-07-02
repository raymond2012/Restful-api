import requests
import json
import pytest
import datetime
import logging

from src.Authentication import Authentication


class User:

    def __init__(self):
        auth = Authentication("test3@gmail.com", "12345677", "12345")
        auth.login()
        self.device_id = auth.get_device_id()
        self.token = auth.get_token()
        self.id = auth.get_user_id()
        self.base_url = "http://api-dev.dress-as.com:4460/users/"

    ###Users###
    def get_user_profile(self):
        logging.debug("Get User Profile")
        url = self.base_url + self.id + "/profile"
        r = requests.get(url)
        print(r.status_code)
        print(url)
        if r.content is not None:
            if r.status_code == 200:
                print(r.content)
                return json.loads(r.content.decode('utf-8'))
            elif r.status_code >= 400:
                print(r.content)
                return
        else:
            print("Unexpected error")
            return

    def change_password(self, curr, new):
        logging.debug("Change password")
        headers_get = {'Authorization': "Bearer " + self.token}
        data_get = {
            "curr_password": curr,
            "new_password": new
        }
        r = requests.post(self.base_url + "/users/" + self.id + "/password", headers=headers_get, data=data_get)
        print(r.status_code)
        if r.status_code == 200:
            logging.debug("Change password Successfully")
            return
        elif r.status_code >= 400:
            if r.content is not None:
                return json.loads(r.content.decode('utf-8'))['error']
            else:
                print("Unexpected error")
                return

    def update_user_profile(self, edit_profile):
        logging.debug("Update User Profile")
        data_get = edit_profile
        header_get = {"Authorization": "Bearer " + self.token}
        r = requests.patch(self.base_url + self.id + "/profile", headers=header_get, data=data_get)
        if r.status_code == 200:
            print("Update Successful")
        elif r.status_code >= 400:
            if r.content is not None:
                return json.loads(r.content.decode('utf-8'))['error']
            else:
                print("Unexpected error")

    def upload_user_profile_pic(self, name, body):
        logging.debug("upload User Profile Pic")
        header_get = {"Authorization": "Bearer " + self.token}
        data_get = {
            "image_name": name,
            "image_body": body
        }
        r = requests.post(self.base_url + self.id + "/propic", headers=header_get, data=data_get)
        if r.status_code == 200:
            logging.debug("Upload Successful")
            return
        elif r.status_code >= 400:
            if r.content is not None:
                return json.loads(r.content.decode('utf-8'))['error']
            else:
                print("Unexpected error")

    def delete_user_profile_pic(self):
        logging.debug("Delete User Profile Pic")
        header_get = {"Authorization": "Bearer " + self.token}
        r = requests.delete(self.base_url + self.id + "/propic", headers=header_get)
        if r.status_code == 200:
            logging.debug("Delete Profile Picture Successful")
            return
        elif r.status_code >= 401:
            if r.content is not None:
                return json.loads(r.content.decode('utf-8'))['error']
            else:
                print("Unexpected error")

    def get_follower(self):
        print("Get Follower")
        header_get = {"Authorization": "Bearer " + self.token}
        r = requests.get(self.base_url + self.id + "/follower", headers=header_get)
        if r.status_code == 200:
            print(r.content)
            return json.loads(r.content.decode('utf-8'))
        else:
            print("Unexpected error")

    def get_following(self):
        logging.debug("Get Following")
        header_get = {"Authorization": "Bearer " + self.token}
        r = requests.get(self.base_url + self.id + "/following", headers=header_get)
        if r.status_code == 200:
            print(r.content)
            return json.loads(r.content.decode('utf-8'))
        else:
            print("Unexpected error")

    def follow_user(self, blogger_id):
        logging.info("Follow a User")
        header_get = {"Authorization": "Bearer " + self.token}
        r = requests.post(self.base_url + self.id + "/follow/" + blogger_id, headers=header_get)
        print(r.status_code)
        if r.status_code == 201:
            logging.debug("Follow a user successfully")
        elif r.status_code >= 400:
            if r.content is not None:
                return json.loads(r.content.decode('utf-8'))['error']
            else:
                print("Unexpected error")

    def unfollow_user(self, blogger_id):
        logging.debug("Unfollow a User")
        header_get = {"Authorization": "Bearer " + self.token}
        r = requests.delete(self.base_url + self.id + "/follow/" + blogger_id, headers=header_get)
        if r.status_code == 201:
            logging.debug("Unfollow a user successfully")
        elif r.status_code >= 400:
            if r.content is not None:
                return json.loads(r.content.decode('utf-8'))['error']
            else:
                print("Unexpected error")

    def print_output(self, time, success, name, task, code):
        if code == 200:
            print("[%s][%s][%s][%s]" % (time, success, task, name))
        else:
            print("[%s][%s][%s][%s] Expected return code is [200], but get [%s]" % (time, success, task, name, code))

def main():
    # result = login("test3@gmail.com", "12345677", "12345")

    # update_user_profile(id, token, {"firstname": "HO", "lastname": "Raymond"})
    # get_user_profile(id)
    user = User()
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
