from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from web.utils.form import OdorModelForm, TemplateModelForm, RoleModelForm, \
    RoleSelectionModelForm, DeviceModelForm
from web.models import Template, UserProfile, Device
from web import models
import socket
import threading
import pymysql
from web.controller.sockets import sockets

from web.utils.code import get_template_tree


@login_required
def admin_main(request):
    """ 管理员主页面 """
    return render(request, 'admin_main.html')


# @login_required
def admin_teaching(request):
    """ 教学页面 """
    return render(request, "admin_teaching.html")


@csrf_exempt
# 处理客户端请求的任务
def admin_teaching_handle_client_request(request):
    # 5. 接收客户端的数据
    # 收发消息都是用返回的这个新的套接字
    # 循环接收客户端的消息
    send_content = request.POST.get('ref')
    for client in sockets:
        # 对字符串进行编码
        send_data = send_content.encode("utf-8")
        # 6. 发送数据到客户端
        try:
            client.send(send_data)
        except Exception as e:
            print("admin_teaching_handle_restart:", e)
            sockets.remove(client)

    # 关闭服务与客户端套接字，表示和客户端终止通信
    # new_client.close()
    return HttpResponse("ok")


def handle_client_request(client_socket):
    ip, port = client_socket.getpeername()
    print(f"New client connected: {ip}:{port}")
    device = None

    try:
        # 在数据库中创建设备记录
        device, created = Device.objects.get_or_create(ip=ip, port=port)
        if created:
            print("Device created successfully")
        else:
            print("Device already exists")

        device.is_connected = True
        device.save()
        print("Device connected status updated")
    except Exception as e:
        print(f"Database error: {e}")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received data from {ip}:{port}: {data.decode('utf-8')}")  # 解码接收到的数据
            # 在此处处理从客户端接收到的数据，例如可以发送响应给客户端
            response = b"Message received"
            client_socket.sendall(response)
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error processing data: {e}")
            break

    try:
        device.is_connected = False
        device.save()
        print("Device connected status updated")
    except Exception as e:
        print(f"Database error: {e}")

    client_socket.close()
    print(f"Client {ip}:{port} disconnected")


@csrf_exempt
def admin_teaching_tcp_conn(request: object) -> object:
    # 1. 创建 tcp 服务端套接字
    # AF_INET: ipv4 , AF_INET6: ipv6
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用，表示意思：服务端程序退出端口号立即释放
    # a. SOL_SOCKET：表示当前套接字
    # b. SO_REUSEADDR：表示复用端口号的选项
    # c. True：确认复用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 2. 绑定端口号
    # 第一个参数表示 ip 地址，一般不用指定，表示本机的任何一个 ip 即可
    # 第二个参数表示端口号
    server_socket.bind(("", 7890))
    # 3. 设置监听
    # 128：表示最大等待建立连接的个数
    server_socket.listen(128)
    print("TCP server started on port 7890")
    # 4. 等待接受客户端的连接请求
    # 注意点：每次当客户端和服务端建立连接成功都会返回一个新的套接字
    # tcp_server_socket 只负责等待接收客户端的连接请求，收发消息不使用该套接字
    # 循环等待接收客户端的连接请求
    while True:
        client_socket, addr = server_socket.accept()
        print("client connected from", addr)
        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))
        client_handler.daemon = True
        client_handler.start()


@login_required
def admin_reality(request):
    """ reality 界面 """
    user_profile = UserProfile.objects.get(user=request.user)

    form_template = TemplateModelForm()
    # form_odor = OdorModelForm()
    odor_list = models.Odor.objects.all().order_by('-id')
    role_list = models.Role.objects.all().order_by('-id')

    # template_tree 树形结构
    template_tree = get_template_tree(user_profile)

    context = {
        'odor_list': odor_list,
        # 'form_odor': form_odor,
        'form_template': form_template,
        'role_list': role_list,
        'template_tree': template_tree,
    }
    return render(request, 'admin_reality.html', context)


@csrf_exempt
def admin_reality_role(request):
    """ 创建新角色 """
    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def admin_reality_role_delete(request, rid):
    """ 删除角色 """
    models.Role.objects.filter(id=rid).delete()
    return redirect('/admin/reality/')


@csrf_exempt
def admin_reality_odor(request):
    """ 创建新气味 """
    form = OdorModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def admin_reality_odor_delete(request, oid):
    """ 删除气味 """
    models.Odor.objects.filter(id=oid).delete()
    return redirect('/admin/reality/')


@csrf_exempt
def admin_reality_add(request):
    """ 新建事件范式（Ajax 请求） """
    form = TemplateModelForm(data=request.POST)
    if form.is_valid():
        # 创建 Template 对象
        try:
            user_profile = UserProfile.objects.get(user=request.user)

            template = Template.objects.create(
                event_name=form.cleaned_data['event_name'],
                uuid=user_profile.uuid,
                threshold=form.cleaned_data['threshold'],
                time_window=form.cleaned_data['time_window'],
                input_description=form.cleaned_data['input_description'],
                output_device=form.cleaned_data['output_device'],
                total_time=form.cleaned_data['total_time'],
            )
            template.save()

            return JsonResponse({"status": True, 'tid': template.id})

        except Exception as e:
            print(e)
            return JsonResponse({"status": False, 'error': e})

    return JsonResponse({"status": False, 'error': form.errors})


def admin_reality_delete(request, tid):
    """ 删除事件范式 """
    models.Template.objects.filter(id=tid).delete()
    return redirect('/admin/reality/')


def admin_reality_detail(request):
    """ 根据 ID 获取订单信息 """
    """  方式 1   uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'error': '数据不存在'})

    # 从数据库中获取到一个对象 row_object
    result = {
        'status': True,
        'data': {
            'title': row_object.title,
            'price': row_object.price,
            'status': row_object.status,
        }
    }
    return JsonResponse(result) """

    # 方式 2
    tid = request.GET.get('tid')
    row_dict = models.Template.objects.filter(id=tid) \
        .values('event_name', 'input_description', 'threshold', 'time_window', 'output_device', 'total_time',
                'parent_id') \
        .first()
    if not row_dict:
        return JsonResponse({'status': False, 'error': 'The data does not exist.'})

    # 从数据库中获取到一个对象 row_object
    result = {
        'status': True,
        'data': row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def admin_reality_edit(request):
    """ 编辑事件范式 """
    tid = request.GET.get("tid")
    row_object = models.Template.objects.filter(id=tid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': "The data does not exist."})

    form = TemplateModelForm(data=request.POST, instance=row_object)
    print('before', models.Template.objects.filter(id=tid).first().parent_id)
    if form.is_valid():
        form.save()
        print('after', models.Template.objects.filter(id=tid).first().parent_id)
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


@login_required
def admin_device(request):
    """ 设备管理界面 """
    form_role = RoleModelForm()
    form_role_selection = RoleSelectionModelForm()
    form_device = DeviceModelForm()
    device_list = models.Device.objects.all().order_by('-id')
    context = {
        'form_role': form_role,
        'form_role_selection': form_role_selection,
        'form_device': form_device,
        'device_list': device_list,
    }
    return render(request, 'admin_device.html', context)


@login_required
def admin_virtual_reality(request):
    """ VR 界面 """
    form_odor = OdorModelForm()
    context = {
        'form_odor': form_odor,
    }
    return render(request, 'admin_virtual_reality.html', context)
