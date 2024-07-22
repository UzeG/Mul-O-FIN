# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import time
import socket
import network
import uasyncio as asyncio
import random
import select
from machine import PWM, Pin

SSID = 'Future Lab-6F'
PASSWORD = 'weilaishiyanshi'
SEND_INTERVAL = 0.05  # Initial send interval, in seconds
RECEIVE_TIMEOUT = 5.0  # Receive timeout, in seconds

async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            print('Waiting for connection...')
            await asyncio.sleep(1)
    print('Network connected:', wlan.ifconfig())

async def tcp_control(tcp_socket):
    global SEND_INTERVAL
    random_id = random.getrandbits(32)
    hex_id = hex(random_id)

    last_receive_time = time.time()

    while True:
        try:
            # Send data to the server
            message = hex_id
            tcp_socket.sendall(message.encode("utf-8"))

            # Check if the socket is ready to receive data
            await asyncio.sleep(0)  # Yield control to other coroutines
            ready_to_read, _, _ = select.select([tcp_socket], [], [], RECEIVE_TIMEOUT)
            if tcp_socket in ready_to_read:
                recv_data = tcp_socket.recv(1024)
                if not recv_data:
                    break
                
                recv_data_str = recv_data.decode("utf-8")
                
                last_receive_time = time.time()
                
                if recv_data_str != "0":
                    print(f"Received data from server: {recv_data_str}")
                    
                    '''Add your control logic here based on received data'''
                    '''Example data: Odor: pie, Port: 1, Start: 0.0, Duration: 3.0, Intensity: 100.0'''
                    '''{pie,1,0.0,3.0,100.0}'''
                    
                    if recv_data_str.startswith("{") and recv_data_str.endswith("}"):  
                        recv_data_str = recv_data_str[1:-1]  
                    parts = recv_data_str.split("}{")   
                    data_list = [part for part in parts] 
                    
                    data_map_list = []
                    
                    max_duration = 0.0
                    
                    for data_str in data_list:
                        # Regular expression to extract data
                        split_str = data_str.split(",")
                        odor, port, start, duration, intensity = split_str[0], split_str[1], split_str[2], split_str[3], split_str[4]

                        # Convert to map
                        data_map = {
                            "Odor": odor,
                            "Port": int(port),
                            "Start": float(start),
                            "Duration": float(duration),
                            "Intensity": float(intensity)
                        }
                        data_map_list.append(data_map)
                        max_duration = max(max_duration, float(duration))*1000
                    
                    pwm_start_time = time.time()
                    pin_list = [26,25,5,23]
                    fan = []
                    fan_duty = []
                    for pin in pin_list:
                        fan.append(PWM(Pin(pin)))
                        fan_duty.append(0)
                        
                    while True:
                        for data_map in data_map_list:
                            duty = int(1023*100)/data_map["Intensity"]
                            t = int(1000*data_map["Duration"])
                            f = fan[data_map["Port"]-1]
                            if pwm_start_time + t < time.time():
                                if fan_duty[data_map["Port"]-1] == 0:
                                    fan_duty[data_map["Port"]-1] = duty
                                    f.duty(int(1023*100)/data_map["Intensity"])
                            else:
                                f.duty(0)
                                fan_duty[data_map["Port"]-1] = 0    
                        if pwm_start_time + max_duration > time.time():
                            break
                    
                    
            else:
                raise print("Receive timeout")

            current_time = time.time()
            receive_duration = current_time - last_receive_time

            if receive_duration > 1.0:
                SEND_INTERVAL += 0.02
                print(f"Receive speed is slow. Adjusting send interval to {SEND_INTERVAL} seconds.")
            else:
                SEND_INTERVAL = 0.05

            await asyncio.sleep(SEND_INTERVAL)

        except Exception as e:
            print(f"Error: {e}")
            break

async def handle_tcp_connection():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_ip = "101.42.17.45" # Replace with actual server IP
    server_ip = "192.168.0.106"
    server_port = 7890
    server_addr = (server_ip, server_port)
    print(server_addr)
    
    try:
        tcp_socket.connect(server_addr)
        print(f"Connected to server {server_ip}:{server_port}")
        
        await tcp_control(tcp_socket)

    except Exception as e:
        print(f"Connection error: {e}")

    finally:
        tcp_socket.close()
        print("TCP connection closed")

async def main():
    await connect_wifi()
    await handle_tcp_connection()

if __name__ == "__main__":
    asyncio.run(main())



