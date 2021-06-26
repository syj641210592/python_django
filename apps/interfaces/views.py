from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions

from .models import InterfacesModel
from .serializers import InterfacesModelSerializer, InterfacesDryModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response


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
    search_fields = ['=name', '=tester', '=id']
    # 指定排序字段
    ordering_fields = ['id', 'name']
    # 鉴权方式
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        # 获取父对象list结果
        respones_data = super().list(request, *args, **kwargs)
        # 重定义结果数据
        for item in respones_data.data['results']:
            # 取出当前的数据id, 根据id获取对应的外键信息
            self.kwargs["pk"] = item["id"]
            interfaces_queryset = self.get_object()
            # 遍历所有的接口字段信息, 根据id获取外键数据
            item['testcases'] = interfaces_queryset.testcasesmodel_set.all(
            ).count() or 0
            item['configures'] = interfaces_queryset.configures.all().count(
            ) or 0
        # 返回结果数据
        return respones_data

    @action(methods=["GET"], detail=False)
    def names(self, ruquest, *args, **kwargs):
        # # 定义新的结果数据
        response = super().list(ruquest, *args, **kwargs)
        return response

    @action(methods=["GET"], detail=True, url_path="(testcases|configures)")
    def testcases_or_configures(self, ruquest, *args, **kwargs):
        # 获取interfaces表id数据
        interfaces_queryset = self.get_object()
        # 获取id对应的interfaces数据
        url = ruquest.path
        if "testcases" in url:
            querysets = interfaces_queryset.testcasesmodel_set.all()
        else:
            querysets = interfaces_queryset.configures.all()
        # 修改返回数据
        # 定义新的结果数据
        respones_list = [{
            "id": queryset["id"],
            "name": queryset["name"]
        } for queryset in querysets]
        return Response(respones_list)

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        dry_field = ["names"]
        if self.action in dry_field:
            return InterfacesDryModelSerializer
        else:
            # return self.serializer_class
            return super().get_serializer_class()

    def paginate_queryset(self, queryset):
        """
        重定义分页引擎
        """
        dry_field = ["names", "testcases_or_configures"]
        if self.action in dry_field:
            return None
        else:
            # return self.serializer_class
            return super().paginate_queryset(queryset)