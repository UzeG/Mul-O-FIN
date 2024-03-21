from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from web.utils.form import OdorModelForm, TemplateModelForm, RoleModelForm, \
    RoleSelectionModelForm, DeviceModelForm
from web.models import Template
from web import models
from web.models import UserProfile
import socket
import threading
import pymysql
from web.controller.sockets import sockets
import uuid
from django.http import QueryDict


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


@csrf_exempt
def admin_teaching_tcp_conn(request):
    # 1. 创建 tcp 服务端套接字
    # AF_INET: ipv4 , AF_INET6: ipv6
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用，表示意思：服务端程序退出端口号立即释放
    # a. SOL_SOCKET：表示当前套接字
    # b. SO_REUSEADDR：表示复用端口号的选项
    # c. True：确认复用
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 2. 绑定端口号
    # 第一个参数表示 ip 地址，一般不用指定，表示本机的任何一个 ip 即可
    # 第二个参数表示端口号
    tcp_server_socket.bind(("", 7890))
    # 3. 设置监听
    # 128：表示最大等待建立连接的个数
    tcp_server_socket.listen(128)
    # 4. 等待接受客户端的连接请求
    # 注意点：每次当客户端和服务端建立连接成功都会返回一个新的套接字
    # tcp_server_socket只负责等待接收客户端的连接请求，收发消息不使用该套接字
    # 循环等待接收客户端的连接请求
    print("服务器启动成功")
    while True:
        new_client, ip_port = tcp_server_socket.accept()
        print("一个新的客户端已经到来", ip_port)
        ip, port = ip_port
        print("ip为", ip)
        print(type(ip))
        print("port为", port)
        print(type(port))
        # 创建连接，数据库主机地址 数据库用户名称 密码 数据库名 数据库端口 数据库字符集编码
        conn = pymysql.connect(host='localhost', user='root', password='root', database='mulo', port=3306,
                               charset='utf8')
        print('连接成功')
        # 创建游标
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO mulo.web_device(ip, port) values('%s','%s')"%(ip, port))
        cursor.execute(
            "INSERT INTO mulo.web_device(ip, port, is_connected) VALUES ('%s', '%s', False)" % (ip, port))

        conn.commit()
        # 代码执行到此，说明客户端和服务端建立连接成功
        sockets.append(new_client)
        # 当客户端和服务端建立连接成功，创建子线程，让子线程专门负责接收客户端的消息
        # sub_thread = threading.Thread(target=admin_teaching_handle_client_request(request))
        sub_thread = threading.Thread(target=admin_teaching_handle_client_request, args=(new_client,))
        # 设置守护主线程，主线程退出子线程直接销毁
        sub_thread.daemon = True
        # 启动子线程执行对应的任务
        sub_thread.start()
    # 7. 关闭服务端套接字，表示服务端以后不再等待接收客户端的连接请求
    # tcp_server_socket.close() # 因为服务端的程序需要一直运行，所以关闭服务端套接字的代码可以省略不写


@login_required
def admin_reality(request):
    """ reality界面 """
    user_profile = UserProfile.objects.get(user=request.user)

    form_template = TemplateModelForm()
    # form_odor = OdorModelForm()
    odor_list = models.Odor.objects.all().order_by('-id')
    role_list = models.Role.objects.all().order_by('-id')
    template_list = models.Template.objects.filter(uuid=user_profile.uuid).order_by('-id')

    context = {
        'odor_list': odor_list,
        # 'form_odor': form_odor,
        'form_template': form_template,
        'role_list': role_list,
        'template_list': template_list,
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
    """ 新建事件范式（Ajax请求） """
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
    """ 根据ID获取订单信息 """
    """  方式1   uid = request.GET.get('uid')
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

    # 方式2
    tid = request.GET.get('tid')
    row_dict = models.Template.objects.filter(id=tid)\
        .values('event_name', 'input_description', 'threshold', 'time_window', 'output_device', 'total_time', 'parent_id')\
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
    if form.is_valid():
        form.save()
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
    """ VR界面 """
    form_odor = OdorModelForm()
    context = {
        'form_odor': form_odor,
    }
    return render(request, 'admin_virtual_reality.html', context)
