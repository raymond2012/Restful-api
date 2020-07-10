import requests


class Miscellaneous:
    def __init__(self):
        self.base_url = "http://api-dev.dress-as.com:4460"

    def get_privacy_policy(self):
        print("Get Privacy Policy")
        r = requests.get(self.base_url + "/privacy")
        self.print_result("get_privacy_policy", r.status_code, r.content)

    def get_terms_and_conditions(self):
        print("Get Terms and Conditions")
        r = requests.get(self.base_url + "/terms")
        self.print_result("get_terms_and_conditions", r.status_code, r.content)

    def get_country_list(self):
        print("Get Terms and Conditions")
        r = requests.get(self.base_url + "/countries")
        self.print_result("get_terms_and_conditions", r.status_code, r.content)

    def get_background_image(self):
        print("Get Getstart Background Images")
        r = requests.get(self.base_url + "/background")
        self.print_result("get_getstart_background_image", r.status_code, r.content)

    def get_social_media_list(self):
        print("Get Social Media List")
        r = requests.get(self.base_url + "/social-media")
        self.print_result("get_social_media_list", r.status_code, r.content)