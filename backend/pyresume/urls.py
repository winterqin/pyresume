from django.urls import path
from . import views

urlpatterns = [
    # Company 相关接口
    path('companies/', views.company_list, name='company_list'),  # GET: 获取公司列表
    path('companies/create/', views.company_create, name='company_create'),  # POST: 创建公司
    path('companies/<int:company_id>/update/', views.company_update, name='company_update'),  # PUT: 更新公司
    path('companies/<int:company_id>/delete/', views.company_delete, name='company_delete'),  # DELETE: 删除公司
    path('companies/options/', views.company_options, name='company_options'),  # GET: 获取公司选项
    
    # Application 相关接口
    path('applications/', views.application_list, name='application_list'),  # GET: 获取求职记录列表
    path('applications/create/', views.application_create, name='application_create'),  # POST: 创建求职记录
    path('applications/<int:application_id>/update/', views.application_update, name='application_update'),  # PUT: 更新求职记录
    path('applications/<int:application_id>/delete/', views.application_delete, name='application_delete'),  # DELETE: 删除求职记录

    # 统计接口
    path('dashboard/stats/', views.dashboard_status, name='company_count')
]
