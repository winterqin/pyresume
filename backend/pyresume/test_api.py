#!/usr/bin/env python3
"""
简单的API测试脚本
用于测试Django后端API是否正常工作
"""

import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def test_company_api():
    """测试公司相关API"""
    print("=== 测试公司API ===")
    
    # 1. 测试创建公司
    print("\n1. 测试创建公司...")
    company_data = {
        "company_name": "测试公司",
        "website_link": "https://test-company.com",
        "login_type": "邮箱",
        "uname": "test@company.com",
        "upass": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/companies/create/",
            json=company_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 创建公司成功:", result['data']['company_name'])
                company_id = result['data']['id']
            else:
                print("❌ 创建公司失败:", result.get('error'))
                return
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(response.text)
            return
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return
    
    # 2. 测试获取公司列表
    print("\n2. 测试获取公司列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/companies/")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ 获取公司列表成功，共 {len(result['data'])} 家公司")
            else:
                print("❌ 获取公司列表失败:", result.get('error'))
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    # 3. 测试获取公司选项
    print("\n3. 测试获取公司选项...")
    try:
        response = requests.get(f"{BASE_URL}/api/companies/options/")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ 获取公司选项成功，共 {len(result['data'])} 个选项")
            else:
                print("❌ 获取公司选项失败:", result.get('error'))
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_application_api():
    """测试求职记录相关API"""
    print("\n=== 测试求职记录API ===")
    
    # 1. 测试创建求职记录
    print("\n1. 测试创建求职记录...")
    application_data = {
        "position": "软件工程师",
        "base": "北京",
        "salery": "15k-25k",
        "status": "已投递",
        "resume": "测试简历",
        "company": None  # 暂时不关联公司
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/applications/create/",
            json=application_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 创建求职记录成功:", result['data']['position'])
                application_id = result['data']['id']
            else:
                print("❌ 创建求职记录失败:", result.get('error'))
                return
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(response.text)
            return
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return
    
    # 2. 测试获取求职记录列表
    print("\n2. 测试获取求职记录列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/applications/")
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ 获取求职记录列表成功，共 {len(result['data'])} 条记录")
            else:
                print("❌ 获取求职记录列表失败:", result.get('error'))
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def main():
    """主函数"""
    print("开始测试Django后端API...")
    print(f"测试地址: {BASE_URL}")
    
    try:
        # 测试公司API
        test_company_api()
        
        # 测试求职记录API
        test_application_api()
        
        print("\n=== 测试完成 ===")
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")

if __name__ == "__main__":
    main() 