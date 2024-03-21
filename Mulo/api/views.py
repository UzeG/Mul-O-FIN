import json

import django.core.serializers
from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from web.models import Device, Role, Odor, UserProfile, Template, TemplateOdorModel
from web.controller.interactive import find_template, convert_template
from web.controller.interactive import Interactive
from web.middleware.auth import is_valid_uuid
from rest_framework import permissions
from django.forms.models import model_to_dict

import datetime
from django.core.serializers import serialize

interactive = Interactive()


class LoginView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):

        ret = {'request': '/api/login/', 'error_code': '10001', 'error': 'System error'}

        username = request.data.get('username')
        password = request.data.get('password')

        if not (isinstance(username, str) and isinstance(password, str)):
            ret['request'] = '/api/login/'
            ret['error_code'] = '10008'
            ret['error'] = 'Param error, see doc for more info'
            return JsonResponse(ret)

        user = authenticate(username=username, password=password)
        if user is not None:

            # 检查用户是否有关联的 UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            if created:
                # 如果创建了新的 UserProfile，可以在这里进行一些初始化设置
                pass

            print(username, user_profile.uuid)

            login(request, user)
            ret['request'] = '/api/login/'
            ret['error_code'] = '0'
            ret['error'] = 'Success'
            return JsonResponse(ret)
        else:
            ret['request'] = '/api/login/'
            ret['error_code'] = '21302'
            ret['error'] = 'Username or password error'
            return JsonResponse(ret)


class RegView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        ret = {'request': '/api/reg/', 'error_code': '10001', 'error': 'System error'}

        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not (isinstance(username, str) and isinstance(password, str)):
            ret['error_code'] = '10008'
            ret['error'] = 'Param error, see doc for more info'
            return JsonResponse(ret)

        if User.objects.filter(username=username).exists():
            ret['error_code'] = '21110'
            ret['error'] = 'The username has been used'
            return JsonResponse(ret)

        # check password
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            ret['error_code'] = '0'
            ret['error'] = 'Success'
            return JsonResponse(ret)

        except Exception as e:
            print(e)
            return JsonResponse(ret)


class LogoutView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        ret = {'request': '/api/logout/', 'error_code': '10001', 'error': 'System error'}

        try:
            logout(request)
            ret['error_code'] = '0'
            ret['error'] = 'Success'
            return JsonResponse(ret)

        except Exception as e:
            print(e)
            return JsonResponse(ret)


class EventView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        ret = {'request': '/api/event/', 'error_code': '10001', 'error': 'System error'}

        uuid = request.data.get('uuid')
        event_name = request.data.get('event')

        if not (isinstance(uuid, str) and isinstance(event_name, str)):
            ret['request'] = '/api/event/'
            ret['error_code'] = '10008'
            ret['error'] = 'Param error, see doc for more info'
            return JsonResponse(ret)

        if not is_valid_uuid(uuid):
            ret['request'] = '/api/event/'
            ret['error_code'] = '21124'
            ret['error'] = 'Wrong uuid code'
            return JsonResponse(ret)

        # 处理event的数据信息
        template = find_template(uuid, event_name)

        if template:

            template_data = convert_template(template)

            interactive.control(template_data)

            ret['error_code'] = '0'
            ret['error'] = 'Success'
            return JsonResponse(ret)

        else:
            ret['request'] = '/api/event/'
            ret['error_code'] = '21125'
            ret['error'] = 'Cannot find the template'
            return JsonResponse(ret)


class DateView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        ret = {'request': datetime.datetime.now()}

        return JsonResponse(ret)


class ClearView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        ret = {'request': '/api/clear/', 'error_code': '10001', 'error': 'System error'}

        authid = request.data.get('authid')
        typename = request.data.get('type')

        if authid == "ASDWi3qwydfweg":
            if typename == "device":
                Device.objects.all().delete()
            if typename == "role":
                Role.objects.all().delete()
            if typename == "odor":
                Odor.objects.all().delete()
            if typename == "template":
                Template.objects.all().delete()

            ret['request'] = '/api/event/'
            ret['error_code'] = '0'
            ret['error'] = 'Success'

            return JsonResponse(ret)

        ret['request'] = '/api/event/'
        ret['error_code'] = '10008'
        ret['error'] = 'Param error, see doc for more info'
        return JsonResponse(ret)


class TemplateView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        ret = {'request': '/api/template/', 'error_code': '10001', 'error': 'System error'}

        # 从请求数据中获取模型字段值
        event_name = request.data.get('event_name')
        uuid = request.data.get('uuid')
        role_num = request.data.get('role_num')
        time_window = request.data.get('time_window')
        input_device_id = request.data.get('input_device')
        output_device_id = request.data.get('output_device')
        port = request.data.get('port')
        duration = request.data.get('duration')
        pwm = request.data.get('pwm')

        # 在创建 Template 对象之前检查 uuid 的有效性
        try:
            user = UserProfile.objects.get(uuid=uuid)
        except User.DoesNotExist:
            ret['error_code'] = '20001'
            ret['error'] = 'Invalid uuid'
            return JsonResponse(ret)

        # 在创建 Template 对象之前检查外键关联的 ID 的有效性
        try:
            input_device = Role.objects.get(id=input_device_id)
            output_device = Role.objects.get(id=output_device_id)
        except Role.DoesNotExist:
            ret['error_code'] = '30001'
            ret['error'] = 'Invalid input_device or output_device ID'
            return JsonResponse(ret)

        # 创建 Template 对象
        try:
            template = Template.objects.create(
                event_name=event_name,
                uuid=uuid,
                role_num=role_num,
                time_window=time_window,
                input_device=input_device,
                output_device=output_device,
                port=port,
                duration=duration,
                pwm=pwm
            )
            template.save()

            ret['error_code'] = '0'
            ret['error'] = 'Success'
            return JsonResponse(ret)

        except Exception as e:
            print(e)
            ret['error_code'] = '10008'
            ret['error'] = 'Param error, see doc for more info'
            return JsonResponse(ret)


class GetOdorList(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        odor_list = list(Odor.objects.values('id', 'odor').all().order_by('-id'))
        return JsonResponse({
            'status': True,
            'data': odor_list
        })


class SaveTemplateOdors(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *arg, **kwargs):
        tid = request.data['tid']
        odors = request.data['odors']

        TemplateOdorModel.objects.all().filter(event_template_id=tid).delete()

        for odor in odors:
            TemplateOdorModel.objects.create(
                event_template_id=str(tid),
                odor_id=str(odor['odor_id']),
                port=str(odor['port_id']),
                start=odor['start'],
                duration=odor['duration'],
                intensity=odor['intensity']
            ).save()

        return JsonResponse({
            'status': True
        })


class GetTemplateOdorsByTid(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        tid = request.query_params.get('tid')
        # {odor_id: string, port_id: string, duration: number, intensity: number, start: number}[]
        odors = TemplateOdorModel.objects\
            .filter(event_template_id=tid)\
            .values('odor_id', 'port', 'start', 'duration', 'intensity')
        odors = list(odors)
        return JsonResponse({
            'status': True,
            'data': odors
        })

