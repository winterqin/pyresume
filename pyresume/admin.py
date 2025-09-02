from django.contrib import admin
from .models import Company, Application


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'website_link', 'login_type', 'created_at', 'user')
    list_filter = ('login_type', 'created_at')
    search_fields = ('company_name', 'website_link')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('company_name', 'website_link', 'login_type')
        }),
        ('登录信息', {
            'fields': ('uname', 'upass')
        }),
        ('系统信息', {
            'fields': ('id', 'user', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'base', 'salery', 'status', 'company', 'created_at', 'user')
    list_filter = ('status', 'created_at', 'company')
    search_fields = ('position', 'base', 'resume')
    readonly_fields = ('id', 'created_at', 'update_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('求职信息', {
            'fields': ('position', 'base', 'salery', 'status', 'resume')
        }),
        ('关联信息', {
            'fields': ('company', 'user')
        }),
        ('系统信息', {
            'fields': ('id', 'created_at', 'update_at'),
            'classes': ('collapse',)
        }),
    )
