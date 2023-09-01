"""secondSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 部门
    path('depart/list/', views.depart_list),
    path(
        'depart/list/<int:page>',
        views.depart_list,
        name="departs-by-page",
    ),
    path('depart/<int:cur_page>/delete/', views.depart_delete),

    # 用户
    path('user/list/', views.user_list),
    path(
        'user/list/<int:page>',
        views.user_list,
        name="users-by-page",
    ),
    path('user/<int:cur_page>/delete/', views.user_delete),

    # 靓号
    path('number/list/', views.number_list),
    path(
        'number/list/<int:page>',
        views.number_list,
        name="nums-by-page",
    ),
    path('number/<int:cur_page>/delete/', views.number_delete),
    path('number/<int:cur_page>/delete/<str:q>', views.number_delete),

    # 管理员
    path('admin/list/', views.admin_list),
    path(
        'admin/list/<int:page>',
        views.admin_list,
        name="admins-by-page",
    ),
    path('admin/<int:cur_page>/delete/', views.admin_delete),
    path('admin/<int:cur_page>/delete/<str:q>', views.admin_delete),
    path('admin/<int:nid>/reset/', views.admin_reset),

    # login
    path('login/', views.login),
    # sign out
    path('signout/', views.sign_out),

    # order
    path('order/list/', views.order_list),
    path(
        'order/list/<int:page>',
        views.order_list,
        name="orders-by-page",
    ),
    path('order/add/', views.order_add),
    path('order/delete/', views.order_delete),
    path('order/detail/', views.order_detail),
    path('order/edit/', views.order_edit),

    # charts
    path('chart/list/', views.chart_list),
    path('chart/bar/', views.chart_bar),
    path('chart/line/', views.chart_line),
    path('chart/pie/', views.chart_pie),

]
