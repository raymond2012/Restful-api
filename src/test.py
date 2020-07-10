import json

import pytest

from src.Authentication import Authentication
from src.Snap import Snap
from src.User import User

### Authentication ###
def test_authetication():
    auth = Authentication("test3@gmail.com", "12345677", "12345")
    r = auth.login()
    login_result = json.loads(r.content.decode('utf-8'))
    assert r.status_code == 200, "Expected Status code: 200 but the status code: " + r.status_code
    assert login_result['token'] is not None and login_result['user_id'] > 0, "Expected token and user_id exist but they are None"
    logout_result = json.loads(auth.logout().content.decode('utf-8'))
    print(logout_result)
    assert logout_result['token'] is None


def test_get_user_profile():
    result = User("test3@gmail.com", "12345677", "12345").get_user_profile()
    print(result)
    assert result.status_code == 200, "Expected Status code: 200 but the status code: " + result.status_code


# def test_change_password():
#     user = User("test3@gmail.com", "12345677", "12345")
#     result = user.change_password("12345677", "12345677")
#     print(result)
#     assert result.status_code == 201

def test_follow_a_user():
    user1 = User("test3@gmail.com", "12345677", "12345")
    user2 = User("test2@gmail.com", "12345678", "12345")
    user2.follow_user(user1.get_user_id())
    assert str(json.loads(user2.get_following().content.decode('utf-8'))['following'][0]['user_id']) == user1.get_user_id()
    assert str(json.loads(user1.get_follower().content.decode('utf-8'))['follower'][0]['user_id']) == user2.get_user_id()
    user2.unfollow_user(user1.get_user_id())
    print(str(json.loads(user2.get_following().content.decode('utf-8'))['following']))
    # assert str(json.loads(user2.get_following().content.decode('utf-8'))['following']) ==

def test_get_snap_order():
    snap = Snap("test3@gmail.com", "12345678", "12345")
    query_full = {"filter": "", "offset": "", "offset_id": "", "limit": "40", "order": "DESC", "orderby": "creation"}
    query_half = {"filter": "", "offset": "", "offset_id": "", "limit": "20", "order": "DESC", "orderby": "creation"}
    query_half_with_offset = {"filter": "", "offset": "", "offset_id": "", "limit": "20", "order": "DESC", "orderby": "creation"}
    result_full = snap.get_snaps(query_full)
    query_half_with_offset['offset_id'] = result_full[int(len(result_full)/2-1)]
    assert result_full == snap.get_snaps(query_half) + snap.get_snaps(query_half_with_offset)

# test_follow_a_user()
# test_get_snap_order()
test_authetication()