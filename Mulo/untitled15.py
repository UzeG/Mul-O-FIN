# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:21:29 2023

@author: xiaol
"""
import uuid
from django.contrib.auth.models import User

# 生成一个新的UUID
new_uuid = uuid.uuid4()

# 创建新用户，并将UUID存储在profile字段中
new_user = User.objects.create_user(username='new_username', password='new_password')
new_user.profile.uuid = new_uuid
new_user.profile.save()
