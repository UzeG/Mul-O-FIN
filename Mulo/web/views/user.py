from django.shortcuts import render


def user_main(request):
    """ 普通用户主页面 """
    return render(request, 'user_main.html')

