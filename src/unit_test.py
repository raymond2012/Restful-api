import datetime
import json
import unittest
import time

import pytest

from User import User
import constant as con


def test_login_status_code_200():
    user = User("test3@gmail.com", "12345677", "12345")
    result_login = user.login()
    assert result_login.status_code == 200, "Expected status code is 200 but the status code is " + str(
        result_login.status_code)


def test_login_status_code_400_by_missing_email():
    result_login = User("", "12345678", "12345").login()
    assert result_login.status_code == 400, "Expected Status Code is 400 but the status code is " + str(
        result_login.status_code)
    result_login_error_code = json.loads(result_login.content.decode('utf-8'))['error']['code']
    assert result_login_error_code == "MISSING_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_login_error_code


def test_login_status_code_400_by_missing_password():
    result_login = User("test3@gmail.com", "", "12345").login()
    assert result_login.status_code == 400, "Expected Status Code is 400 but the status code is " + str(
        result_login.status_code)
    result_login_error_code = json.loads(result_login.content.decode('utf-8'))['error']['code']
    assert result_login_error_code == "MISSING_PASSWORD", "Expected Error code is MISSING_PASSWORD but the error code is " + result_login_error_code


def test_login_status_code_400_by_invalid_email():
    for email in con.invalid_email_list:
        result_login = User(email, "12345678", "12345").login()
        assert result_login.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_login.status_code)
        result_login_error_code = json.loads(result_login.content.decode('utf-8'))['error']['code']
        assert result_login_error_code == "INVALID_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_login_error_code


def test_login_status_code_400_by_logged_in_google_before():
    pass


def test_login_status_code_404_by_unexisting_user():
    result_login = User(con.unexist_email, "12133", "123").login()
    assert result_login.status_code == 404, "Expected status code is 404 but the status code is " + str(
        result_login.status_code)
    result_login_error_code = json.loads(result_login.content.decode('utf-8'))['error']['code']
    assert result_login_error_code == "INVALID_PASSWORD", "Expected Error code is INVALID_EMAIL but the error code is " + result_login_error_code


def test_logout_status_code_200():
    user = User("test3@gmail.com", "12345678", "12345")
    user.login()
    result_logout = user.logout()
    assert result_logout.status_code == 200, "Expected status code is 200 but the status code is " + str(
        result_logout.status_code)


def test_logout_status_code_401_by_not_login():
    result_logout = User("test3@gmail.com", "12345678", "12345").logout()
    con.check_status_code_401_NOT_LOGIN(result_logout)

def test_register_status_code_200():
    result_register = User(datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", '12345').register(
        'Hong Kong')
    assert result_register.status_code == 200, "Expected status code is 200 but the status code is " + str(
        result_register.status_code)


def test_register_status_code_400_by_missing_email():
    result_register = User("", "12345678", '12345').register('Hong Kong')
    assert result_register.status_code == 400, "Expected status code is 400 but the status code is " + str(
        result_register.status_code)
    result_register_error_code = json.loads(result_register.content.decode('utf-8'))['error']['code']
    assert result_register_error_code == "MISSING_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_register_error_code


def test_register_status_code_400_by_missing_password():
    result_register = User("t23143567432@gmail.com", "", '12345').register('Hong Kong')
    assert result_register.status_code == 400, "Expected status code is 400 but the status code is " + str(
        result_register.status_code)
    result_register_error_code = json.loads(result_register.content.decode('utf-8'))['error']['code']
    assert result_register_error_code == "MISSING_PASSWORD", "Expected Error code is INVALID_EMAIL but the error code is " + result_register_error_code


def test_register_status_code_400_by_invalid_email():
    email_list = ['test8rtyuhygfd765403', '#!@1132']
    for email in email_list:
        result_register = User(email, "12345678", '12345').register('Hong Kong')
        assert result_register.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_register.status_code)
        result_register_error_code = json.loads(result_register.content.decode('utf-8'))['error']['code']
        assert result_register_error_code == "INVALID_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_register_error_code


def test_register_status_code_400_by_existing_email():
    result_register = User(datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", '12345').register(
        'Hong Kong')
    assert result_register.status_code == 400, "Expected status code is 400 but the status code is " + str(
        result_register.status_code)
    result_register_error_code = json.loads(result_register.content.decode('utf-8'))['error']['code']
    assert result_register_error_code == "EXIST_ALREADY", "Expected Error code is INVALID_EMAIL but the error code is " + result_register_error_code


