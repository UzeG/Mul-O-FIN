# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:09:40 2023

@author: xiaol
"""

import requests

url = "http://127.0.0.1:8000/api/event/"

# Enter your uuid and eventID, here is an example
data = {
    "uuid": "f5bda815-563e-4665-8a7c-261328d5107c",
    "event": "Event_1"
}
response = requests.post(url, json=data)

if response.status_code == 200:
    print("POST request successful!")
    print("Response:", response.text)
else:
    print("POST request failed. Status code:", response.status_code)
