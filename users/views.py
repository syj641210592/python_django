import re

from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from rest_framework.views import APIView

from .serializers import UserRegisterModelSeralizer
from utils.jwt import jwt_response_payload_handler


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # 指定模型类
    queryset = User.objects.all()
    # 指定序列化模型类
    serializer_class = UserRegisterModelSeralizer

    def create(self, request, *args, **kwargs):
        """重写 创建账户"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 创建用户
            queryset = User.objects.create_user(**serializer.validated_data)
            # 生成payload
            payload = jwt_payload_handler(queryset)
            # 生成token
            token = jwt_encode_handler(payload)
            # 响应结果
            response_data = jwt_response_payload_handler(
                token, queryset, request)
            return Response(response_data)


class UserCountView(APIView):
    def get(self, ruquest, *args, **kwargs):
        # 获取请求路径
        url_path = ruquest.get_full_path()
        # 提取参数
        url_parmar = re.findall(r"/user/(.*)/count/$", url_path)
        # 提取email参数
        url_parmar_email = re.findall(
            r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$", url_parmar[0])
        # 判断为查询email
        if url_parmar_email:
            queryset = User.objects.filter(email=url_parmar_email[0])
            response_data = {"email": url_parmar_email[0]}
        # 判断为查询username
        elif url_parmar:
            queryset = User.objects.filter(username=url_parmar[0])
            response_data = {"username": url_parmar[0]}
        response_data.update({"count": queryset.count()})
        return Response(response_data)
