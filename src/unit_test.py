import datetime
import json
import unittest

from src.User import User


def test_login_status_code_200():
    user = User("test2@gmail.com", "12345677", "12345")
    result_login = user.login()
    assert result_login.status_code == 200, "Expected status code is 200 but the status code is " + str(
        result_login.status_code)


def test_login_status_code_400_by_missing_email_and_password():
    result_login = User().login()
    assert result_login.status_code == 400, "Expected Status Code is 400 but the status code is " + result_login.status_code
    result_login_error_code = json.loads(result_login.content.decode('utf-8'))['error']['code']
    assert result_login_error_code == "MISSING_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_login_error_code


def test_login_status_code_400_by_invalid_email_and_password():
    result_login = User("1235", "12133", "123").login()
    assert result_login.status_code == 400, "Expected status code is 400 but the status code is " + str(
        result_login.status_code)
    result_login_error_code = json.loads(result_login.content.decode('utf-8'))['error']['code']
    assert result_login_error_code == "INVALID_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_login_error_code


# def test_login_status_code_404_by_unexisting_user():
#     result_login = User("test8765403@gmail.com", "12133", "123").login()
#     assert result_login.status_code == 404, "Expected status code is 404 but the status code is " + str(
#         result_login.status_code)
#     result_login_error_code = json.loads(result_login.content.decode('utf-8'))['error']['code']
#     assert result_login_error_code == "INVALID_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_login_error_code


def test_logout_status_code_401_by_not_login_before():
    result_logout = User("test3@gmail.com", "12345678", "12345").logout()
    assert result_logout.status_code == 401, "Expected status code is 401 but the status code is " + str(
        result_logout.status_code)
    result_logout_error_code = json.loads(result_logout.content.decode('utf-8'))['error']['code']
    assert result_logout_error_code == "NOT_LOGIN", "Expected Error code is INVALID_EMAIL but the error code is " + result_logout_error_code


