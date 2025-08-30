from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.email_login, name='login'),
    path('register/', views.register, name='register'),
    path('send_verification_email/', views.send_verification_email, name='send_verification_email'),
    path('login_with_token/', views.login_with_token, name='login_with_token')
]
