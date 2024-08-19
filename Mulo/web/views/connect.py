from django.shortcuts import render
from web.models import Device
import socket


def check_device_connection(device):
    try:
        # 创建一个套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置连接超时时间为 1 秒钟
        s.settimeout(1)
        # 尝试连接设备
        s.connect((device.ip, device.port))
        # 连接成功则设备已连接

        return True
    except socket.timeout:
        # 连接超时，则设备未连接
        return False
    except ConnectionRefusedError:
        # 连接被拒绝，则设备未连接
        return False
    finally:
        # 关闭套接字连接
        s.close()


def device_list(request):
    devices = Device.objects.all()  # 获取所有设备对象

    connected_devices = []  # 存储已连接的设备列表

    for device in devices:  # 遍历设备列表
        check_device_connection(device)  # 调用检查连接状态的函数，传递当前设备对象

        if device.is_connected:  # 如果设备已连接
            connected_devices.append(device)  # 将设备添加到已连接设备列表

    return render(request, 'admin_device.html', {'admin_device': connected_devices})
