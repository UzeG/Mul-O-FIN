# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 19:07:31 2023

@author: xiaol
"""

import time
import socket
import threading
import select
import random

SEND_INTERVAL = 0.05  # 发送间隔，单位秒
RECEIVE_TIMEOUT = 5.0  # 接收超时时间，单位秒


def tcp_control(tcp_socket):
    # 生成 16 位随机整数，用于标识tcp链接
    random_id = random.randint(0x00000000, 0xffffffff)
    # 将整数格式化为 16 进制字符串
    hex_id = hex(random_id)

    last_receive_time = time.time()
    while True:
        try:
            # 发送数据到服务器
            message = hex_id
            tcp_socket.sendall(message.encode("utf-8"))
            # 使用 select 检查 socket 是否准备好接收数据
            ready_to_read, _, _ = select.select([tcp_socket], [], [], RECEIVE_TIMEOUT)
            if tcp_socket in ready_to_read:
                recv_data = tcp_socket.recv(1024)
                if not recv_data:
                    break
                # 接收到的数据，"0"表示已接收，否则则需要解包
                recv_data_str = recv_data.decode("utf-8")
                if recv_data_str != "0":
                    print(f"Received data from server: {recv_data_str}")
                    
                    '''在这里添加你的控制逻辑，根据收到的数据来控制'''
                    '''以下为数据案例：'''
                    '''Odor: pie, Port: 1, Start: 0.0, Duration: 3.0, Intensity: 100.0'''
                    '''{pie,1,0.0,100.0}'''
                    
                last_receive_time = time.time()
            else:
                raise TimeoutError("Receive timeout")

            # 计算接收速度
            current_time = time.time()
            receive_duration = current_time - last_receive_time
            # print(f"Receive duration: {receive_duration:.3f} seconds")

            # 如果接收速度过慢，调整发送频率
            if receive_duration > 1.0:  # 假设大于1秒认为速度过慢
                global SEND_INTERVAL
                SEND_INTERVAL += 0.02  # 增加发送间隔
                print(f"Receive speed is slow. Adjusting send interval to {SEND_INTERVAL} seconds.")
            else:
                SEND_INTERVAL = 0.05  # 恢复默认发送间隔

            # 停顿指定间隔后再发送
            time.sleep(SEND_INTERVAL)

        except TimeoutError:
            print("Receive timeout, re-sending message...")
            continue

        except Exception as e:
            print(f"Error: {e}")
            break

def handle_tcp_connection():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_ip = "101.42.17.45" #此处填写IP
    server_ip = "127.0.0.1"
    server_port = 7890
    server_addr = (server_ip, server_port)
    print(server_addr)
    try:
        tcp_socket.connect(server_addr)
        print(f"Connected to server {server_ip}:{server_port}")
        
        # 启动发送消息的线程
        send_thread = threading.Thread(target=tcp_control, args=(tcp_socket,))
        send_thread.start()

        # 主线程继续保持与服务器的连接
        while True:
            pass

    except Exception as e:
        print(f"Connection error: {e}")

    finally:
        tcp_socket.close()
        print("TCP connection closed")

def main():
    handle_tcp_connection()

if __name__ == "__main__":
    main()

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
