import requests
import json


class Authentication:
    def __init__(self, email, password, dev_id):
        self.__email = email
        self.__password = password
        self.__dev_id = dev_id
        self.__base_url = "http://api-dev.dress-as.com:4460/users/login"
        self.__result = ""

    def login(self):
        print("Login")
        data_get = {'device_id': self.__dev_id,
                    'email': self.__email,
                    'password': self.__password}
        r = requests.Session().post(self.__base_url, data=data_get)
        if r.content is not None:
            print(r.content)
            self.__result = json.loads(r.content.decode('utf-8'))
            print('Status Code: ', r.status_code)
            if r.status_code == 200:
                if self.__result['account_type'] == "application" and self.__result['token'] is not None:
                    print("Login Successful!")
                    return self.__result
                else:
                    print("unexpected error")
            elif r.status_code == 400 or r.status_code == 403:
                return self.__result['error']
        else:
            print("Unexpected Error")
            return

    def register(self, location):
        print("Register")
        data_get = {'email': self.__email,
                    'password': self.__password,
                    'device_id': self.__dev_id,
                    "location": location}
        r = requests.post(self.__base_url + "register", data=data_get)
        result = json.loads(r.content.decode('utf-8'))
        print(r.status_code)
        if r.status_code == 200:
            if result['user_id'] is not None and result['token'] is not None:
                print(r.headers)
                print(result)
                return result
        elif r.status_code == 400:
            print(result['error'])
            return result['error']
        elif r.status_code == 403:
            print(result['error'])
            return result['error']

    def logout(self):
        print("Logout")
        headers_get = {'Authorization': "bearer " + self.get_token()}
        r = requests.post(self.__base_url + "logout", headers=headers_get)
        print(r.status_code)
        result = json.loads(r.content.decode('utf-8'))
        if r.status_code == 200:
            if result['token'] is None:
                print("Logout successful")
            # print(r.headers)
            # print(result['token'])
        elif r.status_code == 401:
            print(result['error'])

    def signin_with_google(self, google_token):
        print("Sign-in with Google")
        data_get = {"id_token": google_token,
                    "device_id": self.__dev_id}
        r = requests.post(self.__base_url + "login/google", data=data_get)
        if r.content is not None:
            result = json.loads(r.content.decode('utf-8'))
            if r.status_code == 200:
                print(result)
            elif r.status_code >= 400:
                print(result['error'])
                return result['error']

    def get_token(self):
        return self.__result['token']

    def get_user_id(self):
        return self.__result['user_id']

    def get_device_id(self):
        return self.__dev_id

    # if __name__ == '__main__':
    #     x = login("test3@gmail.com", "12345677", "12345")
    #     x.authenticate()
    #     print(x.get_token())
    #     print(x.get_user_id())
