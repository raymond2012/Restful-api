import base64

import requests
import json
import pytest
import datetime
import logging
import urllib

temp = {
    "filter": "filter-v",
    "offset": "offset-v",
    "offset_id": "offset_id-v"
}


def test():
    with open(r"C:\Users\user\Downloads\768px-Python-logo-notext.svg.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        print(encoded_string)


print(test())
