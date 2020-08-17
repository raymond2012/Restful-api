import json
import time
import datetime

import pytest

import constant as con
from User import User


def create_a_testing_user():
    testing_user = User("test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", con.testing_password, con.testing_device_id)
    result = testing_user.register()
    con.check_status_code_200(result)
    return testing_user


def create_a_snap_create_user():
    snap_user = User(con.create_snap_user['email'], con.create_snap_user['password'], con.create_snap_user['dev_id'])
    result = snap_user.register()
    con.check_status_code_200(result)
    return snap_user


def get_admin_user_for_snap_product():
    admin_user = User(con.admin_product['email'], con.admin_product['password'], con.admin_product['device_id'])
    result = admin_user.login()
    con.check_status_code_200(result)
    return admin_user


@pytest.fixture(scope="class")
def deleted_snap_id_before_comment_testing():
    # Before testing
    user = create_a_snap_create_user()
    result_create = user.create_snaps(con.get_snap_created_list())
    con.check_status_code_201(result_create)
    snap_id = str(json.loads(result_create.content.decode('utf-8'))['results'][0]['snap_id'])
    result_delete_snap = user.remove_snap(snap_id)
    con.check_status_code_204(result_delete_snap)
    yield snap_id
    # After testing
    user.remove_snap(snap_id)
    user.logout()


@pytest.fixture(scope="function")
def create_snap_with_snap_product_before_snap_product_testing():
    admin_product = get_admin_user_for_snap_product()
    result_created = admin_product.create_snaps(con.get_snap_created_with_snap_products())
    con.check_status_code_201(result_created)
    snap_id = str(json.loads(result_created.content.decode('utf-8'))['results'][0]['snap_id'])
    yield snap_id
    admin_product.remove_snap(snap_id)
    admin_product.logout()


class Test_general:
    def setup_method(self):
        super().__init__()
        self.user = create_a_testing_user()
        self.report_user_param = con.report_user_param
        # self.user = User("test3@gmail.com", "12345677", "12345")
        login_result = self.user.login()
        con.check_status_code_200(login_result)
        # self.user.update_user(self.user.get_user_id, constant.user_profile)

    def teardown_method(self):
        self.user.login()
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)
        time.sleep(0.2)

    def test_login_status_code_200(self):
        result_login = self.user.login()
        con.check_status_code_200(result_login)
        login_content = json.loads(result_login.content.decode('utf-8'))
        con.check_result_is_not_None(login_content['token'])
        con.check_result_is_not_None(login_content['user_id'])
        con.check_two_results_are_the_same("application", login_content['account_type'])

    def test_login_status_code_400_by_missing_email(self):
        email = con.missing_variable
        password = self.user.get_password()
        result_login = User(email, password, "12345").login()
        con.check_status_code_400_BAD_REQUEST(result_login, "MISSING_EMAIL")

    def test_login_status_code_400_by_missing_password(self):
        email = self.user.get_email()
        password = con.missing_variable
        result_login = User(email, password, "12345").login()
        con.check_status_code_400_BAD_REQUEST(result_login, "MISSING_PASSWORD")

    def test_login_status_code_400_by_invalid_email(self):
        password = self.user.get_password()
        for email in con.invalid_email_login_list:
            result_login = User(email, password, "12345").login()
            con.check_status_code_400_BAD_REQUEST(result_login, "INVALID_EMAIL")

    def test_login_status_code_404_by_invalid_password(self):
        email = self.user.get_email()
        for password in con.invalid_password_login_list:
            result_login = User(email, password, con.testing_device_id).login()
            con.check_status_code_400_BAD_REQUEST(result_login, "INVALID_PASSWORD")

    def test_login_status_code_404_by_unexisting_email(self):
        email = con.unexisting_email_login
        password = self.user.get_password()
        result_login = User(email, password, con.testing_device_id).login()
        con.check_status_code_404_NOT_FOUND(result_login)

    def test_login_status_code_400_by_logged_in_google_before(self):
        pass

    def test_logout_status_code_200(self):
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)
        logout_content = json.loads(result_logout.content.decode('utf-8'))
        con.check_two_results_are_the_same(None, logout_content['token'])

    def test_logout_status_code_401_by_not_login(self):
        self.user.logout()
        result_logout = self.user.logout()
        con.check_status_code_401_NOT_LOGIN(result_logout)

    def test_forget_password_status_code_200(self):
        email = self.user.get_email()
        print(email)
        result_forget = self.user.forget_password(email)
        con.check_status_code_200(result_forget)

    def test_forget_password_status_code_400_by_missing_email(self):
        result_forget = self.user.forget_password(con.missing_variable)
        con.check_status_code_400_BAD_REQUEST(result_forget, "MISSING_EMAIL")

    def test_forget_password_status_code_400_by_invalid_email(self):
        for email in con.invalid_email_forget_pass:
            result_forget = self.user.forget_password(email)
            con.check_status_code_200(result_forget)

    def test_report_a_user_status_code_201(self):
        report_param = self.report_user_param
        result_report = self.user.report_user(report_param)
        con.check_status_code_201(result_report)

    def test_report_a_user_status_code_201_by_not_login(self):
        report_param = self.report_user_param
        self.user.logout()
        result_report = self.user.report_user(report_param)
        con.check_status_code_201(result_report)

    def test_report_a_user_status_code_201_by_self_user_id(self):
        report_param = self.report_user_param
        report_param['user_id'] = self.user.get_user_id()
        result_report = self.user.report_user(report_param)
        con.check_status_code_201(result_report)

    def test_report_a_user_status_code_400_by_missing_report_type(self):
        report_param = con.report_user_report_type_param
        report_param['report_type'] = con.missing_variable
        print(report_param)
        result_report = self.user.report_user(report_param)
        con.check_status_code_400_BAD_REQUEST(result_report, "MISSING_REPORT_TYPE")

    def test_report_a_user_status_code_400_by_invalid_report_type(self):
        report_param = con.report_user_report_type_param
        for report_type in con.invalid_report_type_list:
            report_param['report_type'] = report_type
            result_report = self.user.report_user(report_param)
            con.check_status_code_400_BAD_REQUEST(result_report, "INVALID_REPORT_TYPE")

    def test_report_a_user_status_code_400_by_missing_user_id(self):
        report_param = con.report_user_user_id_param
        report_param['user_id'] = con.missing_variable
        result_report = self.user.report_user(report_param)
        con.check_status_code_400_BAD_REQUEST(result_report, "MISSING_USER_ID")

    def test_report_a_user_status_code_404_by_invalid_user_id(self):
        report_param = con.report_user_user_id_param
        for user_id in con.invalid_user_id_list:
            report_param['user_id'] = user_id
            result_report = self.user.report_user(report_param)
            con.check_status_code_404_NOT_FOUND(result_report)

    def test_check_username_valid_or_not_status_code_200_by_self_username(self):
        username = self.user.get_username()
        result_check_username = self.user.check_user_valid(username)
        con.check_status_code_200(result_check_username)

    def test_check_username_valid_or_not_status_code_200_by_unexisting_username(self):
        for username in con.unexisting_username_list:
            result_check_username = self.user.check_user_valid(username)
            con.check_status_code_200(result_check_username)

    def test_check_username_valid_or_not_status_code_400_by_invalid_username(self):
        for username in con.invalid_username_list:
            result_check_username = self.user.check_user_valid(username)
            con.check_status_code_400_BAD_REQUEST(result_check_username, "INVALID_USERNAME")

    def test_check_username_valid_or_not_status_code_401_by_not_login(self):
        username = self.user.get_username()
        self.user.logout()
        result_check_username = self.user.check_user_valid(username)
        con.check_status_code_401_NOT_LOGIN(result_check_username)

    def test_get_user_status_code_200_by_self(self):
        result_get_user = self.user.get_user(self.user.get_user_id())
        con.check_status_code_200(result_get_user)

    def test_get_user_status_code_200_by_another_user(self):
        for user_id in con.user_id_get_user_list:
            result_get_user = self.user.get_user(user_id)
            con.check_status_code_200(result_get_user)

    def test_get_user_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_user_list:
            result_get_user = self.user.get_user(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_user)

    def test_change_password_status_code_200(self):
        new_password = con.new_password
        current_password = self.user.get_password()
        result_change_password = self.user.change_password(current_password, new_password,
                                                           self.user.get_user_id())
        con.check_status_code_200(result_change_password)
        result_change_password_back = self.user.change_password(con.new_password, self.user.get_password(),
                                                                self.user.get_user_id())
        con.check_status_code_200(result_change_password_back)

    def test_change_password_status_code_400_by_missing_current_password(self):
        new_password = con.new_password
        current_password = con.missing_variable
        result_change_password = self.user.change_password(current_password, new_password,
                                                           self.user.get_user_id())
        con.check_status_code_400_BAD_REQUEST(result_change_password, "MISSING_CURR_PASSWORD")

    def test_change_password_status_code_400_by_missing_new_password(self):
        new_password = con.missing_variable
        current_password = self.user.get_password()
        result_change_password = self.user.change_password(current_password, new_password,
                                                           self.user.get_user_id())
        con.check_status_code_400_BAD_REQUEST(result_change_password, "MISSING_NEW_PASSWORD")

    def test_change_password_status_code_400_by_invalid_new_password(self):
        current_password = self.user.get_password()
        for new_password in con.invalid_password_change_list:
            result_change_password = self.user.change_password(current_password, new_password,
                                                               self.user.get_user_id())
            con.check_status_code_400_BAD_REQUEST(result_change_password, "INVALID_NEW_PASSWORD")

    def test_change_password_status_code_403_by_unauthorized_user_id(self):
        new_password = con.new_password
        current_password = self.user.get_password()
        user_id = con.unauthorized_user_id
        result_change_password = self.user.change_password(current_password, new_password,
                                                           user_id)
        con.check_status_code_403_unauthorized(result_change_password)

    def test_change_password_status_code_401_by_not_login(self):
        self.user.logout()
        result_change_password = self.user.change_password(self.user.get_password(), con.new_password,
                                                           self.user.get_user_id())
        con.check_status_code_401_NOT_LOGIN(result_change_password)

    def test_change_password_status_code_404_by_invalid_current_password(self):
        for password in con.invalid_password_change_list:
            result_change_password = self.user.change_password(password, con.new_password, self.user.get_user_id())
            con.check_status_code_404_NOT_FOUND(result_change_password)


