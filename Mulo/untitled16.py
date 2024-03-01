# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:09:40 2023

@author: xiaol
"""

import requests

url = "http://101.42.17.45:8000/api/event/"
'''
data = {
    "uuid": "59253dd3-c200-47a7-b548-0972fef06ec0",
    "event": "123",
    "time": "10:25"
}
'''
data = {
    "uuid": "59253dd3-c200-47a7-b548-0972fef06ec0",
    "event": "123"
}
response = requests.post(url, json=data)

if response.status_code == 200:
    print("POST request successful!")
    print("Response:", response.text)
else:
    print("POST request failed. Status code:", response.status_code)
