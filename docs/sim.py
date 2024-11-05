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

SEND_INTERVAL = 0.05  # Sending interval, in seconds
RECEIVE_TIMEOUT = 5.0  # Receive timeout, in seconds


def tcp_control(tcp_socket):
    # Generate a 16-bit random integer to identify the TCP connection
    random_id = random.randint(0x00000000, 0xffffffff)
    # Format the integer as a hexadecimal string
    hex_id = hex(random_id)

    last_receive_time = time.time()
    while True:
        try:
            # Send data to the server
            message = hex_id
            tcp_socket.sendall(message.encode("utf-8"))
            # Use select to check if the socket is ready to receive data
            ready_to_read, _, _ = select.select([tcp_socket], [], [], RECEIVE_TIMEOUT)
            if tcp_socket in ready_to_read:
                recv_data = tcp_socket.recv(1024)
                if not recv_data:
                    break
                # Received data, "0" indicates it has been received, otherwise unpacking is needed
                recv_data_str = recv_data.decode("utf-8")
                if recv_data_str != "0":
                    print(f"Received data from server: {recv_data_str}")

                    '''Add your control logic here based on the received data'''
                    '''Following is an example of the data format:'''
                    '''Odor: pie, Port: 1, Start: 0.0, Duration: 3.0, Intensity: 100.0'''
                    '''{pie,1,0.0,3.0,100.0}'''

                last_receive_time = time.time()
            else:
                raise TimeoutError("Receive timeout")

            # Calculate reception duration
            current_time = time.time()
            receive_duration = current_time - last_receive_time
            # print(f"Receive duration: {receive_duration:.3f} seconds")

            # If the reception speed is too slow, adjust the sending frequency
            if receive_duration > 1.0:  # Assume slower than 1 second is considered too slow
                global SEND_INTERVAL
                SEND_INTERVAL += 0.02  # Increase sending interval
                print(f"Receive speed is slow. Adjusting send interval to {SEND_INTERVAL} seconds.")
            else:
                SEND_INTERVAL = 0.05  # Restore default sending interval

            # Sleep for the specified interval before sending again
            time.sleep(SEND_INTERVAL)

        except TimeoutError:
            print("Receive timeout, re-sending message...")
            continue

        except Exception as e:
            print(f"Error: {e}")
            break


def handle_tcp_connection():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Fill in the IP address here
    server_ip = "127.0.0.1"
    server_port = 7890
    server_addr = (server_ip, server_port)
    print(server_addr)
    try:
        tcp_socket.connect(server_addr)
        print(f"Connected to server {server_ip}:{server_port}")

        # Start a thread to send messages
        send_thread = threading.Thread(target=tcp_control, args=(tcp_socket,))
        send_thread.start()

        # Main thread continues to maintain the connection with the server
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