class Test_without_user_auth:
    def setup_method(self):
        self.user = User()
        self.location = con.location_register

    def test_register_status_code_200(self):
        email = "test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com"
        password = con.testing_password
        result_register = User(email, password, con.testing_device_id).register(self.location)
        con.check_status_code_200(result_register)

    def test_register_status_code_400_by_missing_email(self):
        email = con.missing_email_register
        password = con.testing_password
        result_register = User(email, password, con.testing_device_id).register(self.location)
        con.check_status_code_400_BAD_REQUEST(result_register, "MISSING_EMAIL")

    def test_register_status_code_400_by_missing_password(self):
        email = con.testing_email
        password = con.missing_password_register
        result_register = User(email, password, con.testing_device_id).register(self.location)
        con.check_status_code_400_BAD_REQUEST(result_register, "MISSING_PASSWORD")

    def test_register_status_code_400_by_invalid_email(self):
        password = con.testing_password
        for email in con.invalid_email_register_list:
            result_register = User(email, password, '12345').register(self.location)
            con.check_status_code_400_BAD_REQUEST(result_register, "INVALID_EMAIL")

    def test_register_status_code_400_by_existing_email(self):
        existing_email = con.testing_email
        password = con.testing_password
        User(existing_email, password, con.testing_device_id).register(self.location)
        result_register = User(existing_email, password, con.testing_device_id).register(self.location)
        con.check_status_code_400_BAD_REQUEST(result_register, "EXIST_ALREADY")

    def test_get_privacy_policy_status_code_200(self):
        result_privacy = self.user.get_privacy_policy()
        con.check_status_code_200(result_privacy)

    def test_get_terms_and_condition_status_code_200(self):
        result_terms = self.user.get_terms_and_conditions()
        con.check_status_code_200(result_terms)

    def test_get_getstart_background_image_status_code_200(self):
        result_background = self.user.get_background_image()
        con.check_status_code_200(result_background)

    def test_social_media_list_status_code_200(self):
        result_media = self.user.get_social_media_list()
        con.check_status_code_200(result_media)

    def test_search_snap_status_code_200(self):
        result_search_snap = self.user.search_snaps(con.search_snap_query)
        con.check_status_code_200(result_search_snap['response'])

    def test_search_snap_status_code_200_by_empty_query(self):
        result_search_snap = self.user.search_snaps(con.empty_search_snap_query)
        con.check_status_code_200(result_search_snap['response'])

    def test_search_snap_status_code_500_by_incorrect_order_parameter(self):
        result_search_snap = self.user.search_snaps(con.incorrect_search_snap_query)
        con.check_status_code_500_SERVER_ERROR(result_search_snap['response'], "GET_FAIL")