class unit_api_testing(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # self.user = User("test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", "12345")
        # self.user.register()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        # self.user.update_user(self.user.get_user_id, constant.user_profile)
        self.user.create_snaps(con.get_snap_created_list(1))
        self.fav_snap_id = '7112'
        self.fav_product_id = '48'

    def tearDown(self) -> None:
        self.user.login()
        snap_id_result_list = self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id']
        for snap_id in snap_id_result_list:
            self.user.remove_snap(str(snap_id))
        result_logout = self.user.logout()
        assert result_logout.status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_logout.status_code)
        time.sleep(0.2)

    # @pytest.fixture(scope="class", autouse=True)
    # def register_a_new_account(self):
    #     self.user = User(datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", '12345')
    #     result_register = self.user.register()
    #     assert result_register.status_code == 200, "Expected status code is 201 but the status code is " + str(
    #         result_register.status_code)

    # # Set Delay time among unit test
    # def tearDown(self) -> None:
    #     time.sleep(0.2)
    #     self.user.login()

    def test_get_snap_status_code_200(self):
        result_get_snap = self.user.get_snaps(con.query_get_snap)
        assert result_get_snap[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_snap.status_code)

    def test_get_snap_status_code_200_by_null_params(self):
        result_get_snap = self.user.get_snaps({})
        assert result_get_snap[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_snap.status_code)

    def test_get_snap_status_code_500_by_invalid_order_param(self):
        result_get_snap = self.user.get_snaps(con.query_get_snap_invalid_param)
        assert result_get_snap['response'].status_code == 500, "Expected status code is 500 but the status code is " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap['response'].content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "GET_FAIL", "Expected Error code is MISSING_TITLE but the error code is " + result_get_snap_error_code

    def test_get_single_snap_status_code_200(self):
        snap_id = '7116'
        result_get_single_snap = self.user.get_single_snap(snap_id)
        assert result_get_single_snap.status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_single_snap.status_code)

    # Abnormal Cases for Get Single Snap
    def test_get_single_snap_status_code_400_by_missing_snap_id(self):
        snap_id = ''
        result_get_single_snap = self.user.get_single_snap(snap_id)
        assert result_get_single_snap.status_code == 400, "Expected status code is 400 but the status code is " + str(result_get_single_snap.status_code)
        result_get_single_snap_error_code = json.loads(result_get_single_snap.content.decode('utf-8'))['error']['code']
        assert result_get_single_snap_error_code == "MISSING_PARAMS", "Expected Error code is INVALID_EMAIL but the error code is " + result_get_single_snap_error_code

    # def test_get_single_snap_status_code_404_by_not_exist_snap_id(self):
    #     snap_id = 'abc'
    #     result_get_single_snap = self.user.get_single_snap(snap_id)
    #     assert result_get_single_snap.status_code == 404, "Expected status code is 404 but the status code is " + str(result_get_single_snap.status_code)
    #     result_get_single_snap_error_code = json.loads(result_get_single_snap.content.decode('utf-8'))['error']['code']
    #     print(result_get_single_snap.content)
    #     assert result_get_single_snap_error_code == "NOT_FOUND", "Expected Error code is INVALID_EMAIL but the error code is " + result_get_single_snap_error_code

    def test_create_snap_status_code_201(self):
        snap_cre = con.get_snap_created_list()
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 201, "Expected status code is 201 but the status code is " + str(
            result_created.status_code)

    def test_create_snap_status_code_400_by_missing_title(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['title'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_TITLE", "Expected Error code is MISSING_TITLE but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_description(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['description'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_DESCRIPTION", "Expected Error code is MISSING_DESCRIPTION but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_image_name(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['image_name'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_IMAGE_NAME", "Expected Error code is MISSING_IMAGE_NAME but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_image_body(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['image_body'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_IMAGE_BODY", "Expected Error code is MISSING_IMAGE_BODY but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_ref_id(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['ref_id'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_REF_ID", "Expected Error code is MISSING_REF_ID but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_413_by_over_10MB_image_size(self):
        snap_cre = con.get_snap_created_list()
        image_path_list = con.image_path_list_code_413
        for image_path in image_path_list:
            snap_cre[0]['image_body'] = con.get_encode_base64_image(image_path)
            result_created = self.user.create_snaps(snap_cre)
            assert result_created.status_code == 413, "Expected status code is 413 but the status code is " + str(
                result_created.status_code)
            result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
            assert result_created_snap_error_code == "IMAGE_SIZE_OVER_LIMIT", "Expected Error code is INVALID_EMAIL but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_image_size_over_limit(self):
        snap_cre = con.get_snap_created_list()
        image_path_list = con.image_path_list_code_400
        for image_path in image_path_list:
            snap_cre[0]['image_body'] = con.get_encode_base64_image(image_path)
            result_created = self.user.create_snaps(snap_cre)
            assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
                result_created.status_code)
            result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
            assert result_created_snap_error_code == "IMAGE_SIZE_OVER_LIMIT", "Expected Error code is IMAGE_SIZE_OVER_LIMIT but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_401_by_not_login(self):
        snap_cre = con.get_snap_created_list()
        self.user.logout()
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_401_NOT_LOGIN(result_created)

    def test_remove_snap_status_code_204(self):
        get_snap = self.user.get_user_snaps_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        result_remove = self.user.remove_snap(snap_id_remove)
        assert result_remove.status_code == 204, "Expected status code is 204 but the status code is " + str(
            result_remove.status_code)

    def test_remove_snap_status_code_404_by_missing_snap_id(self):
        snap_id = con.missing_snap_id_remove_snap
        result_remove = self.user.remove_snap(snap_id)
        con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_snap_status_code_204_by_unexisting_snap_id(self):
        for snap_id in con.unexisting_snap_id_remove_snap_list:
            result_remove = self.user.remove_snap(snap_id)
            assert result_remove.status_code == 204, "Expected status code is 204 but the status code is " + str(
                result_remove.status_code)
            result_remove_snap_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
            assert result_remove_snap_error_code == "NOT_FOUND", "Expected Error code is MISSING_PARAMS but the error code is " + result_remove_snap_error_code

    def test_remove_snap_status_code_401_by_not_login(self):
        get_snap = self.user.get_user_snaps_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        self.user.logout()
        result_remove = self.user.remove_snap(snap_id_remove)
        con.check_status_code_401_NOT_LOGIN(result_remove)

    def test_get_product_of_a_snap_status_code_200(self):
        result_get_product = self.user.get_products_of_a_snap(con.snap_id_get_product_snap)
        assert result_get_product[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_product['response'].status_code)

    def test_get_product_of_a_snap_status_code_200_by_a_deleted_snap(self):
        # Get one Snap of myself
        get_snap = self.user.get_user_snaps_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        # Get product snap before deleting the snap
        result_get_product_before_delete = self.user.get_products_of_a_snap(snap_id_remove)
        assert result_get_product_before_delete['response'].status_code == 200, "Expected status code is 200 but the status code is " + str(result_get_product_before_delete['response'].status_code)
        result_product_list_before = result_get_product_before_delete["list_product_id"]
        # Remove the snap
        result_delete_snap = self.user.remove_snap(snap_id_remove)
        assert result_delete_snap.status_code == 204, "Expected status code is 204 but the status code is " + str(result_delete_snap['response'].status_code)
        # Get product snap after deleting the snap
        result_get_product_after_delete = self.user.get_products_of_a_snap(snap_id_remove)
        assert result_get_product_after_delete['response'].status_code == 200, "Expected status code is 200 but the status code is " + str(result_get_product_after_delete['response'].status_code)
        result_product_list_after = result_get_product_after_delete['list_product_id']
        # Compare the two result of getting product snap
        assert result_product_list_before == result_product_list_after, "The product id list before remove " + result_product_list_before + " is not the same with that after remove " + result_product_list_after

    def test_get_product_of_a_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_get_product_snap_list:
            result_get_product = self.user.get_products_of_a_snap(snap_id)
            con.check_status_code_404_NOT_FOUND(result_get_product)

    def test_search_snap_status_code_200(self):
        result_search_snap = self.user.search_snaps(con.search_snap_query)
        assert result_search_snap[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_search_snap['response'].status_code)

    def test_search_snap_status_code_200_by_empty_query(self):
        result_search_snap = self.user.search_snaps(con.empty_search_snap_query)
        assert result_search_snap[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_search_snap['response'].status_code)

    def test_search_snap_status_code_500_by_incorrect_order_parameter(self):
        result_search_snap = self.user.search_snaps(con.incorrect_search_snap_query)
        assert result_search_snap[
                   'response'].status_code == 500, "Expected status code is 500 but the status code is " + str(
            result_search_snap['response'].status_code)
        result_search_snap_error_code = json.loads(result_search_snap['response'].content.decode('utf-8'))['error'][
            'code']
        assert result_search_snap_error_code == "GET_FAIL", "Expected Error code is GET_FAIL but the error code is " + result_search_snap_error_code

    def test_get_comments_of_a_snap_status_code_200(self):
        result_get_comment = self.user.get_snap_comment(con.snap_id_post_comment)
        assert result_get_comment['response'].status_code == 200, "Expected status code is 200 but the status code is " + str(result_get_comment['response'].status_code)

    def test_get_comments_of_a_snap_status_code_200_by_a_deleted_snap(self):
        result_delete_snap = self.user.remove_snap(con.snap_id_post_comment)
        assert result_delete_snap.status_code == 204, "Expected status code is 204 but the status code is " + str(result_delete_snap['response'].status_code)
        result_get_comment = self.user.get_snap_comment(con.snap_id_post_comment)
        assert result_get_comment['response'].status_code == 200, "Expected status code is 200 but the status code is " + str(result_get_comment['response'].status_code)

    def test_get_comments_of_a_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_get_comments_list:
            result_get_comment = self.user.get_snap_comment(snap_id)
            con.check_status_code_404_NOT_FOUND(result_get_comment)

    def test_post_comment_status_code_201(self):
        result_post = self.user.post_comment(con.snap_id_post_comment, con.comment)
        assert result_post.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_post.status_code)

    def test_post_comment_status_code_201_by_a_deleted_snap(self):
        result_delete_snap = self.user.remove_snap(con.snap_id_post_comment)
        assert result_delete_snap.status_code == 204, "Expected status code is 204 but the status code is " + str(result_delete_snap['response'].status_code)
        result_post = self.user.post_comment(con.snap_id_post_comment, con.comment)
        assert result_post.status_code == 201, "Expected Status code: 201 but the status code: " + str(result_post.status_code)

    def test_post_comment_status_code_400_by_missing_comment(self):
        result_post = self.user.post_comment(con.snap_id_post_comment, con.missing_comment)
        assert result_post.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_post.status_code)
        result_post_error_code = json.loads(result_post.content.decode('utf-8'))['error']['code']
        assert result_post_error_code == "MISSING_MESSAGE", "Expected Error code is MISSING_MESSAGE but the error code is " + result_post_error_code

    def test_post_comment_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_post_comment_list:
            result_post = self.user.post_comment(snap_id, con.comment)
            con.check_status_code_404_NOT_FOUND(result_post)

    def test_post_comment_status_code_401_by_not_login(self):
        self.user.logout()
        result_post = self.user.post_comment(con.snap_id_post_comment, con.comment)
        con.check_status_code_401_NOT_LOGIN(result_post)

    def test_get_snap_info_after_login_status_code_200_by_all_dataset(self):
        result_get_snap = self.user.get_snap_info_after_login(con.query_get_snap_after_login)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_200_by_home_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_200_by_search_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'search'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_200_by_product_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'product'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_200_by_home_and_search_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home' or key == 'search'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_200_by_home_and_product_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home' or key == 'product'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_200_by_search_and_product_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'search' or key == 'product'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_home(self):
        query = con.query_get_snap_after_login
        query['home']['snap_id'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_search(self):
        query = con.query_get_snap_after_login
        query['search']['snap_id'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_product(self):
        query = con.query_get_snap_after_login
        query['snap_id_product'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    # Abnormal case for get snap info after login
    # def test_get_snap_info_after_login_status_code_400_by_invalid_snap_id_for_search(self):
    #     query = self.query_get_snap_after_login
    #     query['search']['snap_id'] = "abc"
    #     result_get_snap = self.user.get_snap_info_after_login(query)
    #     assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
    #         result_get_snap.status_code)
    #     result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
    #     assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    def test_get_snap_info_after_login_status_code_401_by_not_login(self):
        query = con.query_get_snap_after_login
        self.user.logout()
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_401_NOT_LOGIN(result_get_snap)

    # Not find a suitable snap_product_id for testing the snap remove
    # def test_remove_a_snap_product_from_a_snap_status_code_204(self):
    #     snap_product_id = ''
    #     result_remove = self.user.remove_a_snap_product(snap_product_id)
    #     assert result_remove.status_code == 204, "Expected Status code: 204 but the status code: " + str(
    #         result_remove.status_code)

    def test_remove_a_snap_product_from_a_snap_status_code_204_by_unexisting_snap_product_id(self):
        result_remove = self.user.remove_a_snap_product(con.unexisting_snap_product_id_remove_snap_product)
        assert result_remove.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_remove.status_code)
        # result_remove_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        # assert result_remove_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_remove_error_code

    def test_remove_a_snap_product_from_a_snap_status_code_404_by_missing_snap_product_id(self):
        result_remove = self.user.remove_a_snap_product(con.missing_snap_product_id_remove_snap_product)
        con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_a_snap_product_from_a_snap_status_code_401_by_not_login(self):
        self.user.logout()
        result_remove = self.user.remove_a_snap_product(con.snap_product_id_remove_snap_product)
        con.check_status_code_401_NOT_LOGIN(result_remove)

    def test_get_snaps_product_by_snap_product_id_status_code_200(self):
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.snap_product_id_get_snap_product)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snaps_product_by_snap_product_id_status_code_200_by_deleted_snap_product_id(self):
        result_remove = self.user.remove_a_snap_product(con.snap_product_id_get_snap_product_deleted)
        assert result_remove.status_code == 204, "Expected Status code: 204 but the status code: " + str(result_remove.status_code)
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.snap_product_id_get_snap_product_deleted)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snaps_product_by_snap_product_id_status_code_404_by_unexsiting_snap_product_id(self):
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.unexisting_snap_product_id_get_snap_product)
        con.check_status_code_404_NOT_FOUND(result_get_snap)

    def test_get_snaps_product_by_snap_product_id_status_code_404_by_missing_snap_product_id(self):
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.missing_snap_product_id_get_snap_product)
        con.check_status_code_404_NOT_FOUND(result_get_snap)

    def test_get_user_status_code_200_by_self(self):
        result_get_user = self.user.get_user(self.user.get_user_id())
        assert result_get_user.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_user.status_code)

    def test_get_user_status_code_200_by_another_user(self):
        for user_id in con.user_id_get_user_list:
            result_get_user = self.user.get_user(user_id)
            assert result_get_user.status_code == 200, "Expected Status code: 200 but the status code: " + str(
                result_get_user.status_code)

    def test_get_user_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_user_list:
            result_get_user = self.user.get_user(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_user)

    def test_change_password_status_code_200(self):
        result_change_password = self.user.change_password(self.user.get_password(), con.new_password, self.user.get_user_id())
        assert result_change_password.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_change_password.status_code)

    def test_change_password_status_code_400_by_missing_current_password(self):
        result_change_password = self.user.change_password(con.missing_password, con.new_password, self.user.get_user_id())
        assert result_change_password.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_change_password.status_code)
        result_change_password_error_code = json.loads(result_change_password.content.decode('utf-8'))['error']['code']
        assert result_change_password_error_code == "MISSING_CURR_PASSWORD", "Expected Error code is MISSING_CURR_PASSWORD but the error code is " + result_change_password_error_code

    def test_change_password_status_code_400_by_missing_new_password(self):
        result_change_password = self.user.change_password(self.user.get_password(), con.missing_password, self.user.get_user_id())
        assert result_change_password.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_change_password.status_code)
        result_change_password_error_code = json.loads(result_change_password.content.decode('utf-8'))['error']['code']
        assert result_change_password_error_code == "MISSING_NEW_PASSWORD", "Expected Error code is MISSING_NEW_PASSWORD but the error code is " + result_change_password_error_code

    def test_change_password_status_code_400_by_invalid_new_password(self):
        for password in con.invalid_password_list:
            result_change_password = self.user.change_password(self.user.get_password(), password, self.user.get_user_id())
            assert result_change_password.status_code == 400, "Expected Status code: 400 but the status code: " + str(
                result_change_password.status_code)
            result_change_password_error_code = json.loads(result_change_password.content.decode('utf-8'))['error']['code']
            assert result_change_password_error_code == "INVALID_NEW_PASSWORD", "Expected Error code is MISSING_NEW_PASSWORD but the error code is " + result_change_password_error_code

    def test_change_password_status_code_403_by_unauthorized_user_id(self):
        result_change_password = self.user.change_password(self.user.get_password(), con.new_password, con.unauthorized_user_id)
        con.check_status_code_403_unauthorized(result_change_password)

    def test_change_password_status_code_401_by_not_login(self):
        self.user.logout()
        result_change_password = self.user.change_password(self.user.get_password(), con.new_password, self.user.get_user_id())
        con.check_status_code_401_NOT_LOGIN(result_change_password)

    def test_change_password_status_code_404_by_invalid_current_password(self):
        for password in con.invalid_password_list:
            result_change_password = self.user.change_password(password, con.new_password, self.user.get_user_id())
            con.check_status_code_404_NOT_FOUND(result_change_password)

    def test_update_user_profile_status_code_200(self):
        result_update = self.user.update_user(self.user.get_user_id(), con.query_profile)
        assert result_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_update.status_code)

    def test_update_user_profile_status_code_400_by_invalid_username(self):
        for query_profile in con.invalid_username_query_profile_list:
            result_update = self.user.update_user(self.user.get_user_id(), query_profile)
            assert result_update.status_code == 400, "Expected Status code: 400 but the status code: " + str(
                result_update.status_code)
            result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
            assert result_update_error_code == "INVALID_USERNAME", "Expected Error code is INVALID_USERNAME but the error code is " + result_update_error_code

    def test_update_user_profile_status_code_400_by_invalid_bio(self):
        result_update = self.user.update_user(self.user.get_user_id(), con.invalid_bio_query_profile)
        assert result_update.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "INVALID_BIO", "Expected Error code is INVALID_USERNAME but the error code is " + result_update_error_code

    def test_update_user_profile_status_code_401_by_not_login(self):
        self.user.logout()
        result_update = self.user.update_user(self.user.get_user_id(), con.query_profile)
        con.check_status_code_401_NOT_LOGIN(result_update)

    def test_update_user_profile_status_code_401_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_query_profile_list:
            result_update = self.user.update_user(user_id, con.query_profile)
            con.check_status_code_403_unauthorized(result_update)

    def test_update_user_profile_status_code_401_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_update = self.user.update_user(user_id, con.query_profile)
        con.check_status_code_403_unauthorized(result_update)

    def test_update_user_profile_picture_status_code_200(self):
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic, con.image_body_profile_pic)
        assert result_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_update.status_code)

    # Abnormal Case for update user profile picture
    # def test_update_user_profile_picture_status_code_200_by_4_5MB_image(self):
    #     image_name = "Testing"
    #     image_body = self.user.get_encode_base64_image(self.image_path_4_5MB)
    #     result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), image_name, image_body)
    #     assert result_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
    #         result_update.status_code)

    def test_update_user_profile_picture_status_code_400_by_missing_image_name(self):
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.missing_image_name_profile_pic, con.image_body_profile_pic)
        assert result_update.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "MISSING_IMAGE_NAME", "Expected Error code is MISSING_IMAGE_NAME but the error code is " + result_update_error_code

    def test_update_user_profile_picture_status_code_400_by_missing_image_body(self):
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic, con.missing_image_body_profile_pic)
        assert result_update.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "MISSING_IMAGE_BODY", "Expected Error code is MISSING_IMAGE_BODY but the error code is " + result_update_error_code

    def test_update_user_profile_picture_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_update = self.user.upload_user_profile_pic(user_id, con.image_name_profile_pic, con.image_body_profile_pic)
        con.check_status_code_403_unauthorized(result_update)

    def test_update_user_profile_picture_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_update = self.user.upload_user_profile_pic(user_id, con.image_name_profile_pic, con.image_body_profile_pic)
        con.check_status_code_401_NOT_LOGIN(result_update)

    def test_update_user_profile_picture_status_code_404_by_invalid_image_body(self):
        for image_body in con.invalid_user_id_query_profile_list:
            result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic, image_body)
            con.check_status_code_404_NOT_FOUND(result_update)

    def test_remove_user_profile_picture_status_code_204(self):
        self.test_update_user_profile_picture_status_code_200()
        result_remove = self.user.remove_user_profile_pic(self.user.get_user_id())
        assert result_remove.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_remove.status_code)

    def test_remove_user_profile_picture_status_code_401_by_invalid_user_id(self):
        self.test_update_user_profile_picture_status_code_200()
        for user_id in con.invalid_user_id_remove_profile_pic_list:
            result_remove = self.user.remove_user_profile_pic(user_id)
            con.check_status_code_403_unauthorized(result_remove)

    def test_remove_user_profile_picture_status_code_403_by_unauthorized_user_id(self):
        self.test_update_user_profile_picture_status_code_200()
        result_remove = self.user.remove_user_profile_pic(con.unauthorized_user_id)
        con.check_status_code_403_unauthorized(result_remove)

    def test_remove_user_profile_picture_status_code_401_by_not_login(self):
        self.test_update_user_profile_picture_status_code_200()
        self.user.logout()
        result_remove = self.user.remove_user_profile_pic(self.user.get_user_id())
        con.check_status_code_401_NOT_LOGIN(result_remove)

    def test_forget_password_status_code_200(self):
        email = self.user.get_email()
        result_forget = self.user.forget_password(email)
        assert result_forget.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_forget.status_code)

    def test_forget_password_status_code_400_by_missing_email(self):
        result_forget = self.user.forget_password(con.missing_email_forget_pass)
        assert result_forget.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_forget.status_code)
        result_forget_error_code = json.loads(result_forget.content.decode('utf-8'))['error']['code']
        assert result_forget_error_code == "MISSING_EMAIL", "Expected Error code is NOT_LOGIN but the error code is " + result_forget_error_code

    def test_forget_password_status_code_400_by_invalid_email(self):
        for email in con.invalid_email_forget_pass:
            result_forget = self.user.forget_password(email)
            assert result_forget.status_code == 200, "Expected Status code: 400 but the status code: " + str(
                result_forget.status_code)

    def test_report_a_user_status_code_201(self):
        report_param = con.report_user_param
        result_report = self.user.report_user(report_param)
        assert result_report.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_report.status_code)

    def test_report_a_user_status_code_201_by_not_login(self):
        report_param = con.report_user_param
        self.user.logout()
        result_report = self.user.report_user(report_param)
        assert result_report.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_report.status_code)
        self.user.login()

    def test_report_a_user_status_code_201_by_self_user_id(self):
        report_param = con.report_user_param
        report_param['user_id'] = self.user.get_user_id()
        result_report = self.user.report_user(report_param)
        assert result_report.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_report.status_code)

    def test_report_a_user_status_code_201_by_missing_report_type(self):
        report_param = con.report_user_param
        report_param['report_type'] = con.missing_report_type
        result_report = self.user.report_user(report_param)
        assert result_report.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_report.status_code)
        result_report_error_code = json.loads(result_report.content.decode('utf-8'))['error']['code']
        assert result_report_error_code == "MISSING_REPORT_TYPE", "Expected Error code is NOT_LOGIN but the error code is " + result_report_error_code

    def test_report_a_user_status_code_400_by_invalid_report_type(self):
        report_param = con.report_user_param
        for report_type in con.invalid_report_type_list:
            report_param['report_type'] = report_type
            result_report = self.user.report_user(report_param)
            assert result_report.status_code == 400, "Expected Status code: 400 but the status code: " + str(
                result_report.status_code)
            result_report_error_code = json.loads(result_report.content.decode('utf-8'))['error']['code']
            assert result_report_error_code == "INVALID_REPORT_TYPE", "Expected Error code is NOT_LOGIN but the error code is " + result_report_error_code

    def test_report_a_user_status_code_400_by_missing_user_id(self):
        report_param = self.report_user_param
        report_param['user_id'] = con.missing_user_id
        result_report = self.user.report_user(report_param)
        assert result_report.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_report.status_code)
        result_report_error_code = json.loads(result_report.content.decode('utf-8'))['error']['code']
        assert result_report_error_code == "MISSING_USER_ID", "Expected Error code is NOT_LOGIN but the error code is " + result_report_error_code

    def test_report_a_user_status_code_404_by_invalid_user_id(self):
        report_param = con.report_user_param
        for user_id in con.invalid_user_id_list:
            report_param['user_id'] = user_id
            result_report = self.user.report_user(report_param)
            con.check_status_code_404_NOT_FOUND(result_report)

    def test_check_username_valid_or_not_status_code_200_by_self_username(self):
        username = self.user.get_username()
        result_check_username = self.user.check_user_valid(username)
        assert result_check_username.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_check_username.status_code)

    def test_check_username_valid_or_not_status_code_200_by_unexisting_username(self):
        for username in con.unexisting_username_list:
            result_check_username = self.user.check_user_valid(username)
            assert result_check_username.status_code == 200, "Expected Status code: 200 but the status code: " + str(
                result_check_username.status_code)

    def test_check_username_valid_or_not_status_code_400_by_invalid_username(self):
        for username in con.invalid_username_list:
            result_check_username = self.user.check_user_valid(username)
            assert result_check_username.status_code == 400, "Expected Status code: 400 but the status code: " + str(
                result_check_username.status_code)
            result_check_username_error_code = json.loads(result_check_username.content.decode('utf-8'))['error'][
                'code']
            assert result_check_username_error_code == "INVALID_USERNAME", "Expected Error code is INVALID_USERNAME but the error code is " + result_check_username_error_code

    def test_check_username_valid_or_not_status_code_401_by_not_login(self):
        username = self.user.get_username()
        self.user.logout()
        result_check_username = self.user.check_user_valid(username)
        con.check_status_code_401_NOT_LOGIN(result_check_username)

    def test_get_privacy_policy_status_code_200(self):
        result_privacy = self.user.get_privacy_policy()
        assert result_privacy.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_privacy.status_code)

    def test_get_terms_and_condition_status_code_200(self):
        result_terms = self.user.get_terms_and_conditions()
        assert result_terms.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_terms.status_code)

    def test_get_getstart_background_image_status_code_200(self):
        result_background = self.user.get_background_image()
        assert result_background.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_background.status_code)

    def test_social_media_list_status_code_200(self):
        result_media = self.user.get_social_media_list()
        assert result_media.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_media.status_code)


