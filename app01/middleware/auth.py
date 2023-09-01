from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 排除不需要登录就能访问的页面（白名单
        # request.path_info 获取当前用户请求的URL
        if request.path_info == "/login/":
            return
        # 1. 读取当前用户的seesion信息，如果有，说明已登陆过，可以向后走
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 没有登陆过，跳转到登陆页面
        return redirect("/login/")
