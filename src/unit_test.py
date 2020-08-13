import json
import time
import unittest

import constant as con
from User import User


class general_testing(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # self.user = User("test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", "12345")
        # self.user.register()
        self.report_user_param = con.report_user_param
        self.user = User("test3@gmail.com", "12345677", "12345")
        login_result = self.user.login()
        con.check_status_code_200(login_result)
        # self.user.update_user(self.user.get_user_id, constant.user_profile)

    def tearDown(self) -> None:
        self.user.login()
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)
        time.sleep(0.2)

    def test_login_status_code_200(self):
        result_login = self.user.login()
        con.check_status_code_200(result_login)

    def test_login_status_code_400_by_missing_email(self):
        email = con.missing_email_login
        password = self.user.get_password()
        result_login = User(email, password, "12345").login()
        con.check_status_code_400_BAD_REQUEST(result_login, "MISSING_EMAIL")

    def test_login_status_code_400_by_missing_password(self):
        email = self.user.get_email()
        password = con.missing_password_login
        result_login = User(email, password, "12345").login()
        con.check_status_code_400_BAD_REQUEST(result_login, "MISSING_PASSWORD")

    def test_login_status_code_400_by_invalid_email(self):
        password = self.user.get_password()
        for email in con.invalid_email_login_list:
            result_login = User(email, password, "12345").login()
            con.check_status_code_400_BAD_REQUEST(result_login, "INVALID_EMAIL")

    def test_login_status_code_404_by_invalid_password(self):
        email = self.user.get_email()
        password = con.invalid_password_login_list
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
        assert result_logout.status_code == 200, "Expected status code is 200 but the status code is " + str(
            result_logout.status_code)

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
        result_change_password = self.user.change_password(self.user.get_password(), con.new_password,
                                                           self.user.get_user_id())
        con.check_status_code_200(result_change_password)
        result_change_password_back = self.user.change_password(con.new_password, self.user.get_password(),
                                                                self.user.get_user_id())
        con.check_status_code_200(result_change_password_back)

    def test_change_password_status_code_400_by_missing_current_password(self):
        result_change_password = self.user.change_password(con.missing_password_change, con.new_password,
                                                           self.user.get_user_id())
        con.check_status_code_400_BAD_REQUEST(result_change_password, "MISSING_CURR_PASSWORD")

    def test_change_password_status_code_400_by_missing_new_password(self):
        result_change_password = self.user.change_password(self.user.get_password(), con.missing_password_change,
                                                           self.user.get_user_id())
        con.check_status_code_400_BAD_REQUEST(result_change_password, "MISSING_NEW_PASSWORD")

    def test_change_password_status_code_400_by_invalid_new_password(self):
        for password in con.invalid_password_change_list:
            result_change_password = self.user.change_password(self.user.get_password(), password,
                                                               self.user.get_user_id())
            con.check_status_code_400_BAD_REQUEST(result_change_password, "INVALID_NEW_PASSWORD")

    def test_change_password_status_code_403_by_unauthorized_user_id(self):
        result_change_password = self.user.change_password(self.user.get_password(), con.new_password,
                                                           con.unauthorized_user_id)
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


