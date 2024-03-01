from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from io import BytesIO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from web.models import UserProfile

from web.utils.code import validate_code, validate_email
from web.utils.form import LoginForm, RegisterModelForm, ChangeProfileForm, ChangePasswordForm

from django.contrib import messages


def home_main(request):
    """ 主页面 """
    return render(request, 'home_main.html')


def home_login(request):
    """ 登录 """
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'home_login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('home_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error('code', 'Captcha error.')
            return render(request, 'home_login.html', {'form': form})
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        # 用户名与密码错误
        if user is None:
            form.add_error('password', 'Username or password error.')
            return render(request, 'home_login.html', {'form': form})

        else:
            # 检查用户是否有关联的 UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            if created:
                # 如果创建了新的 UserProfile，可以在这里进行一些初始化设置
                pass

            print(username, user_profile.uuid)
            login(request, user)
            next_url = request.GET.get('next')  # 获取next参数
            if next_url:
                return redirect(next_url)
            return redirect('/admin/main/')
    return render(request, 'home_login.html', {'form': form})


def home_code(request):
    """ 生成图片验证码 """
    # 调用pillow函数，生成图片
    img, code_string = validate_code()
    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['home_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    stream.getvalue()
    return HttpResponse(stream.getvalue())


def home_register(request):
    """ 注册 """
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'home_register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")

        # 文本不合法
        if not (isinstance(username, str) and isinstance(password, str) and isinstance(email, str)):
            if not isinstance(username, str):
                form.add_error('username', 'Username error.')
            if not isinstance(password, str):
                form.add_error('password', 'Password error.')
            if not isinstance(email, str):
                form.add_error('email', 'email error.')
            return render(request, 'home_register.html', {'form': form})

        # 邮箱格式错误
        if not validate_email(email):
            form.add_error('email', 'email format error.')
            return render(request, 'home_register.html', {'form': form})

        # 用户名已存在
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'username is exist.')
            return render(request, 'home_register.html', {'form': form})

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('/home/login/')

        except Exception as e:
            print(e)
            form.add_error('email', 'Unknown error')
            return render(request, 'home_register.html', {'form': form})

    return render(request, 'home_register.html', {'form': form})


@login_required  # 使用这个装饰器确保只有已登录的用户才能访问该视图
def home_profile(request):
    """ 用户简介 """
    user = request.user  # 获取当前登录用户

    user_profile = UserProfile.objects.get(user=request.user)  # 获取当前登录用户的 UserProfile

    if request.method == 'POST':
        form = ChangeProfileForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")

            # 文本不合法
            if not isinstance(email, str):
                form.add_error('email', 'email error.')
                return render(request, 'home_profile.html', {'form': form, 'user_profile': user_profile})

            # 邮箱格式错误
            if not validate_email(email):
                form.add_error('email', 'email format error.')
                return render(request, 'home_profile.html', {'form': form, 'user_profile': user_profile})

            # 更新用户的邮箱地址
            user.email = email
            user.save()

            return redirect('/home/main/')  # 重定向到用户简介页面
    else:
        # 通过现有的邮箱填充表单
        form = ChangeProfileForm(initial={'email': user.email})

    return render(request, 'home_profile.html', {'form': form, 'user_profile': user_profile})


def home_modify_password(request):
    """ 修改密码 """
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            user = authenticate(request, username=request.user.username,
                                password=form.cleaned_data.get("current_password"))

            if user is not None:
                try:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password updated successfully.')
                    logout(request)
                    request.session.clear()
                    return redirect('/home/login/')

                except Exception as e:
                    print(e)
                    messages.error(request, 'An error occurred while updating password.')
            else:
                messages.error(request, 'Current password is incorrect.')
    else:
        form = ChangePasswordForm()

    return render(request, 'home_modify_password.html', {'form': form})


def home_logout(request):
    """ 注销 """
    try:
        logout(request)
    except Exception as e:
        print(e)

    request.session.clear()
    return redirect('/home/main/')
