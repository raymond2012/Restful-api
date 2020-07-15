import base64
import datetime
import imghdr
import json

import pytest

from src.Authentication import Authentication
from src.Snap import Snap
from src.User import User


### Authentication ###
class test():
    def __init__(self):
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user2 = User("test2@gmail.com", "12345678", "12345")
        self.login = self.user.login()
        self.login2 = self.user2.login()
        print(self.user.get_header_auth())
        print(self.user.get_user_id())

    def json_result_to_snap_id_list(self, data):
        result = list(map(lambda x: x["snap_id"], json.loads(data.content.decode('utf-8'))))
        print(result)
        return result

    def test_authetication(self):
        login_result = json.loads(self.login.content.decode('utf-8'))
        assert self.r.status_code == 200, "Expected Status code is 200 but the status code is " + \
                                          str(self.login.status_code)
        assert login_result['token'] is not None and \
               login_result['user_id'] > 0, "Expected token and user_id exist but they are None"
        logout_result = json.loads(self.user.logout().content.decode('utf-8'))
        # print(logout_result)
        assert logout_result['token'] is None, "Expected token is null but the token is " + logout_result['token']
        # print(self.user.get_user_profile().status_code)

    def test_get_user_profile(self):
        result = self.user.get_user_profile()
        print(result)
        assert result.status_code == 200, "Expected Status code: 200 but the status code: " + result.status_code

    # def test_change_password():
    #     user = User("test3@gmail.com", "12345677", "12345")
    #     result = user.change_password("12345677", "12345677")
    #     print(result)
    #     assert result.status_code == 201

    def test_follow_a_user(self):
        self.user2.follow_user(self.user.get_user_id())
        assert str(
            json.loads(self.user2.get_following().content.decode('utf-8'))['following'][0][
                'user_id']) == self.user.get_user_id()
        assert str(
            json.loads(self.user.get_follower().content.decode('utf-8'))['follower'][0][
                'user_id']) == self.user2.get_user_id()
        self.user2.unfollow_user(self.user.get_user_id())
        print(str(json.loads(self.user2.get_following().content.decode('utf-8'))['following']))
        # assert str(json.loads(user2.get_following().content.decode('utf-8'))['following']) ==

    def test_get_snap_checking_order_by_creation(self):
        query_full = {"filter": "", "offset": "", "offset_id": "", "limit": "40", "order": "DESC",
                      "orderby": "creation"}
        query_first = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                       "orderby": "creation"}
        query_second = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                        "orderby": "creation"}
        query_third = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                       "orderby": "creation"}
        query_last = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                      "orderby": "creation"}
        result_full = self.user.get_snaps(query_full)
        query_second['offset_id'] = result_full[int(len(result_full) / 4 - 1)]
        query_third['offset_id'] = result_full[int(len(result_full) / 2 - 1)]
        query_last['offset_id'] = result_full[int(len(result_full) * 3 / 4 - 1)]
        assert result_full == self.user.get_snaps(query_first) + self.user.get_snaps(
            query_second) + self.user.get_snaps(query_third) + self.user.get_snaps(query_last)

    def test_search_snap_checking_order_by_creation(self):
        query_full = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "40", "order": "DESC",
                      "orderby": "creation"}
        query_first = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                       "orderby": "creation"}
        query_second = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                        "orderby": "creation"}
        query_third = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                       "orderby": "creation"}
        query_last = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                      "orderby": "creation"}
        result_full = self.user.search_snaps(query_full)
        query_second['offset_id'] = result_full[int(len(result_full) / 4 - 1)]
        query_third['offset_id'] = result_full[int(len(result_full) / 2 - 1)]
        query_last['offset_id'] = result_full[int(len(result_full) * 3 / 4 - 1)]
        assert result_full == self.user.search_snaps(query_first) + self.user.search_snaps(
            query_second) + self.user.search_snaps(query_third) + self.user.search_snaps(query_last)

    def test_get_products_of_a_snap(self):
        query_full = {"offset": "", "offset_id": "", "limit": "40"}
        query_first = {"offset": "", "offset_id": "", "limit": "10"}
        query_second = {"offset": "", "offset_id": "", "limit": "10"}
        query_third = {"offset": "", "offset_id": "", "limit": "10"}
        query_last = {"offset": "", "offset_id": "", "limit": "10"}
        result_full = self.user.get_products_of_a_snap('5114', query_full)

    def test_get_comment_of_a_snap_checking(self, id):
        query_full = {"offset": "", "offset_id": "", "limit": "40"}
        query_first = {"offset": "", "offset_id": "", "limit": "10"}
        query_second = {"offset": "", "offset_id": "", "limit": "10"}
        query_third = {"offset": "", "offset_id": "", "limit": "10"}
        query_last = {"offset": "", "offset_id": "", "limit": "10"}
        result_full = self.user.get_snap_comment(id, query_full)
        # print(len(result_full))
        # query_second['offset_id'] = result_full[int(len(result_full) / 4 - 1)]
        # query_third['offset_id'] = result_full[int(len(result_full) / 2 - 1)]
        # query_last['offset_id'] = result_full[int(len(result_full) * 3 / 4 - 1)]
        # assert result_full == self.user.get_snap_comment(id, query_first) + self.user.get_snap_comment(id,
        #     query_second) + self.user.get_snap_comment(id, query_third) + self.user.get_snap_comment(id, query_last)

    def test_create_snap(self):
        image_path = "../img/768px-Python-logo-notext.svg.png"
        with open(image_path, "rb") as image_file:
            encoded_string = "data:img/" + imghdr.what(image_path) + ";base64," + base64.b64encode(image_file.read()).decode('utf-8')
        snap_cre = [
            {
                "title": "Logo",
                "description": "python Logo",
                "image_name": "python",
                "image_body": "data:image/jpeg;base64,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",
                "ref_id": "1"
            }
        ]
        print(snap_cre)
        self.user.create_snaps(snap_cre)
        # snap.get_single_snap("7749")
        query_snap = {}


# test_follow_a_user()
# test_get_snap_order()
# test().test_search_snap_checking_order_by_creation()
test().test_get_comment_of_a_snap_checking("7740")
