from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions

from .models import InterfacesModel
from testcases.models import TestcasesModel
from configures.models import ConfiguresModel
from .serializers import InterfacesModelSerializer, InterfacesDiryModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework.decorators import action


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

    @action(methods=["GET"], detail=True, url_path="(testcases|configures)")
    def testcases_or_configures(self, ruquest, *args, **kwargs):
        # 获取id对应的interfaces数据
        self.url = ruquest.path
        # 获取interfaces模型查询结果
        response = super().retrieve(ruquest, *args, **kwargs)
        if "testcases" in self.url:
            response.data = response.data["testcasesmodel_set"]
        else:
            response.data = response.data["configures"]
        return response

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        dry_field = ["testcases_or_configures"]
        if self.action in dry_field:
            return InterfacesDiryModelSerializer
        else:
            # return self.serializer_class
            return super().get_serializer_class()

    def get_serializer_context(self):
        """
        自定义向序列化器类传参
        """
        return {"url": self.url}

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