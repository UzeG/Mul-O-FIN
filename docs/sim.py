# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 19:07:31 2023

@author: xiaol
"""

import time
import socket
import threading

def handle_tcp_connection():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_ip = "101.42.17.45" #此处填写IP
    server_ip = "127.0.0.1"
    server_port = 7890
    server_addr = (server_ip, server_port)
    print(server_addr)
    tcp_socket.connect(server_addr)
    print("success")
    while True:
        recv_data = tcp_socket.recv(1024)
        recv_data_str = recv_data.decode("utf-8")
        print("Received data: {}".format(recv_data_str))

        # 在这里添加你的风扇控制逻辑，根据收到的数据来控制风扇

def main():

    handle_tcp_connection()

if __name__ == "__main__":
    main()
