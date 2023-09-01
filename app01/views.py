import random

from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime
from app01 import models
from app01.utils.form import UserModelForm, NumberModelForm, AdminPwdResetModelForm, \
    NumberEditModelForm, AdminModelForm, AdminEditModelForm, LoginForm, OrderModelForm


def depart_list(request, page=1):
    queryset = models.Department.objects.all()

    # 分页
    paginator = Paginator(queryset, per_page=5)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1)
    queryset = paginator.page(page).object_list

    if request.method == "POST":
        if 'add_depart' in request.POST:
            title = request.POST.get("title")
            models.Department.objects.create(title=title)
            # 添加部门则跳转到最后一页
            return redirect("/depart/list/" + str(paginator.num_pages))
        elif 'edit_depart' in request.POST:
            editing_id = request.POST.get("depart_id_editing")
            new_depart_title = request.POST.get("new_depart_title")
            models.Department.objects.filter(id=editing_id).update(title=new_depart_title)
            # 编辑部门则保持在当前页
            return redirect("/depart/list/" + str(page))
    return render(request, "depart_list.html", {"queryset": queryset, "page_obj": page_object})


def depart_delete(request, cur_page):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/" + str(cur_page))


def user_list(request, page=1):
    form = UserModelForm()
    queryset = models.UserInfo.objects.all()

    # 分页
    paginator = Paginator(queryset, per_page=5)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1)
    queryset = paginator.page(page).object_list

    context = {
        'queryset': queryset,
        'gender_choice': models.UserInfo.gender_choices,
        'depart_list': models.Department.objects.all(),
        'page_obj': page_object,
        'form': form
    }

    if request.method == "POST":
        # 获取用户提交数据
        if 'add_user1' in request.POST:
            user_name = request.POST.get("user_name")
            pwd = request.POST.get("pwd")
            age = request.POST.get("age")
            deposit = request.POST.get("deposit")
            create_time = request.POST.get("time")
            gender_id = request.POST.get("gender")
            depart_id = request.POST.get("dp")
            # 添加到数据库中
            models.UserInfo.objects.create(name=user_name, password=pwd, age=age,
                                           deposit=deposit, create_time=create_time,
                                           gender=gender_id, depart_id=depart_id)
            return redirect("/user/list/" + str(paginator.num_pages))
        elif 'add_user2' in request.POST:
            context['form'] = UserModelForm(data=request.POST)
            if context['form'].is_valid():
                context['form'].save()
            else:
                return render(request, "user_list.html", context)
            return redirect("/user/list/" + str(paginator.num_pages))
        elif 'edit_user' in request.POST:
            editing_id = request.POST.get("user_id_editing")
            row_obj = models.UserInfo.objects.filter(id=editing_id).first()
            context['form'] = UserModelForm(data=request.POST, instance=row_obj)
            if context['form'].is_valid():
                context['form'].save()
            else:
                return render(request, "user_list.html", context)
            return redirect("/user/list/" + str(page))

    # 获取用户信息
    # queryset = models.UserInfo.objects.all()
    """
    for obj in queryset:
        # .get_gender_display()找到gender元组编号对应的值; .depart.id/.depart.title找到连表里的内容
        print(obj.get_gender_display(), obj.depart_id, obj.depart.id, obj.depart.title)
    """

    return render(request, "user_list.html", context)


def user_delete(request, cur_page):
    nid = request.GET.get("nid")
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/" + str(cur_page))


def number_list(request, page=1):
    form = NumberModelForm()
    # 搜索号码
    data_dict = {}
    search_data = request.GET.get("query", "")
    if search_data:
        data_dict["mobile__contains"] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 分页
    paginator = Paginator(queryset, per_page=5)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1)
    queryset = paginator.page(page).object_list

    context = {
        "queryset": queryset,
        "form": form,
        "search_data": search_data,
        "page_obj": page_object,
    }

    if request.method == "POST":
        if 'add_number' in request.POST:
            context['form'] = NumberModelForm(data=request.POST)
            if context['form'].is_valid():
                context['form'].save()
            else:
                return render(request, "number_list.html", context)
            return redirect("/number/list/" + str(paginator.num_pages))
        if 'edit_number' in request.POST:
            editing_id = request.POST.get("number_id_editing")
            row_obj = models.PrettyNum.objects.filter(id=editing_id).first()
            context['form'] = NumberEditModelForm(data=request.POST, instance=row_obj)
            if context['form'].is_valid():
                context['form'].save()
            else:
                return render(request, "number_list.html", context)
            return redirect("/number/list/" + str(page) + "?query=" + search_data)

    return render(request, "number_list.html", context)


def number_delete(request, cur_page, q=""):
    nid = request.GET.get("nid")
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/number/list/" + str(cur_page) + "?query=" + q)


