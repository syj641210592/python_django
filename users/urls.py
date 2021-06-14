"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework_jwt import views
from rest_framework import routers

from .views import UserRegisterViewSet, UserCountView

# 生成路由器
router = routers.SimpleRouter()
# 注册路由器
router.register("register", UserRegisterViewSet)

urlpatterns = [
    # 登陆
    path("login/", views.obtain_jwt_token),
    # 注册
    path("", include(router.urls)),
    # 查询用户信息
    re_path(r"(.*)/count/", UserCountView.as_view())
]
