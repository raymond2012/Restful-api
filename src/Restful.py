import requests
import json

base_url = "http://api-dev.dress-as.com:4460"
login_url = "/users/login/"
register_url = "/users/register/"
logout_url = "/users/logout/"
google_sign_in_url = "/users/login/google"

def login(email, password,user_id):
    print("Login")
    data_get = {'device_id': user_id,
                'email': email,
                'password': password}
    r = requests.post(base_url + login_url, data=data_get)
    if r.ok:
        print(r.headers)
        print(r.content.decode('utf-8'))
        return json.loads(r.content.decode('utf-8'))['token']
    return

def register(email, password, device_id, location):
    print("Register")
    data_get = {'email': email,
                'password': password,
                'device_id': device_id,
                "location": location}
    r = requests.post(base_url + register_url, data= data_get)
    if r.ok:
        print(r.headers)
        print(r.content)

def logout(bearer_token):
    print("Logout")
    headers_get = {'Authorization': bearer_token}
    r = requests.post(base_url + logout_url, headers=headers_get)
    if r.ok:
        print(r.headers)
        print(r.content)

def signin_with_google(token, id):
    print("Sign-in with Google")
    data_get = {"id_token": token,
                "device_id": id}
    r = requests.post(base_url + google_sign_in_url, data=data_get)
    if r.ok:
        print(r.headers)
        print(r.content)

def main():
    login("test@gmail.com", "12345678", "12345")
    signin_with_google("212", "12345")

main()