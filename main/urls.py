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
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # 项目
    path('projects/', include('projects.urls')),
    # 接口
    path('interfaces/', include('interfaces.urls')),
    # 该路径是rest自带的一个登陆接口界面 多用户开发中调试
    # path("login/", include("rest_framework.urls")),
    # 用户
    path('user/', include('users.urls')),
    path("docs",
         include_docs_urls(title="测试平台接口文档", description="xxx项目的接口测试说明文档"))
]
