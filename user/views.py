from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .models import myUser
from .utils import send_email, generate_verification_token, verify_token


@require_http_methods(['POST'])
def email_login(request):
    """
    用户登录
    传入参数： email 邮箱地址
                password 密码
    :param request:
    :return:
    """
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')  # 登录成功后跳转的页面
    else:
        # 登录失败处理
        return render(request, 'login.html', {'error': 'Invalid credentials'})


@require_http_methods(['POST'])
def register(request):
    """
    用户注册
    :param request: email 邮箱地址
                    password 密码
                    token 验证码
    :return:
    """
    email = request.POST['email']
    password = request.POST['password']
    token = request.POST['token']

    if not verify_token(email, token, 'register'):
        myUser.objects.create_user(email=email, password=password)
        return redirect('/api/v1/login')  # 注册成功后跳转到登录页面
    else:
        return render(request, 'register.html', {'error': 'Invalid or expired token'})


@require_http_methods(['POST'])
def send_verification_email(request):
    """
    发送验证邮件
    :param request: email 邮箱地址
                    token_type string 验证码类型
    :return:
    """
    email = request.GET.get('email')
    token_type = request.GET.get('token_type')
    # 这里添加发送验证邮件的逻辑
    user_token = generate_verification_token(email, token_type)
    if send_email(user_token):
        return "success"
    else:
        return "failed"


@require_http_methods(['POST'])
def login_with_token(request):
    """
    使用验证码登录
    :param request: email 邮箱地址
                    token 验证码
    :return:
    """
    email = request.POST['email']
    token = request.POST['token']

    if verify_token(email, token, 'login_with_token'):
        try:
            user = myUser.objects.get(email=email)
            login(request, user)
            return redirect('home')  # 登录成功后跳转的页面
        except myUser.DoesNotExist:
            return render(request, 'login.html', {'error': 'User does not exist'})
    else:
        return render(request, 'login.html', {'error': 'Invalid or expired token'})
