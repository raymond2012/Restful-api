import time
import unittest
import ctypes
import pytest

import constant


@pytest.fixture(scope="module", autouse=True)
def mod_header(request):
    print('\n-----------------')
    print('module      : %s' % request.module.__name__)
    print('-----------------')


@pytest.fixture(scope="function")
# @pytest.fixture(scope="function", autouse=True)
def func_header(request):
    print('\n-----------------')
    print('function    : %s' % request.function.__name__)
    print('time        : %s' % time.asctime())
    print('-----------------')

@pytest.fixture(scope="function")
# @pytest.fixture(scope="function", autouse=True)
def func_header_2(request):
    print('\n-----------------')
    print('function 2   : %s' % request.function.__name__)
    print('time 2       : %s' % time.asctime())
    print('-----------------')

@pytest.fixture(scope="class")
# @pytest.fixture(scope="function", autouse=True)
def func_header_3(request):
    print('\n-----------------')
    print('function 3   : %s' % request.function.__name__)
    print('time 3       : %s' % time.asctime())
    print('-----------------')

@pytest.yield_fixture(scope='module')
def func_header_5():
    print('setup')
    yield 'hello'
    print('teardown')


@pytest.mark.usefixtures("func_header")
@pytest.mark.usefixtures("func_header_2")
def test_one(func_header_5):
    print('in test_one()')


def test_two(func_header_5):
    print(func_header_5)
    print('in test_two()')

@pytest.fixture(scope="class")
def resource():
    print("setup")
    yield "resource", "hello"
    print("teardown")


class TestResource:
    @classmethod
    def setup_class(cls):
        print("------ setup before class TestSohu ------")

    @classmethod
    def teardown_class(cls):
        print("------ teardown after class TestResource ------")

    def test_that_depends_on_resource(self):
        result = "{}".format(resource)
        print(result)

    def test_that_depends_on_resource2(self, resource):
        result, hello = "{}".format(resource)
        print(result+"2" + hello)


@pytest.mark.usefixtures("func_header_5")
class test(unittest.TestCase):
    def test_three(self):
        print('in test_three()')

    def test_four(self):
        print(func_header_5)
        pass
