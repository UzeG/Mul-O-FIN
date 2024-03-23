from django.db import models
import uuid
from django.contrib.auth.models import User
import socket


# Create your models here.
port_choices = (
        (1, 'Port 1'),
        (2, 'Port 2'),
        (3, 'Port 3'),
        (4, 'Port 4'),
)


class UserProfile(models.Model):
    """ 用户描述表 """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 添加自定义字段
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)  # 自动生成唯一的 UUID

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username  # 返回用户的用户名作为表示字符串


class RoleInfo(models.Model):
    """ 角色表 """
    id = models.BigAutoField(verbose_name='角色ID', primary_key=True)
    name = models.CharField(verbose_name='角色名', max_length=16)
    create_date = models.DateTimeField(verbose_name='创建时间')
    update_date = models.DateTimeField(verbose_name='更新时间')

    def __str__(self):
        return self.id


'''
class UserInfo(models.Model):
    """ 用户表 """
    id = models.BigAutoField(verbose_name='用户ID', primary_key=True)
    username = models.CharField(verbose_name='username', max_length=16)
    password = models.CharField(verbose_name='password', max_length=64)
    email = models.CharField(verbose_name='email', max_length=64)
    role = models.ForeignKey(verbose_name='角色ID', to='RoleInfo', to_field='id', on_delete=models.CASCADE, default=1)

    create_date = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    update_date = models.DateTimeField(verbose_name='更新时间', default=timezone.now)
    status_choices = (
        (0, '设备未连接'),
        (1, '设备已连接'),
    )
    
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choices, default=0)
'''


class Odor(models.Model):
    """ 气味表 """
    odor = models.CharField(verbose_name='odor', max_length=32)

    def __str__(self):
        return self.odor


class TemplateOdorModel(models.Model):
    event_template = models.ForeignKey(to='Template', on_delete=models.CASCADE, related_name='odors')
    odor = models.ForeignKey(to='Odor', on_delete=models.CASCADE)
    port = models.PositiveIntegerField(choices=port_choices, default=1)
    start = models.FloatField(default=0)
    duration = models.FloatField(default=3)
    intensity = models.FloatField(default=100)  # pwn?


# class OdorSelection(models.Model):
#     """ 气味选择表 """
#     odor_selection = models.ForeignKey(verbose_name='', to='Odor', related_name='FriendList_odor_selection',
#                                        on_delete=models.CASCADE)


class Role(models.Model):
    """ 事件角色 """
    role = models.CharField(verbose_name='role', max_length=32)

    def __str__(self):
        return self.role


class RoleSelection(models.Model):
    """ 角色选择表 """
    role_selection = models.ForeignKey(verbose_name='', to='Role', related_name='FriendList_role_selection',
                                       on_delete=models.CASCADE, default='')


class Template(models.Model):
    """ 事件范式 """
    event_name = models.CharField(verbose_name='event_name', max_length=32)
    # input_device = models.ForeignKey(verbose_name='', to='Role', related_name='FriendList_input_device',
    #                                  on_delete=models.CASCADE,
    #                                  default='')
    input_description = models.CharField(max_length=64, default='', null=True, blank=True)
    # role_num = models.SmallIntegerField(verbose_name='', default=1)
    threshold = models.SmallIntegerField(verbose_name='', default=1)  # role_num -> threshold
    time_window = models.SmallIntegerField(verbose_name='', default=10)
    output_device = models.ForeignKey(verbose_name='', to='Role', related_name='FriendList_output_device',
                                      on_delete=models.CASCADE,
                                      default='')

    # port = models.SmallIntegerField(verbose_name='', choices=port_choices, default=1)
    # duration = models.SmallIntegerField(verbose_name='', default=3)
    # pwm = models.IntegerField(verbose_name='', default=150)

    # parent event
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    # total output time
    total_time = models.PositiveIntegerField(default=10, null=False)
    # valid while parent
    valid_while_parent = models.BooleanField(default=None, blank=True, null=True)

    # 存储所属的uuid
    uuid = models.CharField(verbose_name='', max_length=36, default=None)


class Device(models.Model):
    """ 设备表 """
    ip = models.CharField(verbose_name='ip', max_length=32)
    port = models.IntegerField(verbose_name='port')
    character = models.CharField(verbose_name='character', max_length=32, null=True, blank=True)
    is_connected = models.BooleanField(verbose_name='is connected', default=False)

    def update_connection_status(self):
        try:
            # 创建一个套接字对象
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置连接超时时间为1秒钟
            s.settimeout(1)
            # 尝试连接设备
            s.connect((self.ip, self.port))
            # 连接成功，则设备已连接
            self.is_connected = True
        except (socket.timeout, ConnectionRefusedError):
            # 连接超时或连接被拒绝，则设备未连接
            self.is_connected = False
        finally:
            # 关闭套接字连接
            s.close()

        # 保存设备对象的更改
        self.save()
