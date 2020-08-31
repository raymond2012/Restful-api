import json
import time
import unittest
from datetime import datetime

from src.User import User
import constant as con


class Test_my_test:
    def setup_method(self):
        super().__init__()
        # self.user = User("test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com", "12345678", "12345")
        # self.user.register()
        self.report_user_param = con.report_user_param
        # self.user = User("jmeter-tester@gmail.com", "12345678", "12345")
        self.user = User("test3@gmail.com", "12345677", "12345")
        login_result = self.user.login()
        con.check_status_code_200(login_result)
        # self.user.update_user(self.user.get_user_id, constant.user_profile)

    def teardown_method(self):
        self.user.login()
        snap_id_result_list = self.user.get_user_snaps_of_a_user(self.user.get_user_id(), dict(limit=200))['list_snap_id']
        print(snap_id_result_list)
        for snap_id in snap_id_result_list:
            self.user.remove_snap(str(snap_id))
        result_logout = self.user.logout()
        con.check_status_code_200(result_logout)

    def test_1(self):
        pass

    # def tearDown(self) -> None:
    #     snap_id_result_list = self.user.get_user_snaps_of_a_user(self.user.get_user_id())['list_snap_id']
    #     for snap_id in snap_id_result_list:
    #         self.user.remove_snap(str(snap_id))
    #     result_logout = self.user.logout()
    #     assert result_logout.status_code == 200, "Expected status code is 200 but the status code is " + str(
    #         result_logout.status_code)
    #     time.sleep(0.2)