class Test_comment:
    def setup_method(self):
        super().__init__()
        # self.user = create_a_testing_user()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        # self.user.update_user(self.user.get_user_id, constant.user_profile)

    def teardown_method(self):
        self.user.login()
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)
        time.sleep(0.2)

    def setup_class(self):
        # self.user = create_a_snap_create_user
        self.user_create_snap = User("test4@gmail.com", "12345678", "12345")
        self.user_create_snap.login()
        snap_create = self.user_create_snap.create_snaps(con.get_snap_created_list())
        con.check_status_code_201(snap_create)
        self.snap_id_comment = str(json.loads(snap_create.content.decode('utf-8'))['results'][0]['snap_id'])

    def teardown_class(self):
        self.user_create_snap.remove_snap(self.snap_id_comment)
        self.user_create_snap.logout()

    def test_get_comments_of_a_snap_status_code_200(self):
        result_get_comment = self.user.get_snap_comment(self.snap_id_comment)
        con.check_status_code_200(result_get_comment['response'])

    def test_get_comments_of_a_snap_status_code_200_by_a_deleted_snap(self, deleted_snap_id_before_comment_testing):
        snap_id_get_comment = "{}".format(deleted_snap_id_before_comment_testing)
        result_get_comment = self.user.get_snap_comment(snap_id_get_comment)
        con.check_status_code_200(result_get_comment['response'])

    def test_get_comments_of_a_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_get_comments_list:
            result_get_comment = self.user.get_snap_comment(snap_id)
            con.check_status_code_404_NOT_FOUND(result_get_comment['response'])

    def test_post_comment_status_code_201(self):
        result_post = self.user.post_comment(con.snap_id_post_comment, con.comment)
        con.check_status_code_201(result_post)

    def test_post_comment_status_code_201_by_a_deleted_snap(self, deleted_snap_id_before_comment_testing):
        snap_id_post_comment = "{}".format(deleted_snap_id_before_comment_testing)
        result_post = self.user.post_comment(snap_id_post_comment, con.comment)
        con.check_status_code_201(result_post)

    def test_post_comment_status_code_400_by_missing_comment(self):
        result_post = self.user.post_comment(con.snap_id_post_comment, con.missing_comment)
        con.check_status_code_400_BAD_REQUEST(result_post, "MISSING_MESSAGE")

    def test_post_comment_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_post_comment_list:
            result_post = self.user.post_comment(snap_id, con.comment)
            con.check_status_code_404_NOT_FOUND(result_post)

    def test_post_comment_status_code_401_by_not_login(self):
        self.user.logout()
        result_post = self.user.post_comment(con.snap_id_post_comment, con.comment)
        con.check_status_code_401_NOT_LOGIN(result_post)


