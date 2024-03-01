# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 10:24:38 2023

@author: xiaol
"""

import re
import time
import sys
import machine
import network
import socket
import uasyncio as asyncio
from machine import PWM, Pin


def do_connect():
    # 作用：连接wifi网络
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Future Lab-6F', 'weilaishiyanshi')
        i = 1
        while not wlan.isconnected():
            print("正在连接网络...{}".format(i))
            time.sleep(1)
    print('network config:', wlan.ifconfig())
    
    # 连接成功后启动HTTP服务器
    loop = asyncio.get_event_loop()
    loop.create_task(start_http_server())


async def start_http_server():
    server = await asyncio.start_server(handle_http_request, '0.0.0.0', 80)
    print('HTTP server started')
    
    async with server:
        await server.serve_forever()


async def handle_http_request(reader, writer):
    request = await reader.read()
    request_str = request.decode()
    headers = request_str.split("\r\n")
    method, path, _ = headers[0].split(" ")
    
    if method == "GET" and path == "/check_device":
        response = b"connected" if isDeviceConnected else b"disconnected"
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(response), response))
    else:
        response = b"Not Found"
        writer.write(b"HTTP/1.1 404 Not Found\r\nContent-Length: %d\r\n\r\n%s" % (len(response), response))
    
    await writer.drain()
    writer.close()


async def update_device_status():
    global isDeviceConnected
    
    while True:
        # 检测设备连接状态的条件
        if condition:
            isDeviceConnected = True
        else:
            isDeviceConnected = False
        
        await asyncio.sleep(5)  # 每5秒钟检测一次


def main():
    do_connect()
    
    global isDeviceConnected
    isDeviceConnected = False

    loop = asyncio.get_event_loop()
    loop.create_task(update_device_status())

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "192.168.20.195"
    server_port = 7890
    server_addr = (server_ip, server_port)
    print(server_addr)
    tcp_socket.connect(server_addr)
    
    while True:
        recv_data, sender_info = tcp_socket.recvfrom(1024)
        print("{}发送的数据：{}".format(sender_info, recv_data))
        recv_data_str = recv_data.decode("utf-8")
        print("解码后的数据：{}".format(recv_data_str))
  
        if (recv_data_str == "d1p1") or (recv_data_str == "allp1"):
            print("d1p1 on")
            fan1 = PWM(Pin(26), freq=1000)
            fan1.duty(1023)
            time.sleep_ms(5000)
            fan1.duty(0)
        elif (recv_data_str == "d1p2") or (recv_data_str == "allp2"):
            print("d1p2 on")
            fan2 = PWM(Pin(25), freq=1000)
            fan2.duty(1023)
            time.sleep_ms(5000)
            fan2.duty(0)
        elif (recv_data_str == "d1p3") or (recv_data_str == "allp3"):
            print("d1p3 on")
            fan3 = PWM(Pin(5), freq=1000)
            fan3.duty(1023)
            time.sleep_ms(5000)
            fan3.duty(0)
        elif (recv_data_str == "d1p4") or (recv_data_str == "allp4"):
            print("d1p4 on")
            fan4 = PWM(Pin(23), freq=1000)
            fan4.duty(1023)
            time.sleep_ms(5000)
            fan4.duty(0)
        else:
            # 格式为"d1p1t1"
            match_t = re.search(r't(\d+)', recv_data_str)
            match_p = re.search(r'p(\d+)', recv_data_str)
            t = 5000
            p = 1
            if match_t:
                t = match_t.group(1)*1000
            if match_p:
                p = match_p.group(1)
            
            if int(p) == 1:
                print("p1 on")
                fan1 = PWM(Pin(26), freq=1000)
                fan1.duty(1023)
                time.sleep_ms(t)
                fan1.duty(0)    
            elif int(p) == 2:
                print("p2 on")
                fan2 = PWM(Pin(25), freq=1000)
                fan2.duty(1023)
                time.sleep_ms(t)
                fan2.duty(0)
            elif int(p) == 3:
                print("p3 on")
                fan3 = PWM(Pin(5), freq=1000)
                fan3.duty(1023)
                time.sleep_ms(t)
                fan3.duty(0)
            elif int(p) ==  4:
                print("p4 on")
                fan4 = PWM(Pin(23), freq=1000)
                fan4.duty(1023)
                time.sleep_ms(t)
                fan4.duty(0)
            
            

if __name__ == "__main__":
    main()

