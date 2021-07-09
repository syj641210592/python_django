import json

from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action

from envs.serializers import EnvsIdModelSerializer
from testcases.models import TestcasesModel
from utils import comment
from utils.pagination import PageNumberPagination

from .models import TestsuitsModel
from .serializers import TestsuitsDiyModelSerializer, TestsuitsModelSerializer


class TestsuitsViewSet(viewsets.ReadOnlyModelViewSet):
    # 指定模型类
    queryset = TestsuitsModel.objects.all()
    # 指定序列化模型类
    serializer_class = TestsuitsModelSerializer
    # 指定过滤器
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # 指定分页引擎
    pagination_class = PageNumberPagination
    # 指定搜索字段规则
    search_fields = ['=name', '=id']
    # 指定排序字段
    ordering_fields = ['id', 'name']
    # 鉴权方式
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        # 指定序列化模型类
        self.serializer_class = TestsuitsDiyModelSerializer
        # 指定序列化模型类
        response = super().retrieve(request, *args, **kwargs)
        return response

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        # 创建接口级别测试启动实例
        path_dict = comment.http_run_env_get(self)
        instance = path_dict["instance"]
        include = json.loads(instance.include)
        # 取出当前套件下的所有测试接口
        for interface_id in include:
            querysets = TestcasesModel.objects.filter(
                interface_id=interface_id)
            path_dict["instance"] = querysets.first()
            path_dict["querysets"] = querysets
            response = comment.http_run(path_dict)
        return response

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        if self.action == "run":
            return EnvsIdModelSerializer
        else:
            return super().get_serializer_class()