class Test_snap:
    def setup_method(self):
        super().__init__()
        # self.user = create_a_testing_user()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        self.snap_id = '7822'
        # self.user.update_user(self.user.get_user_id, constant.user_profile)
        # self.user.create_snaps(con.get_snap_created_list(2))
        # snap_id_list = self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id']
        # self.snap_id = snap_id_list[0]

    def teardown_method(self):
        self.user.login()
        snap_id_result_list = self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id']
        for snap_id in snap_id_result_list:
            self.user.remove_snap(str(snap_id))
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)
        time.sleep(0.2)

    def setup_class(self):
        # self.user = create_a_snap_create_user()
        self.user_create_snap = User("test4@gmail.com", "12345678", "12345")
        self.user_create_snap.login()
        snap_create = self.user_create_snap.create_snaps(con.get_snap_created_list())
        con.check_status_code_201(snap_create)
        self.snap_id = str(json.loads(snap_create.content.decode('utf-8'))['results'][0]['snap_id'])

    def teardown_class(self):
        self.user_create_snap.remove_snap(self.snap_id)
        self.user_create_snap.logout()

    def test_get_snap_status_code_200(self):
        query = con.query_get_snap
        result_get_snap = self.user.get_snaps(query)
        con.check_status_code_200(result_get_snap["response"])

    def test_get_snap_status_code_200_by_null_params(self):
        query = {}
        result_get_snap = self.user.get_snaps(query)
        con.check_status_code_200(result_get_snap["response"])

    def test_get_snap_status_code_500_by_invalid_order_param(self):
        query = con.query_get_snap_invalid_param
        result_get_snap = self.user.get_snaps(query)
        con.check_status_code_500_SERVER_ERROR(result_get_snap["response"], "GET_FAIL")

    def test_get_snap_checking_order_by_creation(self):
        # Define 1 query with limit 40 order by creation in descending
        query_full = con.query_full
        # Define 4 queries with limit 10 order by creation in descending
        query_first = con.query_first
        query_second = con.query_second
        query_third = con.query_third
        query_last = con.query_last
        # Get 40 snaps and check the status is 200
        result_full = self.user.get_snaps(query_full)
        con.check_status_code_200(result_full['response'])
        result_full_list = self.user.get_snaps(query_full)['list_snap_id']
        # The offset_id will be defined with the 0th, 10th, 20th and 30th items from the above query
        query_second['offset_id'] = str(result_full_list[int(len(result_full_list) / 4 - 1)])
        query_third['offset_id'] = str(result_full_list[int(len(result_full_list) / 2 - 1)])
        query_last['offset_id'] = str(result_full_list[int(len(result_full_list) * 3 / 4 - 1)])
        # Combine the 4 queries result in one list
        result_list_combine = self.user.get_snaps(query_first)['list_snap_id'] + self.user.get_snaps(query_second)[
            'list_snap_id'] + self.user.get_snaps(query_third)['list_snap_id'] + self.user.get_snaps(query_last)[
                                  'list_snap_id']
        # Compare the results from two types of query are the same
        con.check_two_results_are_the_same(result_full_list, result_list_combine)

    def test_get_single_snap_status_code_200(self):
        snap_id = self.snap_id
        result_get_single_snap = self.user.get_single_snap(snap_id)
        con.check_status_code_200(result_get_single_snap)
        snap_id_get = str(json.loads(result_get_single_snap.content.decode('utf-8'))['snap_id'])
        con.check_two_results_are_the_same(snap_id, snap_id_get)

    def test_get_single_snap_status_code_200_by_missing_snap_id(self):
        snap_id = con.missing_variable
        result_get_single_snap = self.user.get_single_snap(snap_id)
        con.check_status_code_200(result_get_single_snap)

    def test_get_single_snap_status_code_404_by_not_exist_snap_id(self):
        snap_id = 'abc'
        result_get_single_snap = self.user.get_single_snap(snap_id)
        con.check_status_code_404_NOT_FOUND(result_get_single_snap)

    def test_create_snap_status_code_201(self):
        snap_cre = con.get_snap_created_list()
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_201(result_created)

    def test_create_snap_checking_content(self):
        # Create a snap
        snap_cre = con.get_snap_created_list()
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_201(result_created)
        result_created_content = json.loads(result_created.content.decode('utf-8'))['results'][0]
        image_path_created = result_created_content['image_path']
        snap_id_created = str(result_created_content['snap_id'])
        # Get a single snap by the snap_id from the created snap result
        result_get = self.user.get_single_snap(snap_id_created)
        con.check_status_code_200(result_get)
        result_get_content = json.loads(result_get.content.decode('utf-8'))
        image_path_get = result_get_content['image_path']
        con.check_two_results_are_the_same(image_path_created, image_path_get)

    def test_create_snap_status_code_400_by_missing_title(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['title'] = con.missing_variable
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_400_BAD_REQUEST(result_created, "MISSING_TITLE")

    def test_create_snap_status_code_400_by_missing_description(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['description'] = con.missing_variable
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_400_BAD_REQUEST(result_created, "MISSING_DESCRIPTION")

    def test_create_snap_status_code_400_by_missing_image_name(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['image_name'] = con.missing_variable
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_400_BAD_REQUEST(result_created, "MISSING_IMAGE_NAME")

    def test_create_snap_status_code_400_by_missing_image_body(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['image_body'] = con.missing_variable
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_400_BAD_REQUEST(result_created, "MISSING_IMAGE_BODY")

    def test_create_snap_status_code_400_by_missing_ref_id(self):
        snap_cre = con.get_snap_created_list()
        snap_cre[0]['ref_id'] = con.missing_variable
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_400_BAD_REQUEST(result_created, "MISSING_REF_ID")

    # Abnormal Case for create snap 413 -> 400
    def test_create_snap_status_code_400_by_over_10MB_image_size(self):
        snap_cre = con.get_snap_created_list()
        image_path_list = con.image_path_list_code_413
        for image_path in image_path_list:
            snap_cre[0]['image_body'] = con.get_encode_base64_image(image_path)
            result_created = self.user.create_snaps(snap_cre)
            con.check_status_code_400_BAD_REQUEST(result_created, "IMAGE_SIZE_OVER_LIMIT")
            # con.check_status_code_413_PAYLOAD_TOO_BIG(result_created, "IMAGE_SIZE_OVER_LIMIT")

    def test_create_snap_status_code_400_by_image_size_over_limit(self):
        snap_cre = con.get_snap_created_list()
        image_path_list = con.image_path_list_code_400
        for image_path in image_path_list:
            snap_cre[0]['image_body'] = con.get_encode_base64_image(image_path)
            result_created = self.user.create_snaps(snap_cre)
            con.check_status_code_400_BAD_REQUEST(result_created, "IMAGE_SIZE_OVER_LIMIT")

    def test_create_snap_status_code_401_by_not_login(self):
        snap_cre = con.get_snap_created_list()
        self.user.logout()
        result_created = self.user.create_snaps(snap_cre)
        con.check_status_code_401_NOT_LOGIN(result_created)

    def test_remove_snap_status_code_204(self):
        result_create = self.user.create_snaps(con.get_snap_created_list())
        con.check_status_code_201(result_create)
        snap_id_remove = str(json.loads(result_create.content.decode('utf-8'))['results'][0]['snap_id'])
        result_remove = self.user.remove_snap(snap_id_remove)
        con.check_status_code_204(result_remove)

    def test_remove_snap_status_code_204_by_unexisting_snap_id(self):
        for snap_id_remove in con.unexisting_snap_id_remove_snap_list:
            result_remove = self.user.remove_snap(snap_id_remove)
            con.check_status_code_204(result_remove)

    def test_remove_snap_status_code_404_by_missing_snap_id(self):
        snap_id_remove = con.missing_snap_id_remove_snap
        result_remove = self.user.remove_snap(snap_id_remove)
        con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id_remove in con.invalid_snap_id_remove_snap_list:
            result_remove = self.user.remove_snap(snap_id_remove)
            con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_snap_status_code_401_by_not_login(self):
        result_create = self.user.create_snaps(con.get_snap_created_list())
        con.check_status_code_201(result_create)
        snap_id_remove = str(json.loads(result_create.content.decode('utf-8'))['results'][0]['snap_id'])
        self.user.logout()
        result_remove = self.user.remove_snap(snap_id_remove)
        con.check_status_code_401_NOT_LOGIN(result_remove)
        self.user.login()
        result_remove = self.user.remove_snap(snap_id_remove)
        con.check_status_code_204(result_remove)

    def test_get_snaps_of_a_user_status_code_200(self):
        user_id = self.user_create_snap.get_user_id()
        result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
        con.check_status_code_200(result_get_snaps['response'])

    def test_get_snaps_of_a_user_status_code_200_by_another_user_id(self):
        user_id = con.unauthorized_user_id
        result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
        con.check_status_code_200(result_get_snaps['response'])

    def test_get_snaps_of_a_user_status_code_200_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
        con.check_status_code_200(result_get_snaps['response'])

    def test_get_snaps_of_a_user_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_snap_id_get_user_snap_list:
            result_get_snaps = self.user.get_user_snaps_of_a_user(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_snaps['response'])

    def test_get_snaps_of_a_user_status_code_500_by_invalid_order_param(self):
        user_id = self.user.get_user_id()
        for query in con.invalid_query_get_user_snap:
            result_get_snaps = self.user.get_user_snaps_of_a_user(user_id, query)
            con.check_status_code_500_SERVER_ERROR(result_get_snaps['response'], "GET_FAIL")

    # Abnormal case for get snap info after login by all dataset 200 -> 400
    def test_get_snap_info_after_login_status_code_200_by_all_dataset(self):
        result_get_snap = self.user.get_snap_info_after_login(con.query_get_snap_after_login)
        con.check_status_code_200(result_get_snap)

    def test_get_snap_info_after_login_status_code_200_by_missing_query(self):
        query = con.missing_query
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    def test_get_snap_info_after_login_status_code_200_by_home_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    def test_get_snap_info_after_login_status_code_200_by_search_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'search'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    # Abnormal case for get snap info after login 200 -> 400
    def test_get_snap_info_after_login_status_code_200_by_product_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'product'}
        print(query)
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    def test_get_snap_info_after_login_status_code_200_by_home_and_search_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home' or key == 'search'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    # Abnormal case for get snap info after by home and product dataset login 200 -> 400
    def test_get_snap_info_after_login_status_code_200_by_home_and_product_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home' or key == 'product'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    # Abnormal case for get snap info after by search and product dataset login 200 -> 400
    def test_get_snap_info_after_login_status_code_200_by_search_and_product_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'search' or key == 'product'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_home(self):
        query = con.query_get_snap_after_login
        query['home']['snap_id'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_400_BAD_REQUEST(result_get_snap, "MISSING_SNAP_ID")

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_search(self):
        query = con.query_get_snap_after_login
        query['search']['snap_id'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_400_BAD_REQUEST(result_get_snap, "MISSING_SNAP_ID")

    def test_get_snap_info_after_login_status_code_400_by_missing_snap_id_for_product(self):
        query = con.query_get_snap_after_login
        query['product']['snap_product_id'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_400_BAD_REQUEST(result_get_snap, "MISSING_SNAP_ID")

    # Abnormal case for get snap info after login
    # def test_get_snap_info_after_login_status_code_400_by_invalid_snap_id_for_search(self):
    #     query = self.query_get_snap_after_login
    #     query['search']['snap_id'] = "abc"
    #     result_get_snap = self.user.get_snap_info_after_login(query)
    #     con.check_status_code_400_BAD_REQUEST(result_get_snap, "MISSING_SNAP_ID")

    def test_get_snap_info_after_login_status_code_401_by_not_login(self):
        query = con.query_get_snap_after_login
        self.user.logout()
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_401_NOT_LOGIN(result_get_snap)

    def test_create_snap(self):
        # Create a snap with image body
        snap_cre = con.get_snap_created_list()
        result_created = json.loads(self.user.create_snaps(snap_cre).content.decode('utf-8'))['results'][0]
        # Check the return image path exist
        con.check_result_is_not_None(result_created['image_path'])
        con.check_result_is_not_None(result_created['snap_id'])
        snap_id_created = str(result_created['snap_id'])
        # Get a single snap by the snap_id from the created snap result
        result_get = json.loads(self.user.get_single_snap(snap_id_created).content.decode('utf-8'))
        con.check_two_results_are_the_same(result_created['image_path'], result_get['image_path'])
        # Get the snap by user id and check the result contains the created snap by snap_id
        result_get_user_snap = self.user.get_user_snaps_of_a_user(self.user.get_user_id())
        con.check_result_item_in_list(snap_id_created, result_get_user_snap['list_snap_id'])
        # Remove the snap and check the remove request successfully
        result_remove = self.user.remove_snap(snap_id_created)
        con.check_status_code_204(result_remove)


class Test_profile:
    def setup_method(self):
        super().__init__()
        # self.user = create_a_testing_user()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        # result = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic, con.image_body_profile_pic)
        # con.check_status_code_200(result)

    def teardown_method(self):
        self.user.login()
        self.user.remove_user_profile_pic(self.user.get_user_id())
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)

    def test_update_user_profile_status_code_200(self):
        result_update = self.user.update_user(self.user.get_user_id(), con.query_profile)
        con.check_status_code_200(result_update)

    def test_update_user_profile_status_code_400_by_invalid_username(self):
        for query_profile in con.invalid_username_query_profile_list:
            result_update = self.user.update_user(self.user.get_user_id(), query_profile)
            con.check_status_code_400_BAD_REQUEST(result_update, "INVALID_USERNAME")

    def test_update_user_profile_status_code_400_by_invalid_bio(self):
        result_update = self.user.update_user(self.user.get_user_id(), con.invalid_bio_query_profile)
        con.check_status_code_400_BAD_REQUEST(result_update, "INVALID_BIO")

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
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic,
                                                          con.image_body_profile_pic)
        con.check_status_code_200(result_update)

    # Abnormal Case for update user profile picture
    # def test_update_user_profile_picture_status_code_200_by_4_5MB_image(self):
    #     image_name = "Testing"
    #     image_body = self.user.get_encode_base64_image(self.image_path_4_5MB)
    #     result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), image_name, image_body)
    #     assert result_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
    #         result_update.status_code)

    def test_update_user_profile_picture_status_code_400_by_missing_image_name(self):
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.missing_variable,
                                                          con.image_body_profile_pic)
        con.check_status_code_400_BAD_REQUEST(result_update, "MISSING_IMAGE_NAME")

    def test_update_user_profile_picture_status_code_400_by_missing_image_body(self):
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic,
                                                          con.missing_variable)
        con.check_status_code_400_BAD_REQUEST(result_update, "MISSING_IMAGE_BODY")

    def test_update_user_profile_picture_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_update = self.user.upload_user_profile_pic(user_id, con.image_name_profile_pic,
                                                          con.image_body_profile_pic)
        con.check_status_code_403_unauthorized(result_update)

    def test_update_user_profile_picture_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_update = self.user.upload_user_profile_pic(user_id, con.image_name_profile_pic,
                                                          con.image_body_profile_pic)
        con.check_status_code_401_NOT_LOGIN(result_update)

    def test_update_user_profile_picture_status_code_404_by_invalid_image_body(self):
        for image_body in con.invalid_user_id_query_profile_list:
            result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic,
                                                              image_body)
            con.check_status_code_404_NOT_FOUND(result_update)

    def test_remove_user_profile_picture_status_code_204(self):
        self.test_update_user_profile_picture_status_code_200()
        result_remove = self.user.remove_user_profile_pic(self.user.get_user_id())
        con.check_status_code_204(result_remove)

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


class Test_follow:
    def setup_method(self):
        super().__init__()
        # self.user = create_a_testing_user()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()

    def teardown_method(self):
        self.user.login()
        result_unfollow = self.user.unfollow_user(self.user.get_user_id(), self.user_follow.get_user_id())
        con.check_status_code_204(result_unfollow)
        following_num = str(json.loads(self.user.get_following(self.user_follow.get_user_id()).content.decode('utf-8'))['n_following'])
        con.check_two_results_are_the_same('0', following_num)
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)

    def setup_class(self):
        # self.user_follow = create_a_snap_create_user()
        self.user_follow = User("follow_target@gmail.com", "12345678", "12345")
        self.user_follow.login()
        snap_create = self.user_follow.create_snaps(con.get_snap_created_list())
        self.snap_id = str(json.loads(snap_create.content.decode('utf-8'))['results'][0]['snap_id'])

    def teardown_class(self):
        self.user_follow.login()
        snap_id_result_list = self.user_follow.get_user_snaps_of_a_user(self.user_follow.get_user_id())['list_snap_id']
        for snap_id in snap_id_result_list:
            self.user_follow.remove_snap(str(snap_id))
        self.user_follow.logout()

    def test_follow_a_user_status_code_201(self):
        user_id = self.user.get_user_id()
        target_user_id = self.user_follow.get_user_id()
        result_follow = self.user.follow_user(user_id, target_user_id)
        con.check_status_code_201(result_follow)

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
        con.check_status_code_204(result_unfollow)

    # Abnormal Case for unfollow a user by invalid user id 404 -> 204
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
        con.check_status_code_200(result_get_follower)

    def test_get_follower_status_code_200_by_not_login(self):
        user_id = self.user.get_user_id()
        result_get_follower = self.user.get_follower(user_id)
        self.user.logout()
        con.check_status_code_200(result_get_follower)

    def test_get_follower_status_code_200_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_get_follower = self.user.get_follower(user_id)
        con.check_status_code_200(result_get_follower)

    def test_get_follower_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_follower_list:
            result_get_follower = self.user.get_follower(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_follower)

    def test_get_following_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_following = self.user.get_following(user_id)
        con.check_status_code_200(result_get_following)

    def test_get_following_status_code_200_by_not_login(self):
        user_id = self.user.get_user_id()
        result_get_following = self.user.get_following(user_id)
        self.user.logout()
        con.check_status_code_200(result_get_following)

    def test_get_following_status_code_200_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        result_get_following = self.user.get_following(user_id)
        con.check_status_code_200(result_get_following)

    def test_get_following_status_code_404_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_following_list:
            result_get_following = self.user.get_following(user_id)
            con.check_status_code_404_NOT_FOUND(result_get_following)

    def test_get_following_user_snaps_status_code_200(self):
        self.test_follow_a_user_status_code_201()
        result_get = self.user.get_following_users_snaps()
        con.check_status_code_200(result_get)
        result_content = json.loads(result_get.content.decode('utf-8'))[0]
        con.check_two_results_are_the_same(self.user_follow.get_user_id(), str(result_content['user_id']))
        con.check_two_results_are_the_same(self.snap_id, str(result_content['snap_id']))

    def test_get_following_user_snaps_status_code_401_by_not_login(self):
        self.test_follow_a_user_status_code_201()
        self.user.logout()
        result_get = self.user.get_following_users_snaps()
        con.check_status_code_401_NOT_LOGIN(result_get)


