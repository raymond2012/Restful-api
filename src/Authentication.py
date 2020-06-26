import requests
import json
import pytest
import datetime

base_url = "http://api-dev.dress-as.com:4460"
login_url = "/users/login/"
register_url = "/users/register/"
logout_url = "/users/logout/"
google_sign_in_url = "/users/login/google"

### Authorization ###
def login(email, password, user_id):
    # print("Login")
    data_get = {'device_id': user_id,
                'email': email,
                'password': password}
    r = requests.Session().post(base_url + login_url, data=data_get)
    result = json.loads(r.content.decode('utf-8'))
    # print('Status Code: ', r.status_code)
    if r.status_code == 200:
        if result['account_type'] == "application" and result['token'] != None:
            print_output(r.headers['Date'], "Pass", "Email login successful", "Login", r.status_code)
            return result['token']
        else:
            print("unexpected error")
    elif r.status_code == 400 or r.status_code == 403:
        print_output(r.headers['Date'], "Fail", "Email login unsuccessful", "Login", r.status_code)
        return result['error']

def register(email, password, device_id, location):
    print("Register")
    data_get = {'email': email,
                'password': password,
                'device_id': device_id,
                "location": location}
    r = requests.post(base_url + register_url, data=data_get)
    result = json.loads(r.content.decode('utf-8'))
    print(r.status_code)
    if r.status_code == 200:
        print(r.headers)
        print(result)
        return result
    elif r.status_code == 400:
        print(result['error'])
        return result['error']
    elif r.status_code == 403:
        print(result['error'])
        return result['error']


def logout(token):
    print("Logout")
    headers_get = {'Authorization': "bearer " + token}
    r = requests.post(base_url + logout_url, headers=headers_get)
    print(r.status_code)
    result = json.loads(r.content.decode('utf-8'))
    if r.status_code == 200:
        if result['token'] is None:
            print("Logout successful")
        # print(r.headers)
        # print(result['token'])
    elif r.status_code == 401:
        print(result['error'])


def signin_with_google(token, id):
    print("Sign-in with Google")
    data_get = {"id_token": token,
                "device_id": id}
    r = requests.post(base_url + google_sign_in_url, data=data_get)
    result = json.loads(r.content.decode('utf-8'))
    if r.status_code == 200:
        print(r.headers)
        print(result)
    elif r.status_code == 400:
        print(result['error'])
        return result['error']

#snap
def get_snap(filter, offset, limit, order = "ASC", order_by = "creation", token = ""):
    print("Get Sanp")
    headers_get = {'Authorization': "Bearer " + token}
    custom_url = base_url + "/snaps?filter=" + filter + "&limit=" + limit + "&order=" + order + "&orderby=" + order_by




def change_password(token, curr, new):
    print("Change password")
    headers_get = {'Authorization': "Bearer " + token}
    data_get = {
        "curr_password": curr,
        "new_password": new
    }
    r = requests.post(base_url + "/users/5118/password", headers=headers_get, data=data_get)
    print(r.status_code)
    # result = json.loads(r.content.decode('utf-8'))
    if r.status_code == 200:
        print(r.content)
    elif r.status_code == 400 or r.status_code == 401 or r.status_code == 500:
        print(r.content)

def update_user_profile(token):

def print_output(datetime, success, name, task, code):
    if code == 200:
        print("[%s][%s][%s][%s]" % (datetime, success, task, name))
    else:
        print("[%s][%s][%s][%s] Expected return code is [200], but get [%s]" % (datetime, success, task, name, code))

def main():
    login("test3@gmail.com", "12345677", "12345")
    login("", "12345677", "12345")
    login("test3@gmail.com", "", "12345")
    login("test3@gmail.com", "12345677", "")
    login("", "", "12345")
    login("test3@gmail.com", "", "")
    login("", "12345677", "")
    login("test@gmail.com", "12345677", "12345")
    login("test3@gmail.com", "1234567", "12345")

    # change_password(token, '12345678', '12345677')
    # logout(token)
    # register("test3@gmail.com", "12345678", "12345", "Hong Kong")


main()