def test_register_status_code_200():
    result_register = User(datetime.datetime.now().strftime("%d%H%M%S") + "@gmail.com", "12345678", '12345').register(
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


def test_register_status_code_400_by_invalid_param():
    result_register = User("12345", "12345678", '12345').register('Hong Kong')
    assert result_register.status_code == 400, "Expected status code is 400 but the status code is " + str(
        result_register.status_code)
    result_register_error_code = json.loads(result_register.content.decode('utf-8'))['error']['code']
    assert result_register_error_code == "INVALID_EMAIL", "Expected Error code is INVALID_EMAIL but the error code is " + result_register_error_code


def test_register_status_code_400_by_existing_email():
    result_register = User("test3@gmail.com", "12345678", '12345').register('Hong Kong')
    assert result_register.status_code == 400, "Expected status code is 400 but the status code is " + str(
        result_register.status_code)
    result_register_error_code = json.loads(result_register.content.decode('utf-8'))['error']['code']
    assert result_register_error_code == "EXIST_ALREADY", "Expected Error code is INVALID_EMAIL but the error code is " + result_register_error_code


class unit_api_testing(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        self.user = User("test2@gmail.com", "12345677", "12345")
        self.user.login()
        self.image_path = "img/example_image.jpg"
        self.image_path_over_10MB = "img/example_image_11MB.jpg"
        self.image_path_9MB = "img/example_image_9MB.jpg"
        self.image_path_7MB = "img/example_image_7MB.jpg"
        # query template for create snap
        self.snap_created_template = [{
            "title": "Dress" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S"),
            "description": "Flowered Dress",
            "image_name": "Example",
            "image_body": self.user.get_encode_base64_image(self.image_path),
            "ref_id": "1"
        }]
        # query template for get snap info after login
        self.query_get_snap_after_login = dict(snap_id_product='8',
                                               home=dict(snap_id='7112', offset_id='7806', limit="14", order="DESC",
                                                         orderby="creation"),
                                               search=dict(snap_id='7744', limit='14', order='DESC',
                                                           orderby='creation'),
                                               product=dict(offset_id="", limit="12"))

    def test_logout_status_code_200(self):
        result_logout = self.user.logout()
        assert result_logout.status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_logout.status_code)
        self.user.login()

    def test_get_snap_status_code_200(self):
        query_get_snap = {"filter": "", "offset": "", "offset_id": "", "limit": "40", "order": "DESC",
                          "orderby": "creation"}
        result_get_snap = self.user.get_snaps(query_get_snap)
        assert result_get_snap[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_snap.status_code)

    def test_get_single_snap_status_code_200(self):
        snap_id = '7116'
        result_get_single_snap = self.user.get_single_snap(snap_id)
        assert result_get_single_snap.status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_single_snap.status_code)

    ### Abnormal Cases for Get Single Snap###
    # def test_get_single_snap_status_code_400_by_missing_snap_id(self):
    #     snap_id = ''
    #     result_get_single_snap = self.user.get_single_snap(snap_id)
    #     assert result_get_single_snap.status_code == 400, "Expected status code is 400 but the status code is " + str(result_get_single_snap.status_code)
    #     result_get_single_snap_error_code = json.loads(result_get_single_snap.content.decode('utf-8'))['error']['code']
    #     assert result_get_single_snap_error_code == "MISSING_PARAMS", "Expected Error code is INVALID_EMAIL but the error code is " + result_get_single_snap_error_code
    #
    # def test_get_single_snap_status_code_404_by_not_exist_snap_id(self):
    #     snap_id = 'abc'
    #     result_get_single_snap = self.user.get_single_snap(snap_id)
    #     assert result_get_single_snap.status_code == 404, "Expected status code is 404 but the status code is " + str(result_get_single_snap.status_code)
    #     result_get_single_snap_error_code = json.loads(result_get_single_snap.content.decode('utf-8'))['error']['code']
    #     print(result_get_single_snap.content)
    #     assert result_get_single_snap_error_code == "NOT_FOUND", "Expected Error code is INVALID_EMAIL but the error code is " + result_get_single_snap_error_code

    def test_create_snap_status_code_201(self):
        snap_cre = self.snap_created_template
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 201, "Expected status code is 201 but the status code is " + str(
            result_created.status_code)

    def test_create_snap_status_code_400_by_missing_title(self):
        snap_cre = self.snap_created_template
        snap_cre[0]['title'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_TITLE", "Expected Error code is MISSING_TITLE but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_description(self):
        snap_cre = self.snap_created_template
        snap_cre[0]['description'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_DESCRIPTION", "Expected Error code is MISSING_DESCRIPTION but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_image_name(self):
        snap_cre = self.snap_created_template
        snap_cre[0]['image_name'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_IMAGE_NAME", "Expected Error code is MISSING_IMAGE_NAME but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_image_body(self):
        snap_cre = self.snap_created_template
        snap_cre[0]['image_body'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_IMAGE_BODY", "Expected Error code is MISSING_IMAGE_BODY but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_missing_ref_id(self):
        snap_cre = self.snap_created_template
        snap_cre[0]['ref_id'] = ""
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "MISSING_REF_ID", "Expected Error code is MISSING_REF_ID but the error code is " + result_created_snap_error_code

    ### Abnormal Cases for Create Snap###
    # def test_create_snap_status_code_400_by_image_size_over_limit(self):
    #     snap_cre = self.snap_created_template
    #     snap_cre['image_body'] = self.user.get_encode_base64_image(self.image_path_over_10MB)
    #     result_created = self.user.create_snaps(snap_cre)
    #     assert result_created.status_code == 400, "Expected status code is 200 but the status code is " + str(
    #         result_created.status_code)
    #     result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
    #     assert result_created_snap_error_code == "IMAGE_SIZE_OVER_LIMIT", "Expected Error code is INVALID_EMAIL but the error code is " + result_created_snap_error_code

    # def test_create_snap_status_code_400_by_image_size_over_limit(self):
    #     snap_cre = self.snap_created_template
    #     snap_cre['image_body'] = self.user.get_encode_base64_image(self.image_path_9MB)
    #     result_created = self.user.create_snaps(snap_cre)
    #     assert result_created.status_code == 400, "Expected status code is 200 but the status code is " + str(
    #         result_created.status_code)
    #     result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
    #     assert result_created_snap_error_code == "IMAGE_SIZE_OVER_LIMIT", "Expected Error code is INVALID_EMAIL but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_400_by_image_size_over_limit(self):
        snap_cre = self.snap_created_template
        snap_cre[0]['image_body'] = self.user.get_encode_base64_image(self.image_path_7MB)
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 400, "Expected status code is 400 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "IMAGE_SIZE_OVER_LIMIT", "Expected Error code is IMAGE_SIZE_OVER_LIMIT but the error code is " + result_created_snap_error_code

    def test_create_snap_status_code_401_by_not_login(self):
        snap_cre = self.snap_created_template
        self.user.logout()
        # print(self.user.get_token())
        result_created = self.user.create_snaps(snap_cre)
        assert result_created.status_code == 401, "Expected status code is 401 but the status code is " + str(
            result_created.status_code)
        result_created_snap_error_code = json.loads(result_created.content.decode('utf-8'))['error']['code']
        assert result_created_snap_error_code == "NOT_LOGIN", "Expected Error code is NOT_LOGIN but the error code is " + result_created_snap_error_code
        self.user.login()

    def test_remove_snap_status_code_204(self):
        get_snap = self.user.get_user_snap_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        result_remove = self.user.remove_snap(snap_id_remove)
        assert result_remove.status_code == 204, "Expected status code is 204 but the status code is " + str(
            result_remove.status_code)

    def test_remove_snap_status_code_404_by_missing_snap_id(self):
        snap_id_remove = " "
        result_remove = self.user.remove_snap(snap_id_remove)
        assert result_remove.status_code == 404, "Expected status code is 404 but the status code is " + str(
            result_remove.status_code)
        result_remove_snap_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        assert result_remove_snap_error_code == "NOT_FOUND", "Expected Error code is MISSING_PARAMS but the error code is " + result_remove_snap_error_code

    def test_remove_snap_status_code_404_by_unexisting_snap_id(self):
        snap_id_remove = "abc"
        result_remove = self.user.remove_snap(snap_id_remove)
        assert result_remove.status_code == 404, "Expected status code is 404 but the status code is " + str(
            result_remove.status_code)
        result_remove_snap_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        assert result_remove_snap_error_code == "NOT_FOUND", "Expected Error code is MISSING_PARAMS but the error code is " + result_remove_snap_error_code

    def test_remove_snap_status_code_401_by_not_login(self):
        get_snap = self.user.get_user_snap_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        self.user.logout()
        result_remove = self.user.remove_snap(snap_id_remove)
        assert result_remove.status_code == 401, "Expected status code is 401 but the status code is " + str(
            result_remove.status_code)
        result_remove_snap_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        assert result_remove_snap_error_code == "NOT_LOGIN", "Expected Error code is NOT_LOGIN but the error code is " + result_remove_snap_error_code
        self.user.login()

    def test_get_product_of_a_snap_status_code_200(self):
        snap_id = "7112"
        result_get_product = self.user.get_products_of_a_snap(snap_id)
        assert result_get_product[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_product['response'].status_code)

    def test_get_product_of_a_snap_status_code_404_by_missing_snap_id(self):
        snap_id = " "
        result_get_product = self.user.get_products_of_a_snap(snap_id)
        assert result_get_product[
                   'response'].status_code == 404, "Expected status code is 404 but the status code is " + str(
            result_get_product['response'].status_code)
        result_get_product_snap_error_code = \
        json.loads(result_get_product['response'].content.decode('utf-8'))['error']['code']
        assert result_get_product_snap_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_product_snap_error_code

    def test_get_product_of_a_snap_status_code_404_by_unexisting_snap_id(self):
        snap_id = "abc"
        result_get_product = self.user.get_products_of_a_snap(snap_id)
        assert result_get_product[
                   'response'].status_code == 404, "Expected status code is 404 but the status code is " + str(
            result_get_product['response'].status_code)
        result_get_product_snap_error_code = \
        json.loads(result_get_product['response'].content.decode('utf-8'))['error']['code']
        assert result_get_product_snap_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_product_snap_error_code

    def test_search_snap_status_code_200(self):
        search_query = {"q": "A", "limit": "40", "order": "DESC", "orderby": "creation"}
        result_search_snap = self.user.search_snaps(search_query)
        assert result_search_snap[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_search_snap['response'].status_code)

    def test_search_snap_status_code_200_by_empty_query(self):
        search_query = {}
        result_search_snap = self.user.search_snaps(search_query)
        assert result_search_snap[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_search_snap['response'].status_code)

    def test_search_snap_status_code_500_by_incorrect_order_parameter(self):
        search_query = {"order": "abc"}
        result_search_snap = self.user.search_snaps(search_query)
        assert result_search_snap[
                   'response'].status_code == 500, "Expected status code is 500 but the status code is " + str(
            result_search_snap['response'].status_code)
        result_search_snap_error_code = json.loads(result_search_snap['response'].content.decode('utf-8'))['error'][
            'code']
        assert result_search_snap_error_code == "GET_FAIL", "Expected Error code is GET_FAIL but the error code is " + result_search_snap_error_code


    def test_get_comments_of_a_snap_status_code_200(self):
        snap_id = "7112"
        result_get_comment = self.user.get_snap_comment(snap_id)
        assert result_get_comment[
                   'response'].status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_get_comment['response'].status_code)

    def test_get_comments_of_a_snap_status_code_404_by_missing_snap_id(self):
        snap_id = " "
        result_get_comment = self.user.get_snap_comment(snap_id)
        assert result_get_comment[
                   'response'].status_code == 404, "Expected status code is 404 but the status code is " + str(
            result_get_comment['response'].status_code)
        result_get_comment_error_code = json.loads(result_get_comment['response'].content.decode('utf-8'))['error'][
            'code']
        assert result_get_comment_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_comment_error_code

    def test_get_comments_of_a_snap_status_code_404_by_invalid_snap_id(self):
        snap_id = "abc"
        result_get_comment = self.user.get_snap_comment(snap_id)
        assert result_get_comment[
                   'response'].status_code == 404, "Expected status code is 404 but the status code is " + str(
            result_get_comment['response'].status_code)
        result_get_comment_error_code = json.loads(result_get_comment['response'].content.decode('utf-8'))['error'][
            'code']
        assert result_get_comment_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_comment_error_code

    def test_post_comment_status_code_201(self):
        comment = "Unit Testing" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S")
        snap_id = "7112"
        result_post = self.user.post_comment(snap_id, comment)
        assert result_post.status_code == 201, "Expected Status code: 201 but the status code: " + str(
            result_post.status_code)

    def test_post_comment_status_code_400_by_missing_comment(self):
        comment = ""
        snap_id = "7112"
        result_post = self.user.post_comment(snap_id, comment)
        assert result_post.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_post.status_code)
        result_post_error_code = json.loads(result_post.content.decode('utf-8'))['error']['code']
        assert result_post_error_code == "MISSING_MESSAGE", "Expected Error code is MISSING_MESSAGE but the error code is " + result_post_error_code

    def test_post_comment_status_code_404_by_missing_snap_id(self):
        comment = "Unit Testing" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S")
        snap_id = " "
        result_post = self.user.post_comment(snap_id, comment)
        assert result_post.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_post.status_code)
        result_post_error_code = json.loads(result_post.content.decode('utf-8'))['error']['code']
        assert result_post_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_post_error_code

    def test_post_comment_status_code_404_by_unexisting_snap_id(self):
        comment = "Unit Testing" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S")
        snap_id = "abc"
        result_post = self.user.post_comment(snap_id, comment)
        assert result_post.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_post.status_code)
        result_post_error_code = json.loads(result_post.content.decode('utf-8'))['error']['code']
        assert result_post_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_post_error_code

    def test_post_comment_status_code_401_by_not_login(self):
        comment = "Unit Testing" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S")
        snap_id = "7112"
        self.user.logout()
        result_post = self.user.post_comment(snap_id, comment)
        assert result_post.status_code == 401, "Expected Status code: 401 but the status code: " + str(
            result_post.status_code)
        result_post_error_code = json.loads(result_post.content.decode('utf-8'))['error']['code']
        assert result_post_error_code == "NOT_LOGIN", "Expected Error code is NOT_FOUND but the error code is " + result_post_error_code
        self.user.login()

    # def test_collect_product_link_click_information_status_code_201(self):

    def test_get_snap_info_after_login_status_code_200(self):
        query = dict(snap_id_product='8',
                     home=dict(snap_id='7112', offset_id='7806', limit="14", order="DESC", orderby="creation"),
                     search=dict(snap_id='7744', limit='14', order='DESC', orderby='creation'),
                     product=dict(offset_id="", limit="12"))
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_home(self):
        query = self.query_get_snap_after_login
        query['home']['snap_id'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_search(self):
        query = self.query_get_snap_after_login
        query['search']['snap_id'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_product(self):
        query = self.query_get_snap_after_login
        query['snap_id_product'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    ### Abnormal case for get snap info after login
    # def test_get_snap_info_after_login_status_code_400_by_invalid_snap_id_for_search(self):
    #     query = self.query_get_snap_after_login
    #     query['search']['snap_id'] = "abc"
    #     result_get_snap = self.user.get_snap_info_after_login(query)
    #     assert result_get_snap.status_code == 400, "Expected Status code: 400 but the status code: " + str(
    #         result_get_snap.status_code)
    #     result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
    #     assert result_get_snap_error_code == "MISSING_SNAP_ID", "Expected Error code is MISSING_SNAP_ID but the error code is " + result_get_snap_error_code

    def test_get_snap_info_after_login_status_code_401_by_not_login_in(self):
        query = self.query_get_snap_after_login
        self.user.logout()
        result_get_snap = self.user.get_snap_info_after_login(query)
        assert result_get_snap.status_code == 401, "Expected Status code: 400 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "NOT_LOGIN", "Expected Error code is NOT_LOGIN but the error code is " + result_get_snap_error_code
        self.user.login()

    # Not find a suitable snap_product_id for testing the snap remove
    # def test_remove_a_snap_from_a_snap_status_code_204(self):
    #     snap_product_id = ''
    #     result_remove = self.user.remove_a_snap_product(snap_product_id)
    #     assert result_remove.status_code == 204, "Expected Status code: 204 but the status code: " + str(
    #         result_remove.status_code)

    def test_remove_a_snap_from_a_snap_status_code_404_by_unexisting_snap_product_id(self):
        snap_product_id = 'abc'
        result_remove = self.user.remove_a_snap_product(snap_product_id)
        assert result_remove.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_remove.status_code)
        result_remove_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        assert result_remove_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_remove_error_code

    def test_remove_a_snap_from_a_snap_status_code_404_by_missing_snap_product_id(self):
        snap_product_id = ' '
        result_remove = self.user.remove_a_snap_product(snap_product_id)
        assert result_remove.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_remove.status_code)
        result_remove_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        assert result_remove_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_remove_error_code

    def test_remove_a_snap_from_a_snap_status_code_401_by_not_login(self):
        snap_product_id = 'abc'
        self.user.logout()
        result_remove = self.user.remove_a_snap_product(snap_product_id)
        assert result_remove.status_code == 401, "Expected Status code: 401 but the status code: " + str(
            result_remove.status_code)
        result_remove_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        assert result_remove_error_code == "NOT_LOGIN", "Expected Error code is NOT_LOGIN but the error code is " + result_remove_error_code
        self.user.login()

    def test_get_snaps_by_snap_product_id_status_code_200(self):
        snap_product_id = '48'
        result_get_snap = self.user.get_snaps_by_snap_product_id(snap_product_id)
        assert result_get_snap.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_snap.status_code)

    def test_get_snaps_by_snap_product_id_status_code_404_by_unexsiting_snap_product_id(self):
        snap_product_id = '7654321'
        result_get_snap = self.user.get_snaps_by_snap_product_id(snap_product_id)
        assert result_get_snap.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_snap_error_code

    def test_get_snaps_by_snap_product_id_status_code_404_by_missing_snap_product_id(self):
        snap_product_id = ' '
        result_get_snap = self.user.get_snaps_by_snap_product_id(snap_product_id)
        assert result_get_snap.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_get_snap.status_code)
        result_get_snap_error_code = json.loads(result_get_snap.content.decode('utf-8'))['error']['code']
        assert result_get_snap_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_snap_error_code

    def test_get_user_status_code_200(self):
        user_id = '5118'
        result_get_user = self.user.get_user(user_id)
        assert result_get_user.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_get_user.status_code)

    def test_get_user_status_code_404_by_missing_user_id(self):
        user_id = ' '
        result_get_user = self.user.get_user(user_id)
        assert result_get_user.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_get_user.status_code)
        result_get_user_error_code = json.loads(result_get_user.content.decode('utf-8'))['error']['code']
        assert result_get_user_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_user_error_code

    def test_get_user_status_code_400_by_unexisting_user_id(self):
        user_id = '143567'
        result_get_user = self.user.get_user(user_id)
        assert result_get_user.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_get_user.status_code)
        result_get_user_error_code = json.loads(result_get_user.content.decode('utf-8'))['error']['code']
        assert result_get_user_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_get_user_error_code

    def test_change_password_status_code_200(self):
        current_password = '12345677'
        new_password = '12345678'
        result_change_password = self.user.change_password(current_password, new_password)
        assert result_change_password.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_change_password.status_code)
        self.user.change_password(new_password, current_password)

    def test_change_password_status_code_400_by_missing_current_password(self):
        current_password = ''
        new_password = '12345678'
        result_change_password = self.user.change_password(current_password, new_password)
        assert result_change_password.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_change_password.status_code)
        result_change_password_error_code = json.loads(result_change_password.content.decode('utf-8'))['error']['code']
        assert result_change_password_error_code == "MISSING_CURR_PASSWORD", "Expected Error code is MISSING_CURR_PASSWORD but the error code is " + result_change_password_error_code

    def test_change_password_status_code_400_by_missing_new_password(self):
        current_password = '12345677'
        new_password = ''
        result_change_password = self.user.change_password(current_password, new_password)
        assert result_change_password.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_change_password.status_code)
        result_change_password_error_code = json.loads(result_change_password.content.decode('utf-8'))['error']['code']
        assert result_change_password_error_code == "MISSING_NEW_PASSWORD", "Expected Error code is MISSING_NEW_PASSWORD but the error code is " + result_change_password_error_code

    # Abnormal Case for change password by invalid new password
    # def test_change_password_status_code_400_by_invalid_new_password(self):
    #     current_password = '12345677'
    #     new_password = '123'
    #     result_change_password = self.user.change_password(current_password, new_password)
    #     assert result_change_password.status_code == 400, "Expected Status code: 400 but the status code: " + str(
    #         result_change_password.status_code)
    #     result_change_password_error_code = json.loads(result_change_password.content.decode('utf-8'))['error']['code']
    #     assert result_change_password_error_code == "INVALID_NEW_PASSWORD", "Expected Error code is MISSING_NEW_PASSWORD but the error code is " + result_change_password_error_code

    def test_change_password_status_code_401_by_not_login(self):
        current_password = '12345677'
        new_password = '12345678'
        self.user.logout()
        result_change_password = self.user.change_password(current_password, new_password)
        assert result_change_password.status_code == 401, "Expected Status code: 401 but the status code: " + str(
            result_change_password.status_code)
        result_change_password_error_code = json.loads(result_change_password.content.decode('utf-8'))['error']['code']
        assert result_change_password_error_code == "NOT_LOGIN", "Expected Error code is NOT_LOGIN but the error code is " + result_change_password_error_code
        self.user.login()

    def test_change_password_status_code_404_by_invalid_current_password(self):
        current_password = '12345'
        new_password = '12345678'
        result_change_password = self.user.change_password(current_password, new_password)
        assert result_change_password.status_code == 404, "Expected Status code: 404 but the status code: " + str(
            result_change_password.status_code)

    def test_update_user_profile_200(self):
        query_profile = dict(firstname="Testing")
        result_update = self.user.update_user(self.user.get_user_id(), query_profile)
        assert result_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_update.status_code)

    def test_update_user_profile_400_by_missing_username(self):
        query_profile = dict(username="")
        result_update = self.user.update_user(self.user.get_user_id(), query_profile)
        assert result_update.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "INVALID_USERNAME", "Expected Error code is INVALID_USERNAME but the error code is " + result_update_error_code

    def test_update_user_profile_400_by_invalid_username(self):
        query_profile = dict(username="!@#$%^&")
        result_update = self.user.update_user(self.user.get_user_id(), query_profile)
        assert result_update.status_code == 400, "Expected Status code: 400 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "INVALID_USERNAME", "Expected Error code is INVALID_USERNAME but the error code is " + result_update_error_code

    # Abnormal Case for update user profile by invalid bio
    # def test_update_user_profile_400_by_invalid_username(self):
    #     query_profile = {
    #         'bio': "Trump was born and raised in Queens, a borough of New York City, and received a bachelor's degree in economics from the Wharton School. He took charge of his family's real-estate business in 1971, renamed it The Trump Organization, and expanded its operations from Queens and Brooklyn into Manhattan. The company built or renovated skyscrapers, hotels, casinos, and golf courses. Trump later started various side ventures, mostly by licensing his name. He bought the Miss Universe brand of beauty pageants in 1996, and sold it in 2015. He produced and hosted The Apprentice, a reality television series, from 2003 to 2015. As of 2020, Forbes estimated his net worth to be $2.1 billion.[a]Trumps political positions have been described as populist, protectionist, and nationalist. He entered the 2016 presidential race as a Republican and was elected in a surprise victory over Democratic nominee Hillary Clinton, although he lost the popular vote.[b] He became the oldest first-term U.S. president,[c] and the first without prior military or government service. His election and policies have sparked numerous protests. Trump has made many false or misleading statements during his campaign and presidency. The statements have been documented by fact-checkers, and the media have widely described the phenomenon as unprecedented in American politics. Many of his comments and actions have been characterized as racially charged or racist.During his presidency, Trump ordered a travel ban on citizens from several Muslim-majority countries, citing security concerns; after legal challenges, the Supreme Court upheld the policy's third revision. He enacted a tax-cut package for individuals and businesses, rescinding the individual health insurance mandate penalty. He appointed Neil Gorsuch and Brett Kavanaugh to the Supreme Court. In foreign policy, Trump has pursued an America First agenda, withdrawing the U.S. from the Trans-Pacific Partnership trade negotiations, the Paris Agreement on climate change, and the Iran nuclear deal. He imposed import tariffs which triggered a trade war with China, recognized Jerusalem as the capital of Israel, and withdrew U.S. troops from northern Syria. Trump met thrice with North Koreas leader Kim Jong-un, but talks on denuclearization broke down in 2019. Trump began running for a second term shortly after becoming president.A special counsel investigation led by Robert Mueller found that Trump and his campaign welcomed and encouraged Russian interference in the 2016 presidential election under the belief that it would be politically advantageous, but did not find sufficient evidence to press charges of criminal conspiracy or coordination with Russia.[d] Mueller also investigated Trump for obstruction of justice, and his report neither indicted nor exonerated Trump on that offense. After Trump solicited the investigation of a political rival by Ukraine, the House of Representatives impeached him in December 2019 for abuse of power and obstruction of Congress. The Senate acquitted him of both charges in February 2020."
    #     }
    #     result_update = self.user.update_user(query_profile)
    #     assert result_update.status_code == 400, "Expected Status code: 400 but the status code: " + str(
    #         result_update.status_code)
    #     result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
    #     assert result_update_error_code == "INVALID_BIO", "Expected Error code is INVALID_USERNAME but the error code is " + result_update_error_code

    def test_update_user_profile_401_by_not_login(self):
        query_profile = dict(firstname="Testing")
        self.user.logout()
        result_update = self.user.update_user(self.user.get_user_id(), query_profile)
        assert result_update.status_code == 401, "Expected Status code: 401 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "NOT_LOGIN", "Expected Error code is NOT_LOGIN but the error code is " + result_update_error_code
        self.user.login()

    def test_update_user_profile_401_by_another_user_id(self):
        query_profile = dict(firstname="Testing")
        user_id = "5099"
        result_update = self.user.update_user(user_id, query_profile)
        assert result_update.status_code == 401, "Expected Status code: 401 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "UNAUTHORIZED", "Expected Error code is NOT_LOGIN but the error code is " + result_update_error_code

    def test_update_user_profile_401_by_unexisting_user_id(self):
        query_profile = dict(firstname="Testing")
        user_id = " "
        result_update = self.user.update_user(user_id, query_profile)
        assert result_update.status_code == 401, "Expected Status code: 401 but the status code: " + str(
            result_update.status_code)
        result_update_error_code = json.loads(result_update.content.decode('utf-8'))['error']['code']
        assert result_update_error_code == "UNAUTHORIZED", "Expected Error code is NOT_LOGIN but the error code is " + result_update_error_code

    def test