class Test_favourite_snap:
    def setup_method(self):
        super().__init__()
        # self.user = create_a_testing_user()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        result_search = self.user.search_snaps(dict(limit=10))
        con.check_status_code_200(result_search['response'])
        self.snap_list = result_search["list_snap_id"][:4]
        for snap in self.snap_list:
            self.user.add_snap_to_favourite(self.user.get_user_id(), str(snap))
        self.fav_snap_id = str(result_search["list_snap_id"][4])

    def teardown_method(self):
        self.user.login()
        fav_snap_list = self.user.get_favourite_snaps(self.user.get_user_id())['snap_id_list']
        for snap in fav_snap_list:
            self.user.remove_snap_from_favourite(self.user.get_user_id(), str(snap))
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)

    def test_get_favourite_snaps_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_fav_snaps = self.user.get_favourite_snaps(user_id)
        con.check_status_code_200(result_get_fav_snaps['response'])
        result_snap_list = result_get_fav_snaps['snap_id_list']
        con.check_two_results_are_the_same(self.snap_list.sort(), result_snap_list.sort())

    def test_get_favourite_snaps_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_get_fav_snaps = self.user.get_favourite_snaps(user_id)
        con.check_status_code_401_NOT_LOGIN(result_get_fav_snaps['response'])

    def test_get_favourite_snaps_status_code_401_by_invalid_user_id(self):
        user_id_list = con.invalid_snap_id_fav_snap_list
        for user_id in user_id_list:
            result_get_fav_snaps = self.user.get_favourite_snaps(user_id)
            con.check_status_code_403_unauthorized(result_get_fav_snaps['response'])

    def test_add_a_snap_to_favourite_status_code_201(self):
        user_id = self.user.get_user_id()
        fav_snap_id = self.fav_snap_id
        result_add_fav_snap = self.user.add_snap_to_favourite(user_id, fav_snap_id)
        con.check_status_code_201(result_add_fav_snap)

    def test_add_a_snap_to_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        fav_snap_id = self.fav_snap_id
        result_add_fav_snap = self.user.add_snap_to_favourite(user_id, fav_snap_id)
        con.check_status_code_403_unauthorized(result_add_fav_snap)

    def test_add_a_snap_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        fav_snap_id = self.fav_snap_id
        self.user.logout()
        result_add_fav_snap = self.user.add_snap_to_favourite(user_id, fav_snap_id)
        con.check_status_code_401_NOT_LOGIN(result_add_fav_snap)

    def test_add_a_snap_to_favourite_status_code_404_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for fav_snap_id in con.invalid_snap_id_fav_snap_list:
            result_add_fav_snap = self.user.add_snap_to_favourite(user_id, fav_snap_id)
            con.check_status_code_404_NOT_FOUND(result_add_fav_snap)

    def test_remove_a_snap_from_favourite_status_code_204(self):
        user_id = self.user.get_user_id()
        fav_snap_id = self.fav_snap_id
        result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, fav_snap_id)
        con.check_status_code_204(result_remove_fav_snap)

    def test_remove_a_snap_to_favourite_status_code_204_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for fav_snap_id in con.invalid_snap_id_fav_snap_list:
            result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, fav_snap_id)
            con.check_status_code_204(result_remove_fav_snap)

    def test_remove_a_snap_from_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        fav_snap_id = self.fav_snap_id
        result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, fav_snap_id)
        con.check_status_code_403_unauthorized(result_remove_fav_snap)

    def test_remove_a_snap_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        fav_snap_id = self.fav_snap_id
        self.user.logout()
        result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, fav_snap_id)
        con.check_status_code_401_NOT_LOGIN(result_remove_fav_snap)