class follow_test(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # self.user = User(con.testing_email, con.testing_password, con.testing_device_id)
        # self.user.register()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        # self.user_follow = User(con.follow_target_email, con.follow_target_password, con.follow_target_device_id)
        # self.user_follow.register()
        self.user_follow = User("follow_target@gmail.com", "12345678", "12345")
        self.user_follow.login()

    def tearDown(self) -> None:
        self.user.login()
        self.user.get_following(self.user.get_user_id())
        self.user.unfollow_user(self.user.get_user_id(), self.user_follow.get_user_id())
        self.user.get_following(self.user.get_user_id())
        self.user.logout()
        self.user_follow.logout()
        time.sleep(0.2)

    def test_follow_a_user_status_code_201(self):
        user_id = self.user.get_user_id()
        target_user_id = self.user_follow.get_user_id()
        result_follow = self.user.follow_user(user_id, target_user_id)
        assert result_follow.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_follow.status_code)

    def test_follow_a_user_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        target_user_id = self.user_follow.get_user_id()
        self.user.logout()
        result_follow = self.user.follow_user(user_id, target_user_id)
        con.check_status_code_401_NOT_LOGIN(result_follow)

    def test_follow_a_user_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        target_user_id = self.user_follow.get_user_id()
        result_follow = self.user.follow_user(user_id, target_user_id)
        con.check_status_code_403_unauthorized(result_follow)

    def test_follow_a_user_status_code_404_by_invalid_user_id(self):
        user_id = self.user.get_user_id()
        for target_user_id in con.invalid_target_user_id_list:
            result_follow = self.user.follow_user(user_id, target_user_id)
            con.check_status_code_404_NOT_FOUND(result_follow)

    def test_unfollow_a_user_status_code_204(self):
        user_id = self.user.get_user_id()
        target_user_id = self.user_follow.get_user_id()
        result_unfollow = self.user.unfollow_user(user_id, target_user_id)
        assert result_unfollow.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_unfollow.status_code)

    def test_unfollow_a_user_status_code_404_by_invalid_user_id(self):
        user_id = self.user.get_user_id()
        for target_user_id in con.invalid_target_user_id_list:
            result_unfollow = self.user.unfollow_user(user_id, target_user_id)
            con.check_status_code_404_NOT_FOUND(result_unfollow)

    def test_unfollow_a_user_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        target_user_id = self.user_follow.get_user_id()
        result_unfollow = self.user.unfollow_user(user_id, target_user_id)
        con.check_status_code_403_unauthorized(result_unfollow)

    def test_unfollow_a_user_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        target_user_id = self.user_follow.get_user_id()
        self.user.logout()
        result_unfollow = self.user.unfollow_user(user_id, target_user_id)
        con.check_status_code_401_NOT_LOGIN(result_unfollow)

    def test_get_follower_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_follower = self.user.get_follower(user_id)
        assert result_get_follower.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_follower.status_code)

    def test_get_follower_status_code_200_by_not_login(self):
        user_id = self.user.get_user_id()
        result_get_follower = self.user.get_follower(user_id)
        self.user.logout()
        assert result_get_follower.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_follower.status_code)

    def test_get_follower_status_code_200_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_get_follower = self.user.get_follower(user_id)
        assert result_get_follower.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_follower.status_code)

    def test_get_follower_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_follower_list:
            result_get_follower = self.user.get_follower(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_follower)

    def test_get_following_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_following = self.user.get_following(user_id)
        assert result_get_following.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_following.status_code)

    def test_get_following_status_code_200_by_not_login(self):
        user_id = self.user.get_user_id()
        result_get_following = self.user.get_following(user_id)
        self.user.logout()
        assert result_get_following.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_following.status_code)

    def test_get_following_status_code_200_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_get_following = self.user.get_following(user_id)
        assert result_get_following.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_following.status_code)

    def test_get_following_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_following_list:
            result_get_following = self.user.get_following(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_following)

    def test_get_following_user_snaps_status_code_200(self):
        self.test_follow_a_user_status_code_201()
        result_get = self.user.get_following_users_snaps()
        assert result_get.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get.status_code)

    def test_get_following_user_snaps_status_code_401_by_not_login(self):
        self.test_follow_a_user_status_code_201()
        self.user.logout()
        result_get = self.user.get_following_users_snaps()
        con.check_status_code_401_NOT_LOGIN(result_get)


