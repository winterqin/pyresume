from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.email_login, name='login'),
    path('register/', views.register, name='register'),
    path('send_verification_email/', views.send_verification_email, name='send_verification_email'),
    path('login_with_token/', views.login_with_token, name='login_with_token'),
    path('token/refresh/', views.refresh_token, name='token_refresh'),  # ✅ 新增
    path('token/verify/', views.verify_jwt_token, name='token_verify'),  # ✅ 新增
    path('selfinfo/', views.me, name='self_info')
]
