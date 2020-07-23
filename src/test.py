import base64
import datetime
import imghdr
import json
import unittest

import requests

from src.User import User


class complex_test(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        self.user = User("test3@gmail.com", "12345678", "12345")
        self.user2 = User("test2@gmail.com", "12345678", "12345")
        self.user3 = User("celia5@abc.com", "12345678", "12345")
        self.login = self.user.login()
        self.login_result = json.loads(self.login.content.decode('utf-8'))
        self.login2 = self.user2.login()
        self.user3.login()
        self.image_path = "img/example_image_10kB.jpg"


    def test_login_and_logout(self):
        # Check the user login request successfully
        assert self.login.status_code == 200, "Expected Status code is 200 but the status code is " + str(
            self.login.status_code)
        # Check the token and user_id are gotten from the login response successfully
        assert self.login_result['token'] is not None and self.login_result[
            'user_id'] > 0, "Expected token and user_id exist but they are None"
        # Logout the user
        result_logout = self.user.logout()
        result_logout_json = json.loads(result_logout.content.decode('utf-8'))
        # Check the logout request successfully and ensure the logout return token is null
        assert result_logout.status_code == 200, "Expected Status code is 200 but the status code is " + str(
            self.result_logout.status_code)
        assert result_logout_json['token'] is None
        self.user.login()

    def test_get_snap_checking_order_by_creation(self):
        # Define 1 query with limit 40 order by creation in descending
        query_full = {"filter": "", "offset": "", "offset_id": "", "limit": "40", "order": "DESC",
                      "orderby": "creation"}
        # Define 4 queries with limit 10 order by creation in descending
        query_first = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                       "orderby": "creation"}
        query_second = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                        "orderby": "creation"}
        query_third = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                       "orderby": "creation"}
        query_last = {"filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                      "orderby": "creation"}
        # Get 40 snaps and check the status is 200
        result_full = self.user.get_snaps(query_full)
        assert result_full['response'].status_code == 200, "Expected Status code is 200 but the status code is " + str(
            self.login.status_code)
        result_full_list = self.user.get_snaps(query_full)['list']
        # The offset_id will be defined with the 0th, 10th, 20th and 30th items from the above query
        query_second['offset_id'] = result_full_list[int(len(result_full_list) / 4 - 1)]
        query_third['offset_id'] = result_full_list[int(len(result_full_list) / 2 - 1)]
        query_last['offset_id'] = result_full_list[int(len(result_full_list) * 3 / 4 - 1)]
        # Combine the 4 queries result in one list
        result_list_combine = self.user.get_snaps(query_first)['list'] + self.user.get_snaps(query_second)['list'] + self.user.get_snaps(query_third)['list'] + self.user.get_snaps(query_last)['list']
        # Compare the results from two types of query are the same
        assert result_full_list == result_list_combine, "The results are not the same. Full Result with limit 40: " + result_full_list + ". Full Result of 4 queries with limit 10: " + result_list_combine

    def test_create_snap(self):
        # Create a snap with image body
        snap_cre = [{
            "title": "Dress" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S"),
            "description": "Flowered Dress",
            "image_name": "Example",
            "image_body": self.user.get_encode_base64_image(self.image_path),
            "ref_id": "1"
        }]
        result_created = json.loads(self.user.create_snaps(snap_cre).content.decode('utf-8'))
        # Check the return image path exist
        assert result_created['results'][0]['image_path'] is not None, "The image path is null"
        snap_id_testing = str(result_created['results'][0]['snap_id'])
        # Get a single snap by the snap_id from the created snap result
        result_get = json.loads(self.user.get_single_snap(snap_id_testing).content.decode('utf-8'))
        assert result_created['results'][0]['image_path'] == result_get['image_path'], "The image path are not the same"
        # Get the snap by user id and check the result contains the created snap by snap_id
        result_get_user_snap = self.user.get_user_snap_of_a_user(self.user.get_user_id())
        assert int(snap_id_testing) in result_get_user_snap[
            'list_user_id'], "The expected created snap id" + snap_id_testing + " is not in the list from get_snap of a user" + \
                             result_get_user_snap['list_user_id']
        # Remove the snap and check the remove request successfully
        result_remove = self.user.remove_snap(snap_id_testing)
        assert result_remove.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_remove.status_code)

    def test_get_products_of_a_snap(self):
        # Get the products result by the snap_id
        snap_id = '7790'
        result_get_products = self.user.get_products_of_a_snap(snap_id)
        # Check the get requested successfully
        assert result_get_products['response'].status_code == 200
        # Check the snap_id from the results is the same with searched snap_id
        assert all(i == int(snap_id) for i in
                   result_get_products['list_snap_id']), "An snap_id of the item in the product of a snap result list" + \
                                                         result_get_products['list_snap_id'] + " is not " + snap_id

    def test_search_snap_checking_order_by_creation(self):
        # Define 1 query with limit 40 order by creation in descending
        query_full = {"q": "A", "limit": "40", "order": "DESC", "orderby": "creation"}
        # Define 4 queries with limit 10 order by creation in descending
        query_first = {"q": "A", "limit": "10", "order": "DESC", "orderby": "creation"}
        query_second = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                        "orderby": "creation"}
        query_third = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                       "orderby": "creation"}
        query_last = {"q": "A", "filter": "", "offset": "", "offset_id": "", "limit": "10", "order": "DESC",
                      "orderby": "creation"}
        # Get 40 snaps and check the search request successfully
        result_full = self.user.search_snaps(query_full)
        assert result_full['response'].status_code == 200, "Expected Status code is 200 but the status code is " + str(
            self.result_full['response'].status_code)
        # The offset_id will be defined with the 0th, 10th, 20th and 30th items from the above query
        result_full_list = self.user.search_snaps(query_full)['list_snap_id']
        query_second['offset_id'] = result_full_list[int(len(result_full_list) / 4 - 1)]
        query_third['offset_id'] = result_full_list[int(len(result_full_list) / 2 - 1)]
        query_last['offset_id'] = result_full_list[int(len(result_full_list) * 3 / 4 - 1)]
        # Combine the 4 queries result in one list
        result_list_combine = self.user.search_snaps(query_first)['list_snap_id'] + \
                              self.user.search_snaps(query_second)['list_snap_id'] + \
                              self.user.search_snaps(query_third)['list_snap_id'] + self.user.search_snaps(query_last)[
                                  'list_snap_id']
        # Compare the results from two types of query are the same
        assert result_full_list == result_list_combine, "The results are not the same. Full Result with limit 40: " + result_full_list + ". Full Result of 4 queries with limit 10: " + result_list_combine

    def test_get_comment_of_a_snap_checking(self):
        # Get the comment of a snap
        snap_id = '7847'
        query = {"offset": "", "offset_id": "", "limit": "40"}
        result_get_comment = self.user.get_snap_comment(snap_id, query)
        # Check the get comment request successfully
        assert result_get_comment[
                   'response'].status_code == 200, "Expected Status code is 200 but the status code is " + str(
            self.result_get_comment.status_code)
        # Check the number of comment more than 0
        assert int(result_get_comment['json']['n_comment']) > 0, "There is no any comment in this snap"

    def test_snap_comment(self):
        comment = "Testing" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S")
        snap_id = '7796'
        result_post = self.user.post_comment(snap_id, comment)
        assert result_post.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_post.status_code)
        result_get = self.user.get_snap_comment('7796')
        assert result_get["response"].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get["response"].status_code)
        assert result_get['json']['comments'][0]['message'] == comment, "The post comment is not the same with the gotten one"

    # def test_collect_product_link_click(self):
    #     body =  {
    #         "snap_product_id": "12345",
    #         "platform_product_id": "12345",
    #         "url": "http://google.com.hk",
    #         "ip": "192.168.0.1"
    #     }
    #     result_collect = self.user.collect_product_link_click(body)

    def test_get_snap_info_after_login(self):
        # Define the query parameter for get_snap, search_snap, get_product
        user_id = '5166'
        snap_id = '7623'
        query = dict(snap_id_product='',
                     home=dict(snap_id='', offset_id='7806', limit="14", order="DESC", orderby="creation"),
                     search=dict(snap_id='', limit='14', order='DESC', orderby='creation'),
                     product=dict(offset_id="", limit="12"))
        # Get snap
        result_get_snap = self.user.get_user_snap_of_a_user(user_id, query['home'])
        assert result_get_snap['response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap['response'].status_code)
        # Search snap
        result_search_snap = self.user.search_snaps(query['search'])
        assert result_search_snap[
                   'response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_search_snap['response'].status_code)
        # Get product
        result_get_product = self.user.get_products_of_a_snap(snap_id, query['product'])
        assert result_get_product[
                   'response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_product['response'].status_code)
        # Assert the snap_id into the query from the above result
        query['home']['snap_id'] = str(result_get_snap['list_snap_id'][int(len(result_get_snap['list_snap_id']) - 1)])
        query['search']['snap_id'] = str(
            result_search_snap['list_snap_id'][int(len(result_search_snap['list_snap_id']) - 1)])
        query['snap_id_product'] = str(
            result_get_product['list_snap_id'][int(len(result_get_product['list_snap_id']) - 1)])
        # Get snap info after login
        result_get_snap_after_login = self.user.get_snap_info_after_login(query)
        assert result_get_snap_after_login.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap_after_login['response'].status_code)

    def test_remove_a_snap_product(self):
        self.user.remove_a_snap_product('6936')

    def test_get_snaps_by_snap_product_id(self):
        self.user.get_snaps_by_snap_product_id('6936', {})

    def test_get_user_profile(self):
        result_get_profile = self.user.get_user(self.user.get_user_id())
        print(result_get_profile)
        assert result_get_profile.status_code == 200, "Expected Status code: 200 but the status code: " + result_get_profile.status_code
        assert json.loads(result_get_profile.content.decode('utf-8'))['user_id'] == self.login_result[
            'user_id'], "The user id do not match"

    def test_change_password(self):
        # Check new password missing error
        result_change_new_missing = self.user.change_password('12345678', '', self.user.get_user_id())
        assert result_change_new_missing.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_change_new_missing.status_code)
        new_missing_error_code = json.loads(result_change_new_missing.content.decode('utf-8'))['error']['code']
        assert new_missing_error_code == 'MISSING_NEW_PASSWORD', "Expected Error code: MISSING_NEW_PASSWORD but the code: " + new_missing_error_code
        # Check current password missing error
        result_change_curr_missing = self.user.change_password('', '12345678', self.user.get_user_id())
        assert result_change_curr_missing.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_change_new_missing.status_code)
        result_change_curr_missing = json.loads(result_change_curr_missing.content.decode('utf-8'))['error']['code']
        assert result_change_curr_missing == 'MISSING_CURR_PASSWORD', "Expected Error code: MISSING_CURR_PASSWORD but the code: " + result_change_curr_missing
        # Check the correct change password
        result_change_diff = self.user.change_password('12345678', '12345677', self.user.get_user_id())
        assert result_change_diff.status_code == 200, "Expected Status code: 400 but the status code: " + str(
            result_change_diff.status_code)
        result_change_diff = self.user.change_password('12345677', '12345678', self.user.get_user_id())
        assert result_change_diff.status_code == 200, "Expected Status code: 400 but the status code: " + str(
            result_change_diff.status_code)

    def test_user_profile(self):
        profile_update = {
            "firstname": "Testing",
            "lastname": "testing"
        }
        encoded_image = self.user.get_encode_base64_image(self.image_path)
        # Update the user profile - firstname & lastname
        result_prof_update = self.user.update_user( self.user.get_user_id(), profile_update)
        assert result_prof_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_prof_update.status_code)
        # Update the user profile picture
        result_prof_pir_update = self.user.upload_user_profile_pic(self.user.get_user_id(), 'Testing', encoded_image)
        assert result_prof_pir_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_prof_pir_update.status_code)
        # Get the user profile to check the update successfully or not
        result_prof_get = self.user.get_user(self.user.get_user_id())
        assert result_prof_get.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_prof_get.status_code)
        result_prof_get_json = json.loads(result_prof_get.content.decode('utf-8'))
        assert result_prof_get_json['firstname'] == profile_update['firstname'], "The firstname is wrong"
        assert result_prof_get_json['lastname'] == profile_update['lastname'], "The lastname is wrong"
        assert result_prof_get_json['user_propic'] is not None, "The user_propic is null"
        # Delete the profile picture
        result_prof_pir_remove = self.user.remove_user_profile_pic(self.user.get_user_id())
        assert result_prof_pir_remove.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_prof_pir_remove.status_code)
        # Get the user profile again to check the profile deleted or not
        assert json.loads(self.user.get_user(self.user.get_user_id()).content.decode('utf-8'))[
                   'user_propic'] is None, "The profile pic is not removed"

    def test_count_user_follower_and_following(self):
        # Get user follower and following count and check request sent successfully
        result_count = self.user.count_user_follower_and_following()
        assert result_count.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_count.status_code)
        # Get follower and following count from user profile
        result_count_json = json.loads(result_count.content.decode('utf-8'))
        result_profile = self.user.get_user(self.user.get_user_id())
        assert result_profile.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_profile.status_code)
        result_profile_json = json.loads(result_profile.content.decode('utf-8'))
        # Compare two results from the above requests
        assert result_count_json['n_follower'] == result_profile_json['n_follower'], "user follower do not match"
        assert result_count_json['n_following'] == result_profile_json['n_following'], "user following do not match"

    def test_follow_a_user(self):
        # User2 post the follow request to the User
        self.user2.follow_user(self.user2.get_user_id(), self.user.get_user_id())
        # User2 get the following result and check User2 follow User successfully by user_id
        assert str(json.loads(self.user2.get_following(self.user2.get_user_id()).content.decode('utf-8'))['following'][0][
                       'user_id']) == self.user.get_user_id()
        # User get the follower result and check User2 follow User successfully by user_id
        assert str(json.loads(self.user.get_follower(self.user.get_user_id()).content.decode('utf-8'))['follower'][0][
                       'user_id']) == self.user2.get_user_id()
        result_user1_follower = int(
            json.loads(self.user.count_user_follower_and_following().content.decode('utf-8'))['n_follower'])
        assert result_user1_follower > 0
        result_unfollow = self.user2.unfollow_user(self.user2.get_user_id(), self.user.get_user_id())
        assert result_unfollow.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_unfollow.status_code)
        result_get_follower = json.loads(self.user.get_follower(self.user.get_user_id()).content.decode('utf-8'))['n_follower']
        assert int(result_get_follower) == result_user1_follower - 1, "The Expected follower should be " + str(
            result_user1_follower - 1) + " but the result is " + str(result_get_follower)

    def test_favourite_snap(self):
        # Add the favourite snap to check the update successfully or not
        snap_id = '7651'
        result_add_fav_snap = self.user.add_snap_to_favourite(self.user.get_user_id(), snap_id)
        assert result_add_fav_snap.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_add_fav_snap.status_code)
        # Get the favourite snap to check the update request sent successfully
        result_get_fav_snap = self.user.get_favourite_snaps(self.user.get_user_id())
        assert result_get_fav_snap[
                   'response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_fav_snap.status_code)
        assert int(snap_id) in result_get_fav_snap['snap_id_list'], "The snap is added to favourite unsuccessfully"
        # Delete the favourite snap
        result_remove_fav_snap = self.user.remove_snap_from_favourite(snap_id)
        assert result_remove_fav_snap.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_remove_fav_snap.status_code)
        # Get the favourite snap again to check the profile deleted or not
        result_get_fav_snap_again = self.user.get_favourite_snaps(self.user.get_user_id())
        assert int(snap_id) not in result_get_fav_snap_again['snap_id_list'], "The snap is added to favourite unsuccessfully"

    def test_favourite_product(self):
        # Add the favourite product to check the update successfully or not
        snap_product_id = '5'
        result_add_fav_prod = self.user.add_snap_product_to_favourite(snap_product_id)
        assert result_add_fav_prod.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_add_fav_prod.status_code)
        # Get the favourite product to check the update successfully or not
        result_get_fav_prod = self.user.get_favourite_products()
        assert result_get_fav_prod[
                   'response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_fav_prod.status_code)
        assert int(snap_product_id) in result_get_fav_prod[
            'snap_product_id_list'], "The snap product is added to favourite unsuccessfully"
        # Delete the favourite snap
        result_remove_fav = self.user.remove_snap_product_to_favourite(snap_product_id)
        assert result_remove_fav.status_code == 204
        # Get the favourite product again to check the profile deleted or not
        result_get_fav_prod_again = self.user.get_favourite_products()
        assert int(snap_product_id) not in result_get_fav_prod_again[
            'snap_product_id_list'], "The snap product is added to favourite unsuccessfully"

    def test_get_user_snap_of_a_user(self):
        # Get the user snap of user by user_id
        user_id = '5118'
        result_get_user_snap = self.user.get_user_snap_of_a_user(user_id)
        # Check the get request sent successfully
        assert result_get_user_snap[
                   'response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_user_snap['response'].status_code)
        # Check the result
        assert all(i == int(user_id) for i in
                   result_get_user_snap['list_user_id']), "An snap_id of the item in the product of a snap result list" + result_get_user_snap['list'] + " is not " + user_id

    def test_search_user(self):
        # Search the user with search word
        search_word = "howard2"
        result_search = self.user.search_user(search_word)
        # Check the get request sent successfully
        assert result_search['response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_search.status_code)
        # Check the search word match with username list
        assert search_word in result_search[
            'list'], "The search word (" + search_word + ") did not match with the username list " + str(
            result_search['list'])

    def test_forget_password(self):
        # Post a forget password request and check the request sent successfully
        username = 'test3@gmail.com'
        result_forget = self.user.forget_password(username)
        assert result_forget.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_forget.status_code)
        # result_forget_failure = self.user.forget_password("1233")
        # assert result_forget_failure == 400, "Expected Status code: 400 but the status code: " + str(result_forget_failure.status_code)

    def test_get_number_of_likes_of_a_user(self):
        # Get no. of likes of user by user_id
        user_id = "5118"
        result_get = self.user.get_number_of_likes_of_a_user(user_id)
        assert result_get.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get.status_code)
        assert int(json.loads(result_get.content.decode('utf-8'))['likes']) >= 0, "Cannot get the likes result"

    def test_report_user(self):
        # Post a report user request
        report_param = {
            "user_id": "5117",
            "report_type": "1",
            "remark": ""
        }
        result_report = self.user.report_user(report_param)
        # Check the report request sent successfully
        assert result_report.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_report.status_code)

    def test_check_username_valid(self):
        # Check username owned by myself
        result_self = self.user.check_user_valid(json.loads(self.user.get_user(self.user.get_user_id()).content.decode('utf-8'))['username'])
        result_self_json = json.loads(result_self.content.decode('utf-8'))
        # Check the check request sent successfully
        assert result_self.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_self.status_code)
        # Check the username is valid
        assert result_self_json['result'] is True, "Expected result is true but the result is " + str(
            result_self_json['result'])
        # Check a exist username from another user
        result_wrong = self.user.check_user_valid('test2')
        result_wrong_json = json.loads(result_wrong.content.decode('utf-8'))
        # Check the check request sent successfully
        assert result_self.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_self.status_code)
        # Check the username is invalid
        assert result_wrong_json['result'] is False, "Expected result is false but the result is " + str(
            result_wrong_json['result'])

    def test_get_privacy_policy(self):
        # Get the privacy policy
        result_privacy = self.user.get_privacy_policy()
        # Check the check request sent successfully
        assert result_privacy.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_privacy.status_code)
        # Check the data is null or not
        assert json.loads(result_privacy.content.decode('utf-8'))['policy'] is not None, "There is no policy data"

    def test_get_terms_and_condition(self):
        # Get the terms and condition
        result_terms = self.user.get_terms_and_conditions()
        # Check the check request sent successfully
        assert result_terms.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_terms.status_code)
        # Check the data is null or not
        assert json.loads(result_terms.content.decode('utf-8'))['terms'] is not None

    def test_get_getstart_background_image(self):
        # Get the getstart background image
        result_background = self.user.get_background_image()
        # Check the check request sent successfully
        assert result_background.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_background.status_code)
        result_background_json = json.loads(result_background.content.decode('utf-8'))['background']
        # Check the background image url valid
        assert requests.get(result_background_json['left']).status_code == 200, "The left url is not valid"
        assert requests.get(result_background_json['right']).status_code == 200, "The right url is not valid"

    def test_social_media_list(self):
        # Get the social media list
        result_media = self.user.get_social_media_list()
        # Check the check request sent successfully
        assert result_media.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_media.status_code)
        result_media_json = json.loads(result_media.content.decode('utf-8'))
        # Check the data length is 6
        assert len(
            result_media_json['platforms']) == 6, "Expected social media item number is 6 but the number is " + str(
            len(result_media_json['platforms']))

# test_follow_a_user()
# test_get_snap_order()
# test().test_search_snap_checking_order_by_creation()
