import requests
import json
import pytest
import datetime
import logging

from src.Authentication import Authentication


class Test:

    def __init__(self):
        auth = Authentication("test3@gmail.com", "12345677", "12345")
        auth.login()
        self.token = str(auth.get_token())
        self.id = str(auth.get_user_id())
        self.base_url = "http://api-dev.dress-as.com:4460/users/"

    def get_follower(self):
        print("Get Follower")
        header_get = {"Authorization": "Bearer " + self.token}
        r = requests.get(self.base_url + self.id + "/follower", headers=header_get)
        if r.status_code == 200:
            print(r.content)
            return json.loads(r.content.decode('utf-8'))
        else:
            print("Unexpected error")

def main():
    user = Test()
    user.get_follower()

main()