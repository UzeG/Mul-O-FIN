# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 08:27:59 2023

@author: xiaoleiwww
"""

import requests

# URL
url = "http://127.0.0.1:8000/api/template/"
# JSON data
data = {
    "event_name": "Sample Event2",
    "input_device": 9,
    "role_num": 2,
    "time_window": 15,
    "output_device": 9,
    "port": 3,
    "duration": 5,
    "pwm": 200,
    "uuid": "59253dd3-c200-47a7-b548-0972fef06ec0"
}

# Send POST request
response = requests.post(url, json=data)

# Check response
if response.status_code == 200:
    print("POST request successful")
    print("Response:", response.json())
else:
    print("POST request failed")
    print("Response:", response.text)
