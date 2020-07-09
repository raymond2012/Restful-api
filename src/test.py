import json

import pytest

from src.User import User

def test_get_user_profile():
    result = User("test2@gmail.com", "12345678", "12345").get_user_profile()
    print(result)
    # assert result.status_code == 201

def test_change_password():
    user = User("test3@gmail.com", "12345677", "12345")
    result = user.change_password("12345677", "12345677")
    print(result)
    assert result.status_code == 201

def test_follow_a_user():
    user1 = User("test3@gmail.com", "12345677", "12345")
    user2 = User("test2@gmail.com", "12345678", "12345")
    user2.follow_user(user1.get_user_id())
    assert str(json.loads(user2.get_following().content.decode('utf-8'))['following'][0]['user_id']) == user1.get_user_id()
