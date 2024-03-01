# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 11:04:51 2023

@author: xiaol
"""

import machine
import time
import urequests
import network
import uasyncio as asyncio

TRIG_PIN = 12  # 替换为你连接到ESP32的Trig引脚
ECHO_PIN = 13  # 替换为你连接到ESP32的Echo引脚

trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

def measure_distance():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    duration = machine.time_pulse_us(echo, 1)
    distance = duration * 0.034 / 2  # 根据声速计算距离
    return distance

# 连接WiFi网络
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Future Lab-6F', 'weilaishiyanshi')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


        
do_connect()  # 连接WiFi
while True:
    distance = measure_distance()
    print("Distance:", distance, "cm")
    
    if distance < 2000:
        url = "http://101.42.17.45:8000/api/event/"
        data = {
            "uuid": "",
            "event": ""
        }

        response = urequests.post(url, json=data)

        if response.status_code == 200:
            print("POST request successful!")
            print("Response:", response.text)
        else:
            print("POST request failed. Status code:", response.status_code)

