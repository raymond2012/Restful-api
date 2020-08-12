import datetime
import glob
import base64
import imghdr
import json
import random

# Status Code
UNAUTHORIZED_CODE = 401
NOT_LOGIN_CODE = 401
NOT_FOUND_CODE = 404

# Status Code Message
UNAUTHORIZED_CODE_MESSAGE = "Expected Status code: " + str(UNAUTHORIZED_CODE) + " but the status code: "
NOT_LOGIN_CODE_MESSAGE = "Expected Status code: " + str(NOT_LOGIN_CODE) + " but the status code: "
NOT_FOUND_CODE_MESSAGE = "Expected Status code: " + str(NOT_FOUND_CODE) + " but the status code: "

# Error Code
UNAUTHORIZED_ERROR_CODE = "UNAUTHORIZED"
NOT_LOGIN_ERROR_CODE = "NOT_LOGIN"
NOT_FOUND_ERROR_CODE = "NOT_FOUND"

# Error Code Message
UNAUTHORIZED_ERROR_MESSAGE = "Expected Error code is " + UNAUTHORIZED_ERROR_CODE + " but the error code is "
NOT_LOGIN_ERROR_MESSAGE = "Expected Error code is " + NOT_LOGIN_ERROR_CODE + " but the error code is "
NOT_FOUND_ERROR_MESSAGE = "Expected Error code is " + NOT_FOUND_ERROR_CODE + " but the error code is "


def get_encode_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = "data:image/" + imghdr.what(image_path) + ";base64," + base64.b64encode(
            image_file.read()).decode('utf-8')
    return encoded_string


def get_snap_created_list(num=1):
    snap_list = list()
    snap_image_list = random.sample(image_path_list_code_200, num + 1)
    print(snap_image_list)
    for i in range(1, num + 1):
        snap_item = {
            "title": "Test-Title-" + str(i),
            "description": "Test-Description-" + str(i),
            "image_name": "Image-" + str(i),
            "image_body": get_encode_base64_image(snap_image_list[i]),
            "ref_id": str(i)
        }
        snap_list.append(snap_item)
    return snap_list


def check_status_code_401_NOT_LOGIN(result):
    assert result.status_code == NOT_LOGIN_CODE, NOT_LOGIN_CODE_MESSAGE + str(result.status_code)
    error_code = json.loads(result.content.decode('utf-8'))['error']['code']
    assert error_code == NOT_LOGIN_ERROR_CODE, NOT_LOGIN_ERROR_MESSAGE + error_code


def check_status_code_403_unauthorized(result):
    assert result.status_code == UNAUTHORIZED_CODE, UNAUTHORIZED_CODE_MESSAGE + str(result.status_code)
    error_code = json.loads(result.content.decode('utf-8'))['error']['code']
    assert error_code == UNAUTHORIZED_ERROR_CODE, UNAUTHORIZED_ERROR_MESSAGE + error_code


def check_status_code_404_NOT_FOUND(result):
    assert result.status_code == NOT_FOUND_CODE, NOT_FOUND_CODE_MESSAGE + str(result.status_code)
    error_code = json.loads(result.content.decode('utf-8'))['error']['code']
    assert error_code == NOT_FOUND_ERROR_CODE, NOT_FOUND_ERROR_MESSAGE + error_code


# General
unauthorized_user_id = '5108'
testing_email = "test" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com"
testing_password = "testing1234"
testing_device_id = '12345'

# Login
invalid_email_list = ['test8rtyuhygfd765403', '#!@1132']
unexist_email = "unexist" + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com"

# Get Snap
query_get_snap = {"filter": "", "offset": "", "offset_id": "", "limit": "40", "order": "DESC",
                  "orderby": "creation"}
query_get_snap_invalid_param = {"order": "abc"}

# Image Path for Creating Snap
image_path_list_code_413 = glob.glob('img/testing_image_status_code_413/*.jpg')
image_path_list_code_400 = glob.glob('img/testing_image_status_code_400/*.jpg')
image_path_list_code_200 = glob.glob('img/testing_snap_image/*.jpg')

# Remove Snap
missing_snap_id_remove_snap = " "
unexisting_snap_id_remove_snap_list = ['abc', '12345678']

# Get Product of a Snap
snap_id_get_product_snap = '7112'
invalid_snap_id_get_product_snap_list = [" ", "abc"]

# Search Snap
search_snap_query = {"q": "A", "limit": "40", "order": "DESC", "orderby": "creation"}
empty_search_snap_query = {}
incorrect_search_snap_query = {"order": "abc"}

# Get Comments
snap_id_get_comments = '7112'
invalid_snap_id_get_comments_list = [" ", "abc"]

# Post Comments
comment = "Unit Testing" + datetime.datetime.now().strftime("_%Y%m%d-%H%M%S")
missing_comment = ""
snap_id_post_comment = "7112"
invalid_snap_id_post_comment_list = [" ", "abc"]

# Get Snap Info after Login
query_get_snap_after_login = dict(
    home=dict(snap_id='7112', offset_id='7806', limit="14", order="DESC", orderby="creation"),
    search=dict(snap_id='7744', limit='14', order='DESC', orderby='creation'),
    product=dict(snap_id_product='8', offset_id="", limit="12"))

# Remove a Snap Product from a Snap
snap_product_id_remove_snap_product = '32'
unexisting_snap_product_id_remove_snap_product = '12345678'
missing_snap_product_id_remove_snap_product = " "

# Get Snap Product by Snap Product id
snap_product_id_get_snap_product = '32'
snap_product_id_get_snap_product_deleted = '14'
unexisting_snap_product_id_get_snap_product = '12345678'
missing_snap_product_id_get_snap_product = " "

