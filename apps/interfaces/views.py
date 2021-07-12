from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework.decorators import action

from .models import InterfacesModel
from .serializers import InterfacesModelSerializer, InterfacesDiryModelSerializer
from envs.serializers import EnvsIdModelSerializer
from testcases.models import TestcasesModel
from configures.models import ConfiguresModel
from utils import comment
from utils.pagination import PageNumberPagination


class InterfacesViewSet(viewsets.ModelViewSet):
    # 指定模型类
    queryset = InterfacesModel.objects.all()
    # 指定序列化模型类
    serializer_class = InterfacesModelSerializer
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

    def list(self, request, *args, **kwargs):
        # 获取父对象list结果
        respones_data = super().list(request, *args, **kwargs)
        # 重定义结果数据
        for item in respones_data.data['results']:
            # 遍历所有的接口字段信息, 根据id获取外键数据
            item['testcases'] = TestcasesModel.objects.filter(
                interface_id=item["id"]).count()
            item['configures'] = ConfiguresModel.objects.filter(
                interface_id=item["id"]).count()
        # 返回结果数据
        return respones_data

    @action(methods=["GET"], detail=True, url_path="(testcases|configs)")
    def testcases_or_configs(self, ruquest, *args, **kwargs):
        # 获取interfaces模型查询结果
        response = super().retrieve(ruquest, *args, **kwargs)
        response.data = response.data["testcases_or_configures"]
        return response

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        # 创建接口级别测试启动实例
        path_dict = comment.http_run_env_get(self)
        # 取出当前接口下的所有测试用例
        querysets = TestcasesModel.objects.filter(
            interface_id=path_dict["instance"].id)
        response = comment.http_run(path_dict, querysets)
        return response

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        if self.action == "testcases_or_configs":
            return InterfacesDiryModelSerializer
        elif self.action == "run":
            return EnvsIdModelSerializer
        else:
            # return self.serializer_class
            return super().get_serializer_class()

    def paginate_queryset(self, queryset):
        """
        重定义分页引擎
        """
        dry_field = ["testcases_or_configures"]
        if self.action in dry_field:
            return None
        else:
            # return self.serializer_class
            return super().paginate_queryset(queryset)