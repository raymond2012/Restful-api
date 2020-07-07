import pytest

from src.User import User

def test_get_user_profile():
    result = User("test3@gmail.com", "12345677", "12345").get_user_profile()
    assert result == 200

def test_change_password():
    result = User("test3@gmail.com", "12345677", "12345").change_password("12345677", "12345678")
    assert result == 201