def admin_list(request, page=1):
    """ 管理员列表 """
    form = AdminModelForm()
    # 搜索号码
    data_dict = {}
    search_data = request.GET.get("query", "")
    if search_data:
        data_dict["username__contains"] = search_data
    queryset = models.Admin.objects.filter(**data_dict).all()

    # 分页
    paginator = Paginator(queryset, per_page=5)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1)
    queryset = paginator.page(page).object_list

    context = {
        "queryset": queryset,
        "form": form,
        "search_data": search_data,
        "page_obj": page_object,
    }

    if request.method == "POST":
        if 'add_admin' in request.POST:
            context['form'] = AdminModelForm(data=request.POST)
            if context['form'].is_valid():
                context['form'].save()
            else:
                return render(request, "admin_list.html", context)
            return redirect("/admin/list/" + str(paginator.num_pages))
        if 'edit_admin' in request.POST:
            editing_id = request.POST.get("admin_id_editing")
            row_obj = models.Admin.objects.filter(id=editing_id).first()
            context['form'] = AdminEditModelForm(data=request.POST, instance=row_obj)
            if context['form'].is_valid():
                context['form'].save()
            else:
                return render(request, "admin_list.html", context)
            return redirect("/admin/list/" + str(page) + "?query=" + search_data)

    return render(request, "admin_list.html", context)


def admin_delete(request, cur_page, q=""):
    nid = request.GET.get("nid")
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/" + str(cur_page) + "?query=" + q)


def admin_reset(request, nid):
    """ 编辑管理员密码 """
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect("/admin/list/")

    title = "重置密码 - {}".format(row_obj.username)
    if request.method == 'GET':
        form = AdminPwdResetModelForm()
        return render(request, "admin_edit.html", {'form': form, 'title': title})

    form = AdminPwdResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "admin_edit.html", {'form': form, 'title': title})


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        form.cleaned_data.pop("captcha")
        # 获取到的用户名、密码去数据库校验
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("username", "Incorrect username or password")
            return render(request, "login.html", {'form': form})
        # 用户名密码正确，跳转到admin_list
        request.session["info"] = {'id': admin_obj.id, 'name': admin_obj.username}
        return redirect("/admin/list/")
    return render(request, "login.html", {'form': form})


def sign_out(request):
    request.session.clear()
    return redirect("/login/")


def order_list(request, page=1):
    form = OrderModelForm()
    queryset = models.Order.objects.all().order_by("-id")
    # 分页
    paginator = Paginator(queryset, per_page=5)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1)
    queryset = paginator.page(page).object_list

    context = {
        "queryset": queryset,
        "form": form,
        "page_obj": page_object,
    }
    return render(request, "order_list.html", context)


@csrf_exempt
def order_add(request):
    """ 创建订单 """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 随机生成order ID，非用户输入
        form.instance.order_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(10000, 99999))
        # Customer为当前登录用户，注意需要把customer写为customer_id！
        form.instance.customer_id = request.session["info"]["id"]
        # 保存到数据库
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get("uid")
    exist = models.Order.objects.filter(id=uid).exists()
    if not exist:
        return JsonResponse({"status": False, "error": "Order does not exist!"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据ID获取订单详情 """
    uid = request.GET.get("uid")
    # 获取当前order的数据字典
    row_dict = models.Order.objects.filter(id=uid).values("product", "price", "status").first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "Order does not exist!"})
    result = {
        "status": True,
        "data": row_dict,
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_obj = models.Order.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, "msg": "Order does not exist!"})

    form = OrderModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def chart_list(request):
    """ 数据统计页面 """
    return render(request, "chart_list.html")


def chart_bar(request):
    """ 构造柱状图 """
    data_series = [{
        "name": 'Tokyo',
        "data": [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4,
                 194.1, 95.6, 54.4]
    }, {
        "name": 'New York',
        "data": [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5,
                 106.6, 92.3]
    }]
    x_axis = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    result = {
        "status": True,
        "data": {
            "data_series": data_series,
            "x_axis": x_axis,
        }
    }
    return JsonResponse(result)


def chart_line(request):
    """ 构造折线图 """
    data_series = [{
        "name": 'Installation & Developers',
        "data": [43934, 48656, 65165, 81827, 112143, 142383,
                 171533, 165174, 155157, 161454, 154610]
    }, {
        "name": 'Manufacturing',
        "data": [24916, 37941, 29742, 29851, 32490, 30282,
                 38121, 36885, 33726, 34243, 31050]
    }, {
        "name": 'Other',
        "data": [21908, 5548, 8105, 11248, 8989, 11816, 18274,
                 17300, 13053, 11906, 10073]
    }]
    x_start = 2010

    result = {
        "status": True,
        "data": {
            "data_series": data_series,
            "x_start": x_start,
        }
    }
    return JsonResponse(result)


def chart_pie(request):
    """ 构造饼图 """
    data_series = [{
        "name": 'Chrome',
        "y": 8,
        # "sliced": True,
        # "selected": True
    }, {
        "name": 'Firefox',
        "y": 10
    }, {
        "name": 'Safari',
        "y": 6
    }, {
        "name": 'Other',
        "y": 3
    }]

    result = {
        "status": True,
        "data": {
            "data_series": data_series,
        }
    }
    return JsonResponse(result)
