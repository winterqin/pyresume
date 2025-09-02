#!/usr/bin/env python3
"""
用户认证状态测试脚本
演示匿名用户和认证用户的区别
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')
django.setup()

from django.contrib.auth.models import AnonymousUser
from user.models import myUser

def test_user_types():
    """测试不同类型的用户"""
    print("=== 用户类型测试 ===\n")
    
    # 1. 创建匿名用户对象
    anon_user = AnonymousUser()
    print("1. 匿名用户 (AnonymousUser):")
    print(f"   类型: {type(anon_user)}")
    print(f"   是否认证: {anon_user.is_authenticated}")
    print(f"   ID: {anon_user.id}")
    print(f"   用户名: {anon_user.username}")
    print(f"   邮箱: {anon_user.email}")
    print()
    
    # 2. 检查是否存在测试用户
    try:
        test_user = myUser.objects.get(username='testuser')
        print("2. 测试用户 (myUser):")
        print(f"   类型: {type(test_user)}")
        print(f"   是否认证: {test_user.is_authenticated}")
        print(f"   ID: {test_user.id}")
        print(f"   用户名: {test_user.username}")
        print(f"   邮箱: {test_user.email}")
        print()
    except myUser.DoesNotExist:
        print("2. 测试用户不存在，创建中...")
        test_user = myUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"   创建成功: {test_user.username} (ID: {test_user.id})")
        print()
    
    # 3. 演示认证检查
    print("3. 认证状态检查:")
    users_to_test = [anon_user, test_user]
    
    for i, user in enumerate(users_to_test, 1):
        print(f"   用户 {i}:")
        print(f"     类型: {type(user)}")
        print(f"     是否认证: {user.is_authenticated}")
        print(f"     是否为myUser: {isinstance(user, myUser)}")
        print(f"     是否为AnonymousUser: {isinstance(user, AnonymousUser)}")
        print(f"     ID: {user.id}")
        print()
    
    # 4. 演示在视图中的使用
    print("4. 在视图中的使用示例:")
    print("   # 检查用户认证状态")
    print("   if request.user.is_authenticated:")
    print("       print('用户已登录')")
    print("   else:")
    print("       print('用户是匿名用户')")
    print()
    
    print("   # 检查用户类型")
    print("   if isinstance(request.user, myUser):")
    print("       print('用户是myUser实例')")
    print("   elif isinstance(request.user, AnonymousUser):")
    print("       print('用户是匿名用户')")
    print()
    
    print("   # 安全地获取用户ID")
    print("   user_id = getattr(request.user, 'id', None)")
    print("   if user_id:")
    print("       print(f'用户ID: {user_id}')")
    print("   else:")
    print("       print('用户没有ID（匿名用户）')")

def create_test_user():
    """创建测试用户"""
    print("=== 创建测试用户 ===\n")
    
    try:
        # 检查是否已存在
        existing_user = myUser.objects.get(username='testuser')
        print(f"测试用户已存在: {existing_user.username} (ID: {existing_user.id})")
        return existing_user
    except myUser.DoesNotExist:
        pass
    
    try:
        # 创建新用户
        user = myUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        print(f"✅ 测试用户创建成功!")
        print(f"   用户名: {user.username}")
        print(f"   邮箱: {user.email}")
        print(f"   ID: {user.id}")
        print(f"   是否认证: {user.is_authenticated}")
        return user
    except Exception as e:
        print(f"❌ 创建用户失败: {e}")
        return None

def test_model_relationships():
    """测试模型关系"""
    print("=== 模型关系测试 ===\n")
    
    try:
        from .models import Company, Application
        
        # 测试创建公司（不关联用户）
        company = Company.objects.create(
            company_name="测试公司（无用户）",
            website_link="https://test-no-user.com"
        )
        print(f"✅ 创建公司成功（无用户）: {company.company_name}")
        print(f"   用户字段: {company.user}")
        print(f"   用户类型: {type(company.user)}")
        
        # 测试创建公司（关联用户）
        test_user = myUser.objects.get(username='testuser')
        company_with_user = Company.objects.create(
            company_name="测试公司（有用户）",
            website_link="https://test-with-user.com",
            user=test_user
        )
        print(f"✅ 创建公司成功（有用户）: {company_with_user.company_name}")
        print(f"   用户字段: {company_with_user.user}")
        print(f"   用户类型: {type(company_with_user.user)}")
        print(f"   用户名: {company_with_user.user.username}")
        
        # 清理测试数据
        company.delete()
        company_with_user.delete()
        print("\n🧹 测试数据已清理")
        
    except Exception as e:
        print(f"❌ 模型关系测试失败: {e}")

if __name__ == "__main__":
    print("开始用户认证状态测试...\n")
    
    # 创建测试用户
    test_user = create_test_user()
    
    if test_user:
        # 测试用户类型
        test_user_types()
        
        # 测试模型关系
        test_model_relationships()
    
    print("\n=== 测试完成 ===") 