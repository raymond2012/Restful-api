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
        self.user = User("test3@gmail.com", "12345678", "12345")
        self.user2 = User("test2@gmail.com", "12345678", "12345")
        self.login = self.user.login()
        self.login2 = self.user2.login()
        self.image_path = "../img/example_image.jpg"

    def encode_base64_image(self,image_path):
        with open(self.image_path, "rb") as image_file:
            encoded_string = "data:image/" + imghdr.what(image_path) + ";base64," + base64.b64encode(
                image_file.read()).decode('utf-8')
        return encoded_string

    def json_result_to_snap_id_list(self, data):
        result = list(map(lambda x: x["snap_id"], json.loads(data.content.decode('utf-8'))))
        print(result)
        return result

    def test_authetication_login(self):
        login_result = json.loads(self.login.content.decode('utf-8'))
        assert self.r.status_code == 200, "Expected Status code is 200 but the status code is " + \
                                          str(self.login.status_code)
        assert login_result['token'] is not None and \
               login_result['user_id'] > 0, "Expected token and user_id exist but they are None"

    def test_get_user_profile(self):
        result = self.user.get_user()
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
        assert str(json.loads(self.user.count_user_follower_and_following().content.decode('utf-8'))[''])
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

    def test_get_comment_of_a_snap_checking(self):
        query = {"offset": "", "offset_id": "", "limit": "40"}
        self.user.get_snap_comment()

    def test_create_snap(self):
        snap_cre = {
            "title": "Dress" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S"),
            "description": "Flowered Dress",
            "image_name": "Example",
            "image_body": self.encode_base64_image("../img/example_image.jpg"),
            "ref_id": "1"
        }
        result_created = json.loads(self.user.create_snaps(snap_cre).content.decode('utf-8'))
        assert result_created['results'][0]['image_path'] is not None, "The image path is null"
        snap_id_testing = str(result_created['results'][0]['snap_id'])
        result_get = json.loads(self.user.get_single_snap(snap_id_testing).content.decode('utf-8'))
        assert result_created['results'][0]['image_path'] == result_get['image_path']
        result_remove = self.user.remove_snap(snap_id_testing)
        assert result_remove.status_code == 204


    def test_snap_comment(self):
        comment = "Testing" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S")
        result_post = self.user.post_comment('7796', comment)
        assert result_post.status_code == 201
        result_get = self.user.get_snap_comment('7796', {})
        assert result_get.status_code == 200, "Expected Status code: 200 but the status code: " + str(result_get.status_code)
        result_get_json = json.loads(result_get.content.decode('utf-8'))
        assert result_get_json['comments'][0]['message'] == comment, "The post comment is not the same with the gotten one"

    def test_user_profile(self):
        profile_update = {
            "firstname": "Testing",
            "lastname": "testing"
        }
        encoded_image = self.encode_base64_image("../img/example_image.jpg")
        # Update the user profile - firstname & lastname
        result_prof_update = self.user.update_user(profile_update)
        assert result_prof_update.status_code == 200
        # Update the user profile picture
        result_prof_pir_update = self.user.upload_user_profile_pic('Testing', encoded_image)
        assert result_prof_pir_update.status_code == 200
        # Get the user profile check the update successfully or not
        result_prof_get = self.user.get_user()
        assert result_prof_get.status_code == 200
        result_prof_get_json = json.loads(result_prof_get.content.decode('utf-8'))
        assert result_prof_get_json['firstname'] == profile_update['firstname']
        assert result_prof_get_json['lastname'] == profile_update['lastname']
        assert result_prof_get_json['user_propic'] is not None
        # Delete the profile Picture
        assert self.user.remove_user_profile_pic().status_code == 204
        # Get the user profile again to check the profile deleted or not
        assert json.loads(self.user.get_user().content.decode('utf-8'))['user_propic'] is None

    def test_favourite_snap(self):
        snap_id = '7112'
        result_add_fav_snap = self.user.add_snap_to_favourite(snap_id)
        assert result_add_fav_snap.status_code == 201
        result_get_fav_snap = self.user.get_favourite_snaps({})
        assert result_get_fav_snap.status_code == 200
        assert json.loads(result_get_fav_snap.content.decode('utf-8'))[0]['snap_id'] == snap_id
        result_remove_fav_snap = self.user.remove_snap_from_favourite(snap_id)
        assert result_remove_fav_snap.status_code == 204
        assert json.loads(result_get_fav_snap.content.decode('utf-8'))[0]['snap_id'] is not snap_id

    def test_favourite_product(self):
        snap_product_id = '5'
        result_add_fav_prod = self.user.add_snap_to_favourite(snap_product_id)
        assert result_add_fav_prod.status_code == 201
        result_get_fav_prod = self.user.get_favourite_products({})
        assert result_get_fav_prod.status_code == 200
        assert json.loads(result_get_fav_prod.content.decode('utf-8'))[0]['snap_product_id'] == snap_product_id
        result_remove_fav = self.user.remove_snap_product_to_favourite(snap_product_id)
        assert result_remove_fav.status_code == 204
        assert json.loads(result_remove_fav.content.decode('utf-8'))[0]['snap_product_id'] is not snap_product_id

    def test_forget_password(self):
        result_forget = self.user.forget_password('test3@gmail.com')
        assert result_forget.status_code == 200, "Expected Status code: 200 but the status code: " + str(result_forget.status_code)
        # result_forget_failure = self.user.forget_password("1233")
        # assert result_forget_failure == 400, "Expected Status code: 400 but the status code: " + str(result_forget_failure.status_code)

    def test_change_password(self):
        #Check new password missing error
        result_change_new_missing = self.user.change_password('12345678', '')
        assert result_change_new_missing.status_code == 400, "Expected Status code: 400 but the status code: " + str(result_change_new_missing.status_code)
        new_missing_error_code = json.loads(result_change_new_missing.content.decode('utf-8'))['error']['code']
        assert new_missing_error_code == 'MISSING_NEW_PASSWORD', "Expected Error code: MISSING_NEW_PASSWORD but the code: " + new_missing_error_code
        #Check current password missing error
        result_change_curr_missing = self.user.change_password('', '12345678')
        assert result_change_curr_missing.status_code == 400, "Expected Status code: 400 but the status code: " + str(result_change_new_missing.status_code)
        result_change_curr_missing = json.loads(result_change_curr_missing.content.decode('utf-8'))['error']['code']
        assert result_change_curr_missing == 'MISSING_CURR_PASSWORD', "Expected Error code: MISSING_CURR_PASSWORD but the code: " + result_change_curr_missing
        #Check the correct change password
        result_change_diff = self.user.change_password('12345678', '12345678')
        assert result_change_diff.status_code == 200, "Expected Status code: 400 but the status code: " + str(result_change_diff.status_code)

    def test_authetication_logout(self):
        result_logout = self.user.logout()
        result_logout_json = json.loads(result_logout.content.decode('utf-8'))
        assert result_logout.status_code == 200
        assert result_logout_json['token'] is None


# test_follow_a_user()
# test_get_snap_order()
# test().test_search_snap_checking_order_by_creation()
test().test_change_password()
