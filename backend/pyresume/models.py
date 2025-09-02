from django.db import models
from user.models import myUser as MyUser


class Company(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    website_link = models.URLField(null=True, blank=True)
    login_type = models.CharField(max_length=100, null=True, blank=True)
    uname = models.CharField(max_length=100, null=True, blank=True)
    upass = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)

    # 如果你在创建记录时允许为空，去掉 null=True 的做法
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return self.company_name or "Company"


class Application(models.Model):
    id = models.BigAutoField(primary_key=True)
    position = models.TextField(null=True, blank=True)
    base = models.TextField(null=True, blank=True)
    salery = models.TextField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    resume = models.TextField(null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True, blank=True)

    # 如果你在创建记录时允许为空，去掉 null=True 的做法
    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"Application for {self.position} at {self.company.company_name if self.company else 'No Company'}"