class without_user_auth_test(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User()
        self.location = con.location_register

    def test_register_status_code_200(self):
        email = con.testing_email
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

class comment_test(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # self.user = User("test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", "12345")
        # self.user.register()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        self.snap_id = '7822'
        # self.user.update_user(self.user.get_user_id, constant.user_profile)

    def tearDown(self) -> None:
        self.user.login()
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)
        time.sleep(0.2)

    def test_get_comments_of_a_snap_status_code_200(self):
        result_get_comment = self.user.get_snap_comment(con.snap_id_post_comment)
        con.check_status_code_200(result_get_comment['response'])

    def test_get_comments_of_a_snap_status_code_200_by_a_deleted_snap(self):
        self.user.create_snaps(con.get_snap_created_list())
        snap_id_get_comment = str(self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id'][0])
        self.user.post_comment(snap_id_get_comment, con.comment)
        result_delete_snap = self.user.remove_snap(snap_id_get_comment)
        con.check_status_code_204(result_delete_snap)
        result_get_comment = self.user.get_snap_comment(snap_id_get_comment)
        con.check_status_code_200(result_get_comment['response'])

    def test_get_comments_of_a_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_get_comments_list:
            result_get_comment = self.user.get_snap_comment(snap_id)
            con.check_status_code_404_NOT_FOUND(result_get_comment['response'])

    def test_post_comment_status_code_201(self):
        result_post = self.user.post_comment(con.snap_id_post_comment, con.comment)
        con.check_status_code_201(result_post)

    def test_post_comment_status_code_201_by_a_deleted_snap(self):
        self.user.create_snaps(con.get_snap_created_list())
        snap_id_post_comment = str(self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id'][0])
        result_delete_snap = self.user.remove_snap(snap_id_post_comment)
        con.check_status_code_204(result_delete_snap)
        result_post = self.user.post_comment(con.snap_id_post_comment, con.comment)
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


class snap_test(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # self.user = User("test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", "12345")
        # self.user.register()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        self.snap_id = '7822'
        # self.user.update_user(self.user.get_user_id, constant.user_profile)
        # self.user.create_snaps(con.get_snap_created_list(2))
        # snap_id_list = self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id']
        # self.snap_id = snap_id_list[0]

    def tearDown(self) -> None:
        self.user.login()
        snap_id_result_list = self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id']
        for snap_id in snap_id_result_list:
            self.user.remove_snap(str(snap_id))
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)
        time.sleep(0.2)

    def test_get_snap_status_code_200(self):
        result_get_snap = self.user.get_snaps(con.query_get_snap)
        con.check_status_code_200(result_get_snap["response"])

    def test_get_snap_status_code_200_by_null_params(self):
        result_get_snap = self.user.get_snaps({})
        con.check_status_code_200(result_get_snap["response"])

    def test_get_snap_status_code_500_by_invalid_order_param(self):
        result_get_snap = self.user.get_snaps(con.query_get_snap_invalid_param)
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
        con.check_two_result_are_the_same(result_full_list, result_list_combine)

    def test_get_single_snap_status_code_200(self):
        snap_id = self.snap_id
        result_get_single_snap = self.user.get_single_snap(snap_id)
        con.check_status_code_200(result_get_single_snap)
        snap_id_get = str(json.loads(result_get_single_snap.content.decode('utf-8'))['snap_id'])
        con.check_two_result_are_the_same(snap_id, snap_id_get)

    def test_get_single_snap_status_code_200_by_missing_snap_id(self):
        snap_id = con.missing_variable
        result_get_single_snap = self.user.get_single_snap(snap_id)
        con.check_status_code_200(result_get_single_snap)

    def test_get_single_snap_status_code_404_by_not_exist_snap_id(self):
        snap_id = 'abc'
        result_get_single_snap = self.user.get_single_snap(snap_id)
        assert result_get_single_snap.status_code == 404, "Expected status code is 404 but the status code is " + str(result_get_single_snap.status_code)
        result_get_single_snap_error_code = json.loads(result_get_single_snap.content.decode('utf-8'))['error']['code']
        print(result_get_single_snap.content)
        assert result_get_single_snap_error_code == "NOT_FOUND", "Expected Error code is INVALID_EMAIL but the error code is " + result_get_single_snap_error_code

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
        con.check_two_result_are_the_same(image_path_created, image_path_get)

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
        get_snap = self.user.get_user_snaps_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        result_remove = self.user.remove_snap(snap_id_remove)
        con.check_status_code_204(result_remove)

    def test_remove_snap_status_code_204_by_unexisting_snap_id(self):
        for snap_id in con.unexisting_snap_id_remove_snap_list:
            result_remove = self.user.remove_snap(snap_id)
            con.check_status_code_204(result_remove)

    def test_remove_snap_status_code_404_by_missing_snap_id(self):
        snap_id = con.missing_snap_id_remove_snap
        result_remove = self.user.remove_snap(snap_id)
        con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_remove_snap_list:
            result_remove = self.user.remove_snap(snap_id)
            con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_snap_status_code_401_by_not_login(self):
        get_snap = self.user.get_user_snaps_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        self.user.logout()
        result_remove = self.user.remove_snap(snap_id_remove)
        con.check_status_code_401_NOT_LOGIN(result_remove)

    # Abnormal case for get snap info after login 200 -> 400
    def test_get_snap_info_after_login_status_code_200_by_all_dataset(self):
        result_get_snap = self.user.get_snap_info_after_login(con.query_get_snap_after_login)
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
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    def test_get_snap_info_after_login_status_code_200_by_home_and_search_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home' or key == 'search'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    def test_get_snap_info_after_login_status_code_200_by_home_and_product_dataset(self):
        query = {key: val for key, val in con.query_get_snap_after_login.items() if key == 'home' or key == 'product'}
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_200(result_get_snap)

    # Abnormal case for get snap info after login 200 -> 400
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
        query['snap_id_product'] = ""
        result_get_snap = self.user.get_snap_info_after_login(query)
        con.check_status_code_400_BAD_REQUEST(result_get_snap, "MISSING_SNAP_ID")

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

    def test_update_user_profile_status_code_200(self):
        result_update = self.user.update_user(self.user.get_user_id(), con.query_profile)
        assert result_update.status_code == 200, "Expected Status code: 200 but the status code: " + str(
            result_update.status_code)

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
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.missing_image_name_profile_pic,
                                                          con.image_body_profile_pic)
        con.check_status_code_400_BAD_REQUEST(result_update, "MISSING_IMAGE_NAME")

    def test_update_user_profile_picture_status_code_400_by_missing_image_body(self):
        result_update = self.user.upload_user_profile_pic(self.user.get_user_id(), con.image_name_profile_pic,
                                                          con.missing_image_body_profile_pic)
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
        # print(snap_list)
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
        con.check_status_code_201(result_add_fav_snap)

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
        con.check_status_code_204(result_remove_fav_snap)

    def test_remove_a_snap_to_favourite_status_code_204_by_invalid_snap_id(self):
        user_id = self.user.get_user_id()
        for snap_id in con.invalid_snap_id_fav_snap_list:
            result_remove_fav_snap = self.user.remove_snap_from_favourite(user_id, snap_id)
            con.check_status_code_204(result_remove_fav_snap)

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
        con.check_status_code_200(result_get_snaps['response'])

    def test_get_snaps_of_a_user_status_code_200_by_unauthorized_user_id(self):
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
            con.check_status_code_404_NOT_FOUND(result_get_snaps)

    def test_get_snaps_of_a_user_status_code_500_by_invalid_order_param(self):
        user_id = self.user.get_user_id()
        for query in con.invalid_query_get_user_snap:
            result_get_snaps = self.user.get_user_snaps_of_a_user(user_id, query)
            con.check_status_code_500_SERVER_ERROR(result_get_snaps['response'], "GET_FAIL")


class favourite_snap_product_test(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        # self.user = User(con.testing_email, con.testing_password, con.testing_device_id)
        # self.user.register()
        self.user = User("test3@gmail.com", "12345677", "12345")
        self.user.login()
        self.admin_product = User(con.admin_product['email'], con.admin_product['password'],
                                  con.admin_product['device_id'])
        self.admin_product.login()
        # result_create_snap = self.admin_product.create_snaps(con.get_snap_created_with_snap_products())
        # result_content = json.loads(result_create_snap.content.decode('utf-8'))['results'][0]
        # result_has_products = result_content['has_products']
        # assert result_has_products == 'Y'
        # self.snap_id_with_product = result_content['snap_id']
        # self.fav_product_id_list = self.user.get_products_of_a_snap(str(result_content['snap_id']))['list_snap_product_id']
        self.user.add_snap_product_to_favourite(self.user.get_user_id(), con.fav_snap_id_add_before_testing)
        self.fav_snap_product_id_list = con.fav_snap_product_id_list
        time.sleep(0.2)

    def tearDown(self) -> None:
        self.user.login()
        fav_snap_list = self.user.get_favourite_products(self.user.get_user_id())['snap_product_id_list']
        print(fav_snap_list)
        for snap in fav_snap_list:
            self.user.remove_snap_product_from_favourite(self.user.get_user_id(), str(snap))
        self.user.logout()
        time.sleep(0.2)
        self.admin_product.login()
        snap_list = self.admin_product.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id']
        for snap in snap_list:
            self.user.remove_snap(str(snap))
        self.admin_product.logout()
        time.sleep(0.2)

    def test_get_favourite_products_status_code_200(self):
        user_id = self.admin_product.get_user_id()
        result_get_fav_products = self.user.get_favourite_products(user_id)
        con.check_status_code_200(result_get_fav_products['response'])

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
        for snap_product_id in self.fav_snap_product_id_list:
            result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
            con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_snap_product_to_favourite_status_code_201_by_deleted_snap_product(self):
        user_id = self.user.get_user_id()
        snap_product_id = con.fav_snap_product_id_add_before_testing
        result_remove_fav_snap_product = self.user.remove_snap_product_from_favourite(user_id, snap_product_id)
        con.check_status_code_201(result_remove_fav_snap_product)
        result_remove_snap_product = self.admin_product.remove_a_snap_product(snap_product_id)
        con.check_status_code_204(result_remove_snap_product)
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_snap_product_to_favourite_status_code_201_by_already_added(self):
        user_id = self.user.get_user_id()
        snap_product_id = con.fav_snap_product_id_add_before_testing
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_snap_product_to_favourite_status_code_201_by_deleted_snap(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_snap_product_id_list[0]
        self.admin_product.remove_snap(snap_product_id)
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_201(result_add_fav_snap_product)

    def test_add_a_product_to_favourite_status_code_403_by_unauthorized_user_id(self):
        user_id = con.unauthorized_user_id
        snap_product_id = self.fav_snap_product_id_list[0]
        result_add_fav_snap_product = self.user.add_snap_product_to_favourite(user_id, snap_product_id)
        con.check_status_code_403_unauthorized(result_add_fav_snap_product)

    def test_add_a_product_to_favourite_status_code_401_by_not_login(self):
        user_id = self.user.get_user_id()
        snap_product_id = self.fav_snap_product_id_list[0]
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
        fav_snap_product_id = con.fav_snap_product_id_add_before_testing
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

    def test_get_snaps_product_by_snap_product_id_status_code_200_by_deleted_snap_product_id(self):
        result_remove = self.user.remove_a_snap_product(con.snap_product_id_get_snap_product_deleted)
        con.check_status_code_204(result_remove)
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.snap_product_id_get_snap_product_deleted)
        con.check_status_code_200(result_get_snap)

    def test_get_snaps_product_by_snap_product_id_status_code_404_by_unexsiting_snap_product_id(self):
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.unexisting_snap_product_id_get_snap_product)
        con.check_status_code_404_NOT_FOUND(result_get_snap)

    def test_get_snaps_product_by_snap_product_id_status_code_404_by_missing_snap_product_id(self):
        result_get_snap = self.user.get_snaps_by_snap_product_id(con.missing_snap_product_id_get_snap_product)
        con.check_status_code_404_NOT_FOUND(result_get_snap)

    def test_get_product_of_a_snap_status_code_200(self):
        result_get_product = self.user.get_products_of_a_snap(con.snap_id_get_product_snap)
        con.check_status_code_200(result_get_product['response'])

    def test_get_product_of_a_snap_status_code_200_by_a_deleted_snap(self):
        # Get one Snap of myself
        get_snap = self.user.get_user_snaps_of_a_user(self.user.get_user_id())
        snap_id_remove = str(get_snap['list_snap_id'][0])
        # Get product snap before deleting the snap
        result_get_product_before_delete = self.user.get_products_of_a_snap(snap_id_remove)
        con.check_status_code_200(result_get_product_before_delete['response'])
        result_product_list_before = result_get_product_before_delete["list_product_id"]
        # Remove the snap
        result_delete_snap = self.user.remove_snap(snap_id_remove)
        con.check_status_code_204(result_delete_snap)
        # Get product snap after deleting the snap
        result_get_product_after_delete = self.user.get_products_of_a_snap(snap_id_remove)
        con.check_status_code_200(result_get_product_after_delete['response'])
        result_product_list_after = result_get_product_after_delete['list_product_id']
        # Compare the two result of getting product snap
        con.check_two_result_are_the_same(result_product_list_before, result_product_list_after)

    def test_get_product_of_a_snap_status_code_404_by_invalid_snap_id(self):
        for snap_id in con.invalid_snap_id_get_product_snap_list:
            result_get_product = self.user.get_products_of_a_snap(snap_id)
            con.check_status_code_404_NOT_FOUND(result_get_product)

    def test_remove_a_snap_product_from_a_snap_status_code_204_by_unexisting_snap_product_id(self):
        result_remove = self.user.remove_a_snap_product(con.unexisting_snap_product_id_remove_snap_product)
        con.check_status_code_204(result_remove)
        # result_remove_error_code = json.loads(result_remove.content.decode('utf-8'))['error']['code']
        # assert result_remove_error_code == "NOT_FOUND", "Expected Error code is NOT_FOUND but the error code is " + result_remove_error_code

    def test_remove_a_snap_product_from_a_snap_status_code_404_by_missing_snap_product_id(self):
        result_remove = self.user.remove_a_snap_product(con.missing_snap_product_id_remove_snap_product)
        con.check_status_code_404_NOT_FOUND(result_remove)

    def test_remove_a_snap_product_from_a_snap_status_code_401_by_not_login(self):
        self.user.logout()
        result_remove = self.user.remove_a_snap_product(con.snap_product_id_remove_snap_product)
        con.check_status_code_401_NOT_LOGIN(result_remove)