class Test_favourite_snap_product_test:
    def setup_method(self):
        super().__init__()
        # self.user = create_a_testing_user()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        for snap_id in self.fav_snap_product_id_list:
            result_add = self.user.add_snap_product_to_favourite(self.user.get_user_id(), str(snap_id))
            con.check_status_code_201(result_add)

    def teardown_method(self):
        self.user.login()
        fav_snap_list = self.user.get_favourite_products(self.user.get_user_id())['snap_product_id_list']
        for snap in fav_snap_list:
            self.user.remove_snap_product_from_favourite(self.user.get_user_id(), str(snap))
        self.user.logout()

    def setup_class(self):
        # self.user_follow = create_a_snap_create_user()
        self.admin_product = User(con.admin_product['email'], con.admin_product['password'],
                                  con.admin_product['device_id'])
        self.admin_product.login()
        result_create_snap = self.admin_product.create_snaps(con.get_snap_created_with_snap_products())
        result_content = json.loads(result_create_snap.content.decode('utf-8'))['results'][0]
        self.snap_id_with_product = str(result_content['snap_id'])
        snap_product_id_list = self.admin_product.get_products_of_a_snap(str(result_content['snap_id']))['list_snap_product_id']
        assert len(snap_product_id_list) > 1
        self.fav_snap_product_id_list = snap_product_id_list[2:5]
        self.fav_snap_product_id = str(snap_product_id_list[0])
        self.fav_snap_product_id_remove = str(snap_product_id_list[0])

    def teardown_class(self):
        self.admin_product.login()
        snap_list = self.admin_product.get_user_snaps_of_a_user(self.admin_product.get_user_id())['list_snap_id']
        for snap in snap_list:
            self.admin_product.remove_snap(str(snap))
        self.admin_product.logout()

    def test_get_favourite_products_status_code_200(self):
        user_id = self.user.get_user_id()
        result_get_fav_products = self.user.get_favourite_products(user_id)
        con.check_status_code_200(result_get_fav_products['response'])
        result_snap_product_id_list = result_get_fav_products['snap_product_id_list']
        con.check_two_results_are_the_same(self.fav_snap_product_id_list.sort(), result_snap_product_id_list.sort())

    def test_get_favourite_products_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        self.user.logout()
        result_get_fav_products = self.user.get_favourite_products(user_id)
        con.check_status_code_401_NOT_LOGIN(result_get_fav_products['response'])

    def test_get_favourite_products_status_code_403_by_invalid_user_id(self):
        for user_id in con.invalid_user_id_get_fav_product_list:
            result_get_fav_products = self.user.get_favourite_products(user_id)
            con.check_status_code_403_unauthorized(result_get_fav_products['response'])

    def test_add_a_snap_product_to_favourite_status_code_201(self):
        user_id = self.user.get_user_id()
        for snap_product_id in self.fav_snap_product_id_list:
            result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, str(snap_product_id))
            con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_snap_product_to_favourite_status_code_201_by_deleted_snap_product(self,
                                                                                     create_snap_with_snap_product_before_snap_product_testing):
        user_id = self.user.get_user_id()
        snap_id = "{}".format(create_snap_with_snap_product_before_snap_product_testing)
        # Get snap product of snap
        snap_product_id = str(self.admin_product.get_products_of_a_snap(snap_id)['list_snap_product_id'][0])
        # Remove a snap product
        result_remove_snap_product = self.admin_product.remove_a_snap_product(snap_product_id)
        con.check_status_code_204(result_remove_snap_product)
        # Add a deleted snap product to favourite
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_snap_product_to_favourite_status_code_201_by_already_added(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_snap_product_id
        for i in range(2):
            result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
            con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_snap_product_to_favourite_status_code_201_by_deleted_snap(self,
                                                                             create_snap_with_snap_product_before_snap_product_testing):
        user_id = self.user.get_user_id()
        snap_id = "{}".format(create_snap_with_snap_product_before_snap_product_testing)
        # Get snap product of snap
        snap_product_id = str(self.admin_product.get_products_of_a_snap(snap_id)['list_snap_product_id'][0])
        # Remove a snap
        result_remove_snap = self.admin_product.remove_snap(snap_id)
        con.check_status_code_204(result_remove_snap)
        # Add a snap product of deleted snap to favourite
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_product_to_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        snap_product_id = self.fav_snap_product_id
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_403_unauthorized(result_add_fav_snap_product)

    def test_add_a_product_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_snap_product_id
        self.user.logout()
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_401_NOT_LOGIN(result_add_fav_snap_product)

    def test_add_a_product_to_favourite_status_code_401_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for snap_product_id in con.invalid_snap_id_add_fav_snap_product_list:
            result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
            con.check_status_code_404_NOT_FOUND(result_add_fav_snap_product)

    def test_remove_a_product_from_favourite_status_code_204(self):
        user_id = self.user.get_user_id()
        fav_snap_product_id = self.fav_snap_product_id[0]
        result_remove_fav_snap_product = self.user.remove_snap_product_from_favourite(user_id, fav_snap_product_id)
        con.check_status_code_204(result_remove_fav_snap_product)

    def test_remove_a_product_to_favourite_status_code_204_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for snap_product_id in con.invalid_snap_id_remove_fav_snap_product_list:
            result_remove_fav_snap_product = self.user.remove_snap_product_from_favourite(user_id, snap_product_id)
            con.check_status_code_204(result_remove_fav_snap_product)

    def test_remove_a_product_from_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        snap_product_id = con.fav_snap_id_add_before_testing
        result_remove_fav_snap_product = self.user.remove_snap_product_from_favourite(user_id, snap_product_id)
        con.check_status_code_403_unauthorized(result_remove_fav_snap_product)

    def test_remove_a_product_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        snap_product_id = con.fav_snap_id_add_before_testing
        self.user.logout()
        result_remove_fav_snap_product = self.user.remove_snap_product_from_favourite(user_id, snap_product_id)
        con.check_status_code_401_NOT_LOGIN(result_remove_fav_snap_product)

    def test_get_snaps_product_by_snap_product_id_status_code_200(self):
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.snap_product_id_get_snap_product)
        con.check_status_code_200(result_get_snap)

    def test_get_snaps_product_by_snap_product_id_status_code_200_by_deleted_snap_product_id(self, create_snap_with_snap_product_before_snap_product_testing):
        snap_id = "{}".format(create_snap_with_snap_product_before_snap_product_testing)
        # Get snap product of snap
        snap_product_id = str(self.admin_product.get_products_of_a_snap(snap_id)['list_snap_product_id'][0])
        # Remove a snap
        result_remove_snap = self.admin_product.remove_a_snap_product(snap_product_id)
        con.check_status_code_204(result_remove_snap)
        # Get a deleted snap product
        result_get_snap = self.user.get_snaps_by_snap_product_id(snap_product_id)
        con.check_status_code_200(result_get_snap)

    def test_get_snaps_product_by_snap_product_id_status_code_404_by_unexsiting_snap_product_id(self):
        snap_product_id = con.unexisting_snap_product_id_get_snap_product
        result_get_snap = self.user.get_snaps_by_snap_product_id(snap_product_id)
        con.check_status_code_404_NOT_FOUND(result_get_snap)

    def test_get_snaps_product_by_snap_product_id_status_code_404_by_missing_snap_product_id(self):
        snap_product_id = con.missing_variable
        result_get_snap = self.user.get_snaps_by_snap_product_id(snap_product_id)
        con.check_status_code_404_NOT_FOUND(result_get_snap)

    def test_get_product_of_a_snap_status_code_200(self):
        result_get_product = self.user.get_products_of_a_snap(con.snap_id_get_product_snap)
        con.check_status_code_200(result_get_product['response'])

    def test_get_product_of_a_snap_status_code_200_by_a_deleted_snap(self,
                                                                     create_snap_with_snap_product_before_snap_product_testing):
        user_id = self.user.get_user_id()
        snap_id = "{}".format(create_snap_with_snap_product_before_snap_product_testing)
        # Get snap product of snap
        snap_product_id = str(self.admin_product.get_products_of_a_snap(snap_id)['list_snap_product_id'][0])
        # Remove a snap
        result_remove_snap = self.admin_product.remove_snap(snap_id)
        con.check_status_code_204(result_remove_snap)
        # Get a snap product of deleted snap
        result_get_fav_snap_product = self.user.get_products_of_a_snap(snap_product_id)
        con.check_status_code_200(result_get_fav_snap_product["response"])

    def test_get_product_of_a_snap_status_code_200_by_a_deleted_snap_product(self,
                                                                             create_snap_with_snap_product_before_snap_product_testing):
        user_id = self.user.get_user_id()
        snap_id = "{}".format(create_snap_with_snap_product_before_snap_product_testing)
        # Get snap product of snap
        snap_product_id = str(self.admin_product.get_products_of_a_snap(snap_id)['list_snap_product_id'][0])
        # Remove a snap product
        result_remove_snap = self.admin_product.remove_a_snap_product(snap_product_id)
        con.check_status_code_204(result_remove_snap)
        # Get a deleted snap product
        result_get_fav_snap_product = self.user.get_products_of_a_snap(snap_product_id)
        con.check_status_code_200(result_get_fav_snap_product["response"])

    def test_get_product_of_a_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_get_product_snap_list:
            result_get_product = self.user.get_products_of_a_snap(snap_id)
            con.check_status_code_404_NOT_FOUND(result_get_product['response'])

    def test_remove_a_snap_product_from_a_snap_status_code_204(self):
        snap_product_id = self.fav_snap_product_id_remove
        result_remove = self.admin_product.remove_a_snap_product(snap_product_id)
        con.check_status_code_204(result_remove)

    def test_remove_a_snap_product_from_a_snap_status_code_404_by_unexisting_snap_product_id(self):
        snap_product_id = con.unexisting_snap_product_id_remove_snap_product
        result_remove = self.admin_product.remove_a_snap_product(snap_product_id)
        con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_a_snap_product_from_a_snap_status_code_404_by_missing_snap_product_id(self):
        snap_product_id = con.missing_variable
        result_remove = self.admin_product.remove_a_snap_product(snap_product_id)
        con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_a_snap_product_from_a_snap_status_code_401_by_not_login(self):
        self.admin_product.logout()
        result_remove = self.admin_product.remove_a_snap_product(con.snap_product_id_remove_snap_product)
        con.check_status_code_401_NOT_LOGIN(result_remove)
