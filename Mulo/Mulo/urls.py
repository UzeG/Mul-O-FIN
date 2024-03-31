"""Mulo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from web.views import home, admin, user
from web.views.device import bind_device_role
from django.contrib.admin import site
from api.views import LoginView, RegView, LogoutView, EventView, DateView, ClearView, TemplateView
from api.views import GetOdorList, SaveTemplateOdors, GetTemplateOdorsByTid, SetTemplateParent, GetSubTemplatesByTid, \
    GetValidWhileParentByTid, SaveTemplateValidWhileParent

urlpatterns = [
    # 主界面
    path('', home.home_main),
    path('home/main/', home.home_main),
    path('home/login/', home.home_login),
    path('accounts/login/', home.home_login),
    path('home/logout/', home.home_logout),
    path('home/code/', home.home_code),
    path('home/register/', home.home_register),
    path('home/profile/', home.home_profile),
    path('home/modify_password/', home.home_modify_password),
    # 超级管理员界面
    path('admin/main/', admin.admin_main),
    path('admin/teaching/', admin.admin_teaching),
    path('admin/teaching/tcp/conn/', admin.admin_teaching_tcp_conn),
    path('admin/teaching/handle/client/request/', admin.admin_teaching_handle_client_request),
    path('admin/reality/', admin.admin_reality),
    path('admin/reality/role/', admin.admin_reality_role),
    path('admin/reality/role/<int:rid>/delete/', admin.admin_reality_role_delete),
    path('admin/reality/odor/', admin.admin_reality_odor),
    path('admin/reality/odor/<int:oid>/delete/', admin.admin_reality_odor_delete),
    path('admin/reality/add/', admin.admin_reality_add),
    path('admin/reality/detail/', admin.admin_reality_detail),
    path('admin/reality/edit/', admin.admin_reality_edit),
    path('admin/reality/<int:tid>/delete/', admin.admin_reality_delete),
    path('admin/device/', admin.admin_device),
    path('admin/virtual/reality/', admin.admin_virtual_reality),
    # 用户界面
    path('user/main/', user.user_main),
    # 后台界面
    path('manage/', site.urls),

    # 设备绑定
    path('devices/bind/', bind_device_role, name='bind_device_role'),

    # api
    re_path(r'^api/login/$', LoginView.as_view()),
    re_path(r'^api/login', LoginView.as_view()),
    re_path(r'^api/reg/$', RegView.as_view()),
    re_path(r'^api/reg', RegView.as_view()),
    re_path(r'^api/logout/$', LogoutView.as_view()),
    re_path(r'api/logout', LogoutView.as_view()),
    re_path(r'^api/event/$', EventView.as_view()),
    re_path(r'^api/event', EventView.as_view()),

    re_path(r'^api/date/$', DateView.as_view()),
    re_path(r'^api/date', DateView.as_view()),
    re_path(r'^api/clear/$', ClearView.as_view()),
    re_path(r'^api/clear', ClearView.as_view()),
    re_path(r'^api/template/$', TemplateView.as_view()),
    re_path(r'^api/template', TemplateView.as_view()),
    re_path(r'^api/get_odor_list', GetOdorList.as_view()),
    re_path(r'^api/save_template_odors/$', SaveTemplateOdors.as_view()),
    re_path(r'^api/get_template_odors_by_tid/$', GetTemplateOdorsByTid.as_view()),
    re_path(r'^api/set_template_parent/$', SetTemplateParent.as_view()),
    re_path(r'^api/get_sub_templates_by_tid/$', GetSubTemplatesByTid.as_view()),
    re_path(r'^api/get_valid_while_parent_by_tid/$', GetValidWhileParentByTid.as_view()),
    re_path(r'^api/save_template_valid_while_parent/$', SaveTemplateValidWhileParent.as_view())
]
