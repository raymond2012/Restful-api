import requests
import json

from src.Authentication import login


class login():
    def __init__(self, email, password, user_id):
        self.email = email
        self.password = password
        self.user_id = user_id
        self.url = "http://api-dev.dress-as.com:4460/users/login/"
        self.result = ""

    def authenticate(self):
        # print("Login")
        data_get = {'device_id': self.user_id,
                    'email': self.email,
                    'password': self.password}
        r = requests.Session().post(self.url, data=data_get)
        self.result = json.loads(r.content.decode('utf-8'))
        # print('Status Code: ', r.status_code)
        if r.status_code == 200:
            if self.result['account_type'] == "application" and self.result['token'] is not None:
                print("Login Successful!")
                return self.result
            else:
                print("unexpected error")
        elif r.status_code == 400 or r.status_code == 403:
            return self.result['error']

    def get_token(self):
        return self.result['token']

    def get_user_id(self):
        return self.result['user_id']

    # if __name__ == '__main__':
    #     x = login("test3@gmail.com", "12345677", "12345")
    #     x.authenticate()
    #     print(x.get_token())
    #     print(x.get_user_id())