# Change Password
new_password = 'testing9999'
missing_password = ''
invalid_password_list = ['1234']

# Get User Status
user_id_get_user_list = ['5112', '5113', '5114']
invalid_user_id_get_user_list = [' ', 'abc', '12345678']

# Update User Profile
query_profile = dict(firstname='Testing-firstname', lastname='Testing-lastname')
invalid_username_query_profile_list = [dict(username=""), dict(username="!@#$%^&")]
invalid_bio_query_profile = dict(
    bio="Trump was born and raised in Queens, a borough of New York City, and received a bachelor's degree in economics from the Wharton School. He took charge of his family's real-estate business in 1971, renamed it The Trump Organization, and expanded its operations from Queens and Brooklyn into Manhattan. The company built or renovated skyscrapers, hotels, casinos, and golf courses. Trump later started various side ventures, mostly by licensing his name. He bought the Miss Universe brand of beauty pageants in 1996, and sold it in 2015. He produced and hosted The Apprentice, a reality television series, from 2003 to 2015. As of 2020, Forbes estimated his net worth to be $2.1 billion.[a]Trumps political positions have been described as populist, protectionist, and nationalist. He entered the 2016 presidential race as a Republican and was elected in a surprise victory over Democratic nominee Hillary Clinton, although he lost the popular vote.[b] He became the oldest first-term U.S. president,[c] and the first without prior military or government service. His election and policies have sparked numerous protests. Trump has made many false or misleading statements during his campaign and presidency. The statements have been documented by fact-checkers, and the media have widely described the phenomenon as unprecedented in American politics. Many of his comments and actions have been characterized as racially charged or racist.During his presidency, Trump ordered a travel ban on citizens from several Muslim-majority countries, citing security concerns; after legal challenges, the Supreme Court upheld the policy's third revision. He enacted a tax-cut package for individuals and businesses, rescinding the individual health insurance mandate penalty. He appointed Neil Gorsuch and Brett Kavanaugh to the Supreme Court. In foreign policy, Trump has pursued an America First agenda, withdrawing the U.S. from the Trans-Pacific Partnership trade negotiations, the Paris Agreement on climate change, and the Iran nuclear deal. He imposed import tariffs which triggered a trade war with China, recognized Jerusalem as the capital of Israel, and withdrew U.S. troops from northern Syria. Trump met thrice with North Koreas leader Kim Jong-un, but talks on denuclearization broke down in 2019. Trump began running for a second term shortly after becoming president.A special counsel investigation led by Robert Mueller found that Trump and his campaign welcomed and encouraged Russian interference in the 2016 presidential election under the belief that it would be politically advantageous, but did not find sufficient evidence to press charges of criminal conspiracy or coordination with Russia.[d] Mueller also investigated Trump for obstruction of justice, and his report neither indicted nor exonerated Trump on that offense. After Trump solicited the investigation of a political rival by Ukraine, the House of Representatives impeached him in December 2019 for abuse of power and obstruction of Congress. The Senate acquitted him of both charges in February 2020.")
invalid_user_id_query_profile_list = [" ", "2134567"]

# Update User Profile Picture
image_name_profile_pic = 'Testing'
missing_image_name_profile_pic = ''
image_body_profile_pic = get_encode_base64_image(random.sample(image_path_list_code_200, 1)[0])
image_body_profile_pic_code_400 = get_encode_base64_image(random.sample(image_path_list_code_400, 1)[0])
image_body_profile_pic_code_413 = get_encode_base64_image(random.sample(image_path_list_code_413, 1)[0])
missing_image_body_profile_pic = ""
invalid_image_body_profile_pic_list = ["12345678", 'abc', '#$%^&']

# Remove User Profile Picture
invalid_user_id_remove_profile_pic_list = [' ', '123455']

# Follower and Following (Add/Get/Remove)
follow_target_email = 'follower' + datetime.datetime.now().strftime("%m%d%H%M%S") + "@gmail.com"
follow_target_password = 'follow1234'
follow_target_device_id = '24680'
invalid_target_user_id_list = ['', '123456789']
invalid_user_id_get_follower_list = [' ', '12345678']
invalid_user_id_get_following_list = [' ', '12345678']

# Favourite Snap (Add/Get/Remove)
invalid_snap_id_fav_snap_list = ['1234567', ' ', 'abc']

# Favourite Product (Add/Get/Remove)
fav_snap_id = '34'
invalid_user_id_get_fav_product_list = [unauthorized_user_id, ' ', '12345678']
invalid_snap_id_add_fav_snap_product_list = ['1234567', ' ', 'abc']
invalid_snap_id_remove_fav_snap_product_list = ['1234567', ' ', 'abc']
search_snap_query_fav = {"offset": 1234}

# Get Snaps of a User
invalid_snap_id_get_user_snap_list = [' ', '12234567']
invalid_query_get_user_snap = [{'order': 'abc'}]

# Forget Password
missing_email_forget_pass = ''
invalid_email_forget_pass = ['12345@fdvbvdsfrte5rf', 'abc', '2$%^&*(']

# Report User
report_user_param = dict(user_id="5112", report_type="1", remark="")
missing_report_type = " "
invalid_report_type_list = ['123', 'abc', '#$%', ' ']
missing_user_id = " "
invalid_user_id_list = ['abc', '456787654', '%^&*']

# Check Username valid
unexisting_username_list = ['qwertyuio', 'br4567ujb', '098765tgb']
invalid_username_list = ['@#$', 'dsfhj@gmai.com', '3435!$#']

def main():
    print(image_body_profile_pic)


main()
