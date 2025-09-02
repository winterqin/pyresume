from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
from .models import Company, Application
from user.models import myUser


# 状态验证函数
def validate_status(status):
    """验证状态值是否有效"""
    valid_statuses = [
        '已投递',
        '简历筛选中',
        '测评/笔试中',
        '面试中',
        '已录用',
        '已结束'
    ]
    return status in valid_statuses


# Company 相关视图
@csrf_exempt
@require_http_methods(["GET"])
def company_list(request):
    """获取公司列表，支持搜索和分页"""
    try:
        # 获取查询参数
        search_term = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # 构建查询
        companies = Company.objects.all()

        # 搜索过滤
        if search_term:
            companies = companies.filter(
                Q(company_name__icontains=search_term) |
                Q(website_link__icontains=search_term)
            )

        # 排序
        companies = companies.order_by('company_name')

        # 分页
        paginator = Paginator(companies, page_size)
        companies_page = paginator.get_page(page)

        # 序列化数据
        companies_data = []
        for company in companies_page:
            companies_data.append({
                'id': company.id,
                'company_name': company.company_name,
                'website_link': company.website_link,
                'login_type': company.login_type,
                'uname': company.uname,
                'upass': company.upass,
                'created_at': company.created_at.isoformat() if company.created_at else None,
                'user': company.user.id if company.user else None
            })

        return JsonResponse({
            'success': True,
            'data': companies_data,
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def company_create(request):
    """创建新公司"""
    try:
        data = json.loads(request.body)

        # 检查用户认证状态，但允许匿名用户创建（用于测试）
        user = None
        if request.user.is_authenticated and isinstance(request.user, myUser):
            user = request.user

        # 创建公司
        company = Company.objects.create(
            company_name=data.get('company_name'),
            website_link=data.get('website_link'),
            login_type=data.get('login_type'),
            uname=data.get('uname'),
            upass=data.get('upass'),
            user=user  # 可以是None（匿名用户）或认证用户
        )

        return JsonResponse({
            'success': True,
            'data': {
                'id': company.id,
                'company_name': company.company_name,
                'website_link': company.website_link,
                'login_type': company.login_type,
                'uname': company.uname,
                'upass': company.upass,
                'created_at': company.created_at.isoformat() if company.created_at else None
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def company_update(request, company_id):
    """更新公司信息"""
    try:
        data = json.loads(request.body)
        # 检查用户认证状态，但允许匿名用户创建（用于测试）
        user = None
        if request.user.is_authenticated and isinstance(request.user, myUser):
            user = request.user
        # # 检查用户认证状态
        # if not request.user.is_authenticated:
        #     return JsonResponse({
        #         'success': False,
        #         'error': '用户未认证，请先登录'
        #     }, status=401)

        company = Company.objects.get(id=company_id)

        # 检查权限（只有创建者或管理员可以编辑）
        if company.user and company.user != request.user:
            return JsonResponse({
                'success': False,
                'error': '没有权限编辑此公司信息'
            }, status=403)

        # 更新字段
        if 'company_name' in data:
            company.company_name = data['company_name']
        if 'website_link' in data:
            company.website_link = data['website_link']
        if 'login_type' in data:
            company.login_type = data['login_type']
        if 'uname' in data:
            company.uname = data['uname']
        if 'upass' in data:
            company.upass = data['upass']

        company.save()

        return JsonResponse({
            'success': True,
            'data': {
                'id': company.id,
                'company_name': company.company_name,
                'website_link': company.website_link,
                'login_type': company.login_type,
                'uname': company.uname,
                'upass': company.upass,
                'created_at': company.created_at.isoformat() if company.created_at else None
            }
        })

    except Company.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '公司不存在'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def company_delete(request, company_id):
    """删除公司"""
    try:
        # 检查用户认证状态，但允许匿名用户创建（用于测试）
        user = None
        if request.user.is_authenticated and isinstance(request.user, myUser):
            user = request.user
        # # 检查用户认证状态
        # if not request.user.is_authenticated:
        #     return JsonResponse({
        #         'success': False,
        #         'error': '用户未认证，请先登录'
        #     }, status=401)

        company = Company.objects.get(id=company_id)

        # 检查权限（只有创建者或管理员可以删除）
        if company.user and company.user != request.user:
            return JsonResponse({
                'success': False,
                'error': '没有权限删除此公司信息'
            }, status=403)

        company.delete()

        return JsonResponse({
            'success': True,
            'message': '公司删除成功'
        })

    except Company.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '公司不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# Application 相关视图
@csrf_exempt
@require_http_methods(["GET"])
def application_list(request):
    """获取求职记录列表，支持搜索和分页"""
    try:
        # 获取查询参数
        search_term = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # 构建查询
        applications = Application.objects.select_related('company').all()

        # 搜索过滤
        if search_term:
            applications = applications.filter(
                Q(position__icontains=search_term) |
                Q(base__icontains=search_term) |
                Q(company__company_name__icontains=search_term)  # 新增公司名称搜索
            )
        # 排序
        applications = applications.order_by('-created_at')

        # 分页
        paginator = Paginator(applications, page_size)
        applications_page = paginator.get_page(page)

        # 序列化数据
        applications_data = []
        for application in applications_page:
            applications_data.append({
                'id': application.id,
                'position': application.position,
                'base': application.base,
                'salery': application.salery,
                'status': application.status,
                'resume': application.resume,
                'update_at': application.update_at.isoformat() if application.update_at else None,
                'created_at': application.created_at.isoformat() if application.created_at else None,
                'company': {
                    'id': application.company.id,
                    'company_name': application.company.company_name
                } if application.company else None,
                'user': application.user.id if application.user else None
            })

        return JsonResponse({
            'success': True,
            'data': applications_data,
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def application_create(request):
    """创建新求职记录"""
    try:
        data = json.loads(request.body)

        # 验证状态值
        if 'status' in data and not validate_status(data['status']):
            return JsonResponse({
                'success': False,
                'error': f'无效的状态值: {data["status"]}。有效状态包括: 已投递, 简历筛选中, 测评/笔试中, 面试中, 已录用, 已结束'
            }, status=400)

        # 检查用户认证状态，但允许匿名用户创建（用于测试）
        user = None
        if request.user.is_authenticated and isinstance(request.user, myUser):
            user = request.user

        # 创建求职记录
        application = Application.objects.create(
            position=data.get('position'),
            base=data.get('base'),
            salery=data.get('salery'),
            status=data.get('status', '已投递'),  # 默认状态为已投递
            resume=data.get('resume'),
            company_id=data.get('company') if data.get('company') else None,
            user=user  # 可以是None（匿名用户）或认证用户
        )

        return JsonResponse({
            'success': True,
            'data': {
                'id': application.id,
                'position': application.position,
                'base': application.base,
                'salery': application.salery,
                'status': application.status,
                'resume': application.resume,
                'company': application.company.id if application.company else None,
                'created_at': application.created_at.isoformat() if application.created_at else None
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def application_update(request, application_id):
    """更新求职记录"""
    try:
        data = json.loads(request.body)
        # 检查用户认证状态，但允许匿名用户创建（用于测试）
        user = None
        if request.user.is_authenticated and isinstance(request.user, myUser):
            user = request.user
        # # 检查用户认证状态
        # if not request.user.is_authenticated:
        #     return JsonResponse({
        #         'success': False,
        #         'error': '用户未认证，请先登录'
        #     }, status=401)

        application = Application.objects.get(id=application_id)

        # 检查权限（只有创建者或管理员可以编辑）
        if application.user and application.user != request.user:
            return JsonResponse({
                'success': False,
                'error': '没有权限编辑此求职记录'
            }, status=403)

        # 更新字段
        if 'position' in data:
            application.position = data['position']
        if 'base' in data:
            application.base = data['base']
        if 'salery' in data:
            application.salery = data['salery']
        if 'status' in data:
            # 验证状态值
            if not validate_status(data['status']):
                return JsonResponse({
                    'success': False,
                    'error': f'无效的状态值: {data["status"]}。有效状态包括: 已投递, 简历筛选中, 测评/笔试中, 面试中, 已录用, 已结束'
                }, status=400)
            application.status = data['status']
        if 'resume' in data:
            application.resume = data['resume']
        if 'company' in data:
            application.company_id = data['company'] if data['company'] else None

        application.save()

        return JsonResponse({
            'success': True,
            'data': {
                'id': application.id,
                'position': application.position,
                'base': application.base,
                'salery': application.salery,
                'status': application.status,
                'resume': application.resume,
                'company': application.company.id if application.company else None,
                'update_at': application.update_at.isoformat() if application.update_at else None
            }
        })

    except Application.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '求职记录不存在'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': '无效的JSON数据'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def application_delete(request, application_id):
    """删除求职记录"""
    try:
        # 检查用户认证状态，但允许匿名用户创建（用于测试）
        user = None
        if request.user.is_authenticated and isinstance(request.user, myUser):
            user = request.user
        # 检查用户认证状态
        # if not request.user.is_authenticated:
        #     return JsonResponse({
        #         'success': False,
        #         'error': '用户未认证，请先登录'
        #     }, status=401)

        application = Application.objects.get(id=application_id)

        # 检查权限（只有创建者或管理员可以删除）
        if application.user and application.user != request.user:
            return JsonResponse({
                'success': False,
                'error': '没有权限删除此求职记录'
            }, status=403)

        application.delete()

        return JsonResponse({
            'success': True,
            'message': '求职记录删除成功'
        })

    except Application.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '求职记录不存在'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# 获取公司列表（用于选择）
@csrf_exempt
@require_http_methods(["GET"])
def company_options(request):
    """获取公司选项列表，用于下拉选择"""
    try:
        companies = Company.objects.values('id', 'company_name').order_by('company_name')

        return JsonResponse({
            'success': True,
            'data': list(companies)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# @csrf_exempt
# @require_http_methods(["GET"])
# def dashboard_status():
#     """
#     获取各个统计指标
#     :return:
#     """
#     try:
#         application = Application.objects.all()
#         all_application_count = application.count()
#         status1_count = application.filter(status='已投递').count()
#         status2_count = application.filter(status='简历筛选中').count()
#         status3_count = application.filter(status='测评/笔试中').count()
#         status4_count = application.filter(status='面试中').count()
#         status5_count = application.filter(status='已录用').count()
#         status6_count = application.filter(status='已结束').count()
#         top_5_applications = application.order_by('-created_at')[:5]
#
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'error': str(e)
#         }, status=500)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Application


@csrf_exempt
@require_http_methods(["GET"])
def dashboard_status(request):
    """
    获取招聘流程的统计指标和漏斗数据
    :return: JSON格式的统计数据
    """
    try:
        # 获取所有申请记录
        applications = Application.objects.all()

        # 状态统计
        status_counts = {
            "已投递": applications.filter(status='已投递').count(),
            "简历筛选中": applications.filter(status='简历筛选中').count(),
            "测评/笔试中": applications.filter(status='测评/笔试中').count(),
            "面试中": applications.filter(status='面试中').count(),
            "已录用": applications.filter(status='已录用').count(),
            "已结束": applications.filter(status='已结束').count()
        }

        # 漏斗统计
        total_applications = applications.count()
        passed_screening = applications.filter(
            status__in=["测评/笔试中", "面试中", "已录用"]
        ).count()
        passed_assessment = applications.filter(
            status__in=["面试中", "已录用"]
        ).count()
        passed_interview = applications.filter(
            status="已录用"
        ).count()
        hired = passed_interview  # 已录用人数

        # 最近5条申请记录
        recent_applications = applications.order_by('-created_at')[:5]
        recent_applications_data = [
            {
                "id": app.id,
                "job_title": app.position if app.position else "",
                "company": app.company.company_name if app.company.company_name else "",
                "status": app.status,
                "created_at": app.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for app in recent_applications
        ]

        return JsonResponse({
            "success": True,
            "data": {
                "status_counts": status_counts,
                "funnel_stats": {
                    "total_applications": total_applications,
                    "passed_screening": passed_screening,
                    "passed_assessment": passed_assessment,
                    "passed_interview": passed_interview,
                    "hired": hired
                },
                "recent_applications": recent_applications_data,
                "conversion_rates": {
                    "screening_rate": round(passed_screening / total_applications * 100,
                                            2) if total_applications else 0,
                    "assessment_rate": round(passed_assessment / passed_screening * 100, 2) if passed_screening else 0,
                    "interview_rate": round(passed_interview / passed_assessment * 100, 2) if passed_assessment else 0,
                    "hire_rate": round(hired / total_applications * 100, 2) if total_applications else 0
                }
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