class favourite_snap_test(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # self.user = User(con.testing_email, con.testing_password, con.testing_device_id)
        # self.user.register()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        snap_list = self.user.search_snaps(dict(limit=5))["list_snap_id"]
        print(snap_list)
        for snap in snap_list:
            self.user.add_snap_to_favourite(self.user.get_user_id(), str(snap))
        self.fav_snap_id = str(self.user.search_snaps(dict(limit=1, order='ASC'))['list_snap_id'][0])

    def tearDown(self) -> None:
        self.user.login()
        fav_snap_list = self.user.get_favourite_snaps(self.user.get_user_id())['snap_id_list']
        print(fav_snap_list)
        for snap in fav_snap_list:
            self.user.remove_snap_from_favourite(self.user.get_user_id(), str(snap))
        # self.user.logout()
        time.sleep(0.2)

    def test_get_favourite_snaps_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_fav_snaps = self.user.get_favourite_snaps(user_id)
        assert result_get_fav_snaps[
                   'response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_fav_snaps['response'].status_code)

    def test_get_favourite_snaps_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_get_fav_snaps = self.user.get_favourite_snaps(user_id)
        con.check_status_code_401_NOT_LOGIN(result_get_fav_snaps)

    def test_get_favourite_snaps_status_code_401_by_invalid_user_id(self):
        user_id_list = [con.unauthorized_user_id, ' ', '12345678']
        for user_id in user_id_list:
            result_get_fav_snaps = self.user.get_favourite_snaps(user_id)
            con.check_status_code_403_unauthorized(result_get_fav_snaps)

    def test_add_a_snap_to_favourite_status_code_201(self):
        user_id = self.user.get_user_id()
        snap_id = self.fav_snap_id
        result_add_fav_snap = self.user.add_snap_to_favourite(user_id, snap_id)
        assert result_add_fav_snap.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_add_fav_snap.status_code)

    def test_add_a_snap_to_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        snap_id = self.fav_snap_id
        result_add_fav_snap = self.user.add_snap_to_favourite(user_id, snap_id)
        con.check_status_code_403_unauthorized(result_add_fav_snap)

    def test_add_a_snap_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        snap_id = self.fav_snap_id
        self.user.logout()
        result_add_fav_snap = self.user.add_snap_to_favourite(user_id, snap_id)
        con.check_status_code_401_NOT_LOGIN(result_add_fav_snap)

    def test_add_a_snap_to_favourite_status_code_404_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for snap_id in con.invalid_snap_id_fav_snap_list:
            result_add_fav_snap = self.user.add_snap_to_favourite(user_id, snap_id)
            con.check_status_code_404_NOT_FOUND(result_add_fav_snap)

    def test_remove_a_snap_from_favourite_status_code_204(self):
        user_id = self.user.get_user_id()
        snap_id = self.fav_snap_id
        result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, snap_id)
        assert result_remove_fav_snap.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_remove_fav_snap.status_code)

    def test_remove_a_snap_to_favourite_status_code_204_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for snap_id in con.invalid_snap_id_fav_snap_list:
            result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, snap_id)
            assert result_remove_fav_snap.status_code == 204, "Expected Status code: 204 but the status code: " + str(
                result_remove_fav_snap.status_code)

    def test_remove_a_snap_from_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        snap_id = self.fav_snap_id
        result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, snap_id)
        con.check_status_code_403_unauthorized(result_remove_fav_snap)

    def test_remove_a_snap_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        snap_id = self.fav_snap_id
        self.user.logout()
        result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, snap_id)
        con.check_status_code_401_NOT_LOGIN(result_remove_fav_snap)

    def test_get_snaps_of_a_user_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
        assert result_get_snaps['response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snaps['response'].status_code)

    def test_get_snaps_of_a_user_status_code_200_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
        assert result_get_snaps['response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snaps['response'].status_code)

    def test_get_snaps_of_a_user_status_code_200_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
        assert result_get_snaps['response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snaps['response'].status_code)

    def test_get_snaps_of_a_user_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_snap_id_get_user_snap_list:
            result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_snaps)

    def test_get_snaps_of_a_user_status_code_500_by_invalid_order_param(self):
        user_id = self.user.get_user_id()
        for query in con.invalid_query_get_user_snap:
            result_get_snaps = self.user.get_user_snaps_of_a_user(user_id, query)
            assert result_get_snaps['response'].status_code == 500, "Expected Status code: 500 but the status code: " + str(
                result_get_snaps['response'].status_code)
            result_get_snaps_error_code = json.loads(result_get_snaps['response'].content.decode('utf-8'))['error']['code']
            assert result_get_snaps_error_code == "GET_FAIL", "Expected Error code is GET_FAIL but the error code is " + result_get_snaps_error_code


class favourite_snap_product_test(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # snap_product_list = []
        # self.user = User(con.testing_email, con.testing_password, con.testing_device_id)
        # self.user.register()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        # snap_list = self.user.search_snaps(con.search_snap_query_fav)['list_snap_id']
        # print(snap_list)
        # for snap_id in snap_list:
        #     snap_product_list.append(self.user.get_products_of_a_snap(str(snap_id))['list_snap_product_id'])
        #     time.sleep(0.2)
        # print(snap_product_list)
        self.fav_product_id = con.fav_snap_id

    def tearDown(self) -> None:
        self.user.login()
        fav_snap_list = self.user.get_favourite_products(self.user.get_user_id())['snap_product_id_list']
        print(fav_snap_list)
        for snap in fav_snap_list:
            self.user.remove_snap_product_to_favourite(self.user.get_user_id(), str(snap))
        self.user.logout()
        time.sleep(0.2)

    def test_get_favourite_products_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_fav_products = self.user.get_favourite_products(user_id)
        assert result_get_fav_products[
                   'response'].status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_fav_products['response'].status_code)

    def test_get_favourite_products_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_get_fav_products = self.user.get_favourite_products(user_id)
        con.check_status_code_401_NOT_LOGIN(result_get_fav_products)

    def test_get_favourite_products_status_code_403_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_fav_product_list:
            result_get_fav_products = self.user.get_favourite_products(user_id)
            con.check_status_code_403_unauthorized(result_get_fav_products)

    def test_add_a_snap_product_to_favourite_status_code_201(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_product_id
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        assert result_add_fav_snap_product.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_add_fav_snap_product.status_code)

    def test_add_a_snap_product_to_favourite_status_code_201_by_deleted_snap_product(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.user.get_favourite_snaps(self.user.get_user_id())
        result_remove_snap_product = self.user.remove_a_snap_product(snap_product_id)
        assert result_remove_snap_product.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_remove_snap_product.status_code)
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        assert result_add_fav_snap_product.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_add_fav_snap_product.status_code)

    def test_add_a_snap_product_to_favourite_status_code_201_by_already_added(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_product_id
        for x in range(2):
            result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
            assert result_add_fav_snap_product.status_code == 201, "Expected Status code: 201 but the status code: " + str(
                result_add_fav_snap_product.status_code)

    # Not Finished delete snap function yet
    def test_add_a_snap_product_to_favourite_status_code_201_by_deleted_snap(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_product_id
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        assert result_add_fav_snap_product.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_add_fav_snap_product.status_code)

    def test_add_a_product_to_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        snap_product_id = self.fav_product_id
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_403_unauthorized(result_add_fav_snap_product)

    def test_add_a_product_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, self.fav_product_id)
        con.check_status_code_401_NOT_LOGIN(result_add_fav_snap_product)

    def test_add_a_product_to_favourite_status_code_401_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for snap_product_id in con.invalid_snap_id_add_fav_snap_product_list:
            result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
            con.check_status_code_404_NOT_FOUND(result_add_fav_snap_product)

    def test_remove_a_product_from_favourite_status_code_204(self):
        user_id = self.user.get_user_id()
        result_remove_fav_snap_product = self.user.remove_snap_product_to_favourite(user_id, self.fav_product_id)
        assert result_remove_fav_snap_product.status_code == 204, "Expected Status code: 204 but the status code: " + str(
            result_remove_fav_snap_product.status_code)

    def test_remove_a_product_to_favourite_status_code_204_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for snap_product_id in con.invalid_snap_id_remove_fav_snap_product_list:
            result_remove_fav_snap_product = self.user.remove_snap_product_to_favourite(user_id, snap_product_id)
            assert result_remove_fav_snap_product.status_code == 204, "Expected Status code: 204 but the status code: " + str(
                result_remove_fav_snap_product.status_code)

    def test_remove_a_product_from_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        snap_product_id = self.fav_product_id
        result_remove_fav_snap_product = self.user.remove_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_403_unauthorized(result_remove_fav_snap_product)

    def test_remove_a_product_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_product_id
        self.user.logout()
        result_remove_fav_snap_product = self.user.remove_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_401_NOT_LOGIN(result_remove_fav_snap_product)
