from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import json
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken  # ✅ 加上 AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import myUser
from .utils import send_email, generate_verification_token, verify_token


def get_tokens_for_user(user):
    """
    为用户生成JWT token
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@csrf_exempt
@require_http_methods(['POST'])
def email_login(request):
    """
    用户登录
    传入参数： email 邮箱地址
                password 密码
    :param request:
    :return:
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': '邮箱和密码不能为空'}, status=400)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # 生成JWT token
            tokens = get_tokens_for_user(user)
            return JsonResponse({
                'message': '登录成功',
                'user': {'email': user.email},
                'tokens': tokens
            })
        else:
            return JsonResponse({'error': '邮箱或密码错误'}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    """
    用户注册
    :param request: email 邮箱地址
                    password 密码
                    token 验证码
    :return:
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        token = data.get('token')

        if not email or not password or not token:
            return JsonResponse({'error': '邮箱、密码和验证码不能为空'}, status=400)

        if not verify_token(email, token, 'register'):
            # 验证码验证失败
            return JsonResponse({'error': '验证码无效或已过期'}, status=400)

        # 检查用户是否已存在
        if myUser.objects.filter(email=email).exists():
            return JsonResponse({'error': '该邮箱已被注册'}, status=400)

        user = myUser.objects.create_user(email=email, password=password)
        # 注册成功后自动登录并生成JWT token
        login(request, user)
        tokens = get_tokens_for_user(user)
        return JsonResponse({
            'message': '注册成功',
            'user': {'email': user.email},
            'tokens': tokens
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def send_verification_email(request):
    """
    发送验证邮件
    :param request: email 邮箱地址
                    token_type string 验证码类型
    :return:
    """
    try:
        if request.method == 'GET':
            email = request.GET.get('email')
            token_type = request.GET.get('token_type')
        else:
            data = json.loads(request.body)
            email = data.get('email')
            token_type = data.get('token_type')

        if not email or not token_type:
            return JsonResponse({'error': '邮箱和验证码类型不能为空'}, status=400)

        # 这里添加发送验证邮件的逻辑
        user_token = generate_verification_token(email, token_type)
        if send_email(user_token):
            return JsonResponse({'message': '验证码发送成功'})
        else:
            return JsonResponse({'error': '验证码发送失败'}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def login_with_token(request):
    """
    使用验证码登录
    :param request: email 邮箱地址
                    token 验证码
    :return:
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        token = data.get('token')

        if not email or not token:
            return JsonResponse({'error': '邮箱和验证码不能为空'}, status=400)

        if not verify_token(email, token, 'login_with_token'):
            return JsonResponse({'error': '验证码无效或已过期'}, status=400)

        try:
            user = myUser.objects.get(email=email)
            login(request, user)
            # 生成JWT token
            tokens = get_tokens_for_user(user)
            return JsonResponse({
                'message': '登录成功',
                'user': {'email': user.email},
                'tokens': tokens
            })
        except myUser.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def refresh_token(request):
    """
    刷新JWT token
    :param request: refresh token
    :return: 新的access token
    """
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh')

        if not refresh_token:
            return JsonResponse({'error': 'refresh token不能为空'}, status=400)

        try:
            # 验证refresh token并生成新的access token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return JsonResponse({
                'access': access_token,
                'message': 'token刷新成功'
            })
        except (InvalidToken, TokenError) as e:
            return JsonResponse({'error': '无效的refresh token'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


@csrf_exempt
@require_http_methods(['POST'])
def verify_jwt_token(request):
    """
    验证JWT access token
    请求体：{"access": "<access_token>"}
    """
    try:
        data = json.loads(request.body)
        access_token = data.get('access')
        if not access_token:
            return JsonResponse({'error': 'access token不能为空'}, status=400)

        try:
            token = AccessToken(access_token)  # ✅ 使用 AccessToken
            user_id = token.get('user_id')  # SimpleJWT 默认存 user_id
            user = myUser.objects.get(id=user_id)  # ✅ 用 id（主键）查询
            return JsonResponse({
                'valid': True,
                'user': {'email': user.email},
                'message': 'token有效'
            })
        except (InvalidToken, TokenError):
            return JsonResponse({'valid': False, 'error': '无效的token'}, status=401)
        except myUser.DoesNotExist:
            return JsonResponse({'valid': False, 'error': '用户不存在'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return JsonResponse({'email': request.user.email})
