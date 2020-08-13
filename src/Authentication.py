import requests
import json
import constant as con


class Authentication:
    def __init__(self, email, password, dev_id):
        self.get_token = None
        self.__email = email
        self.__password = password
        self.__get_device_id = dev_id
        self.__auth_url = con.USER_URL
        self.__token = ""
        self.__id = ""

    def login(self):
        # print("Login")
        data_get = {'device_id': self.get_device_id,
                    'email': self.__email,
                    'password': self.__password}
        r = requests.Session().post(self.__auth_url + "login", data=data_get)
        self.print_result("login", r.status_code, r.content)
        if r.status_code == 200:
            result = json.loads(r.content.decode('utf-8'))
            self.__token = result['token']
            self.__id = result['user_id']
        return r

    def register(self, location='Hong Kong'):
        # print("Register")
        data_get = {'email': self.__email,
                    'password': self.__password,
                    'device_id': self.get_device_id,
                    "location": location}
        r = requests.post(self.__auth_url + "/register", data=data_get)
        self.print_result("register", r.status_code, r.content)
        return r

    def logout(self):
        # print("Logout")
        headers_get = self.get_header_auth_json()
        r = requests.post(self.__auth_url + "logout", headers=headers_get)
        self.print_result("logout", r.status_code, r.content)
        return r

    def signin_with_google(self, google_token):
        # print("Sign-in with Google")
        data_get = {"id_token": google_token,
                    "device_id": self.get_device_id}
        r = requests.post(self.__auth_url + "login/google", data=data_get)
        self.print_result("signin_with_google", r.status_code, r.content)

    def get_token(self):
        return str(self.__token) if self.__token is not None else ""

    def set_token(self, token):
        self.__token = token

    def get_header_auth(self):
        return {"Authorization": "Bearer " + self.__token} if self.__token is not None else {"Authorization": "Bearer "}

    def get_header_auth_json(self):
        return {"Authorization": "Bearer " + self.__token,
                "Content-Type": "application/json"} if self.__token is not None else {"Authorization": "Bearer ",
                                                                                      "Content-Type": "application/json"}

    def get_user_id(self):
        return str(self.__id) if self.__id is not None else None

    def get_device_id(self):
        return str(self.__get_device_id) if self.__get_device_id is not None else None

    def get_email(self):
        return self.__email if self.__email is not None else None

    def get_password(self):
        return self.__password if self.__password is not None else None

    def get_username(self):
        return self.__email.split("@")[0] if self.__email is not None else None

    def get_base_url(self):
        return self.__base_url if self.__base_url is not None else None

    # if __name__ == '__main__':
    #     x = login("test3@gmail.com", "12345677", "12345")
    #     x.authenticate()
    #     print(x.get_token())
    #     print(x.get_user_id())
    @staticmethod
    def print_result(fun_name, status_code, content=None):
        try:
            if content is None:
                result = ""
            else:
                result = json.loads(content.decode('utf-8'))
        except ValueError:
            # print("Unexpected error:", sys.exc_info()[0])
            result = content.decode('utf-8')
        finally:
            if 200 <= status_code < 300:
                if result is not None:
                    print("Function: %s, Status Code: %s, Result: %s" % (fun_name, str(status_code), result))
                else:
                    print("Function: %s, Status Code: %s, Result: Successful" % (fun_name, str(status_code)))
            elif status_code >= 400:
                if result is not None:
                    print("Function: %s, Status Code: %s, Error : %s" % (fun_name, str(status_code), result))
                else:
                    print("Function: %s, Status Code: %s, Error: No error Message" % (fun_name, str(status_code)))
            else:
                print("Function: %s, Status Code: %s, Error: unexpected error" % (fun_name, str(status_code)))
