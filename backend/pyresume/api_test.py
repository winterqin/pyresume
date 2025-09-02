"""
API 接口测试文件
包含所有接口的测试示例和说明
"""

# 基础URL配置
BASE_URL = "http://localhost:8000"  # Django后端地址

# Company 相关接口测试
COMPANY_API = {
    # 获取公司列表（支持搜索和分页）
    "list": {
        "method": "GET",
        "url": f"{BASE_URL}/api/companies/",
        "params": {
            "search": "公司名称关键词",  # 可选，搜索公司名称或网站
            "page": 1,                  # 可选，页码，默认1
            "page_size": 10             # 可选，每页数量，默认10
        },
        "description": "获取公司列表，支持搜索和分页"
    },
    
    # 创建新公司
    "create": {
        "method": "POST",
        "url": f"{BASE_URL}/api/companies/create/",
        "data": {
            "company_name": "示例公司",
            "website_link": "https://example.com",
            "login_type": "邮箱",
            "uname": "user@example.com",
            "upass": "password123"
        },
        "description": "创建新公司信息"
    },
    
    # 更新公司信息
    "update": {
        "method": "PUT",
        "url": f"{BASE_URL}/api/companies/1/update/",  # 1是公司ID
        "data": {
            "company_name": "更新后的公司名称",
            "website_link": "https://updated-example.com"
        },
        "description": "更新指定公司的信息"
    },
    
    # 删除公司
    "delete": {
        "method": "DELETE",
        "url": f"{BASE_URL}/api/companies/1/delete/",  # 1是公司ID
        "description": "删除指定公司"
    },
    
    # 获取公司选项（用于下拉选择）
    "options": {
        "method": "GET",
        "url": f"{BASE_URL}/api/companies/options/",
        "description": "获取公司选项列表，用于下拉选择"
    }
}

# Application 相关接口测试
APPLICATION_API = {
    # 获取求职记录列表（支持搜索和分页）
    "list": {
        "method": "GET",
        "url": f"{BASE_URL}/api/applications/",
        "params": {
            "search": "职位关键词",      # 可选，搜索职位或地点
            "page": 1,                  # 可选，页码，默认1
            "page_size": 10             # 可选，每页数量，默认10
        },
        "description": "获取求职记录列表，支持搜索和分页"
    },
    
    # 创建新求职记录
    "create": {
        "method": "POST",
        "url": f"{BASE_URL}/api/applications/create/",
        "data": {
            "position": "软件工程师",
            "base": "北京",
            "salery": "15k-25k",
            "status": "已投递",
            "resume": "简历链接或描述",
            "company": 1                # 可选，关联的公司ID
        },
        "description": "创建新求职记录"
    },
    
    # 更新求职记录
    "update": {
        "method": "PUT",
        "url": f"{BASE_URL}/api/applications/1/update/",  # 1是求职记录ID
        "data": {
            "position": "高级软件工程师",
            "status": "面试中"
        },
        "description": "更新指定求职记录"
    },
    
    # 删除求职记录
    "delete": {
        "method": "DELETE",
        "url": f"{BASE_URL}/api/applications/1/delete/",  # 1是求职记录ID
        "description": "删除指定求职记录"
    }
}

# 使用示例
if __name__ == "__main__":
    print("=== Company API 接口 ===")
    for name, api in COMPANY_API.items():
        print(f"\n{name.upper()}:")
        print(f"  方法: {api['method']}")
        print(f"  URL: {api['url']}")
        print(f"  描述: {api['description']}")
        if 'params' in api:
            print(f"  参数: {api['params']}")
        if 'data' in api:
            print(f"  数据: {api['data']}")
    
    print("\n=== Application API 接口 ===")
    for name, api in APPLICATION_API.items():
        print(f"\n{name.upper()}:")
        print(f"  方法: {api['method']}")
        print(f"  URL: {api['url']}")
        print(f"  描述: {api['description']}")
        if 'params' in api:
            print(f"  参数: {api['params']}")
        if 'data' in api:
            print(f"  数据: {api['data']}")
    
    print("\n=== 测试命令示例 ===")
    print("\n# 获取公司列表")
    print(f"curl -X GET '{BASE_URL}/api/companies/?page=1&page_size=10'")
    
    print("\n# 创建公司")
    print(f"curl -X POST '{BASE_URL}/api/companies/create/' \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"company_name\":\"测试公司\",\"website_link\":\"https://test.com\"}'")
    
    print("\n# 获取求职记录")
    print(f"curl -X GET '{BASE_URL}/api/applications/?search=软件工程师&page=1'")
    
    print("\n# 创建求职记录")
    print(f"curl -X POST '{BASE_URL}/api/applications/create/' \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '{\"position\":\"软件工程师\",\"base\":\"北京\",\"status\":\"已投递\"}'") 