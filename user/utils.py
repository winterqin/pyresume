from user.models import UserToken
from django.utils import timezone
from datetime import timedelta
import random

import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_email(token: UserToken):
    """
    发送邮件，带有错误处理和日志记录
    Args:
        token: 要发送的验证码/令牌
    Returns:
        bool: 邮件是否成功发送
    """
    subject = f'Your {token.token_type} code'
    message = f'Your code is {token.token}, valid for 10 minutes.'  # ✅ 修正
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
    recipient_list = [token.email]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False  # 设为False让异常能够被捕获
        )
        logger.info(f"Email sent successfully to {token.email}, type: {token.token_type}")
        return True
    except Exception as e:
        logger.error(
            f"Failed to send email to {token.email}, type: {token.token_type}. Error: {str(e)}",
            exc_info=True
        )
        return False


def generate_verification_token(email, token_type='email_verification'):
    """
    生成并保存一个验证码
    :param email:
    :param token_type:
    :return:
    """
    # 生成一个随机验证码
    token = str(random.randint(100000, 999999))
    expires_at = timezone.now() + timedelta(minutes=10)  # 10分钟过期

    # 保存到数据库
    user_token = UserToken.objects.create(
        email=email,
        token=token,
        token_type=token_type,
        expires_at=expires_at
    )
    return user_token


def verify_token(email, token, token_type='email_verification'):
    try:
        user_token = UserToken.objects.get(email=email, token=token, token_type=token_type)
        if user_token.is_expired():
            return False
        return True
    except UserToken.DoesNotExist:
        return False
