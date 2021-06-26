from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from debugtalks.models import DebugTalksModel
from utils.pagination import PageNumberPagination

from .models import ProjectsModel
from .serializers import ProjectsDryModelSerializer, ProjectsModelSerializer


class ProjectsViewSet(viewsets.ModelViewSet):
    # 指定模型类
    queryset = ProjectsModel.objects.all()
    # 指定序列化模型类
    serializer_class = ProjectsModelSerializer
    # 指定过滤器
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # 指定分页引擎
    pagination_class = PageNumberPagination
    # 指定搜索字段规则
    search_fields = ['=name', '=leader', '=id']
    # 指定排序字段
    ordering_fields = ['id', 'name']
    # 鉴权方式
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # 创建项目数据
        response_data = super().create(request, *args, **kwargs)
        # 创建debuglist数据
        DebugTalksModel.objects.create(project_id=response_data.data["id"])
        # 返回项目创建结果
        return response_data

    def list(self, request, *args, **kwargs):
        # 获取父对象list结果
        respones_data = super().list(request, *args, **kwargs)
        # 重定义结果数据
        for item in respones_data.data['results']:
            # 取出当前的数据id, 根据id获取对应的外键信息
            self.kwargs["pk"] = item["id"]
            projects_queryset = self.get_object()
            interfaces_querysets = projects_queryset.project_link_Interface.all(
            )
            item['testsuits'] = projects_queryset.testsuits.all().count()
            item['interfaces'] = interfaces_querysets.count()
            # 遍历所有的接口字段信息, 根据id获取外键数据
            testcases_count = 0
            configures_count = 0
            for interfaces_queryset in interfaces_querysets:
                testcases_count += interfaces_queryset.testcasesmodel_set.all(
                ).count() or 0
                configures_count += interfaces_queryset.configures.all().count(
                ) or 0
            item['testcases'] = testcases_count
            item['configures'] = configures_count

        # 返回结果数据
        return respones_data

    @action(methods=["GET"], detail=False)
    def names(self, ruquest, *args, **kwargs):
        # # 定义新的结果数据
        response = super().list(ruquest, *args, **kwargs)
        return response

    @action(methods=["GET"], detail=True)
    def interfaces(self, ruquest, *args, **kwargs):
        # 获取projects表id数据
        projects_queryset = self.get_object()
        # 获取id对应的interfaces数据
        interfaces_queryset = projects_queryset.project_link_Interface.all()
        # 修改返回数据
        # 定义新的结果数据
        respones_list = [{
            "id": project["id"],
            "name": project["name"]
        } for project in interfaces_queryset]
        return Response(respones_list)

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        dry_field = ["names", "interfaces"]
        if self.action in dry_field:
            return ProjectsDryModelSerializer
        else:
            # return self.serializer_class
            return super().get_serializer_class()

    def paginate_queryset(self, queryset):
        """
        重定义分页引擎
        """
        dry_field = ["interfaces"]
        if self.action in dry_field:
            return None
        else:
            # return self.serializer_class
            return super().paginate_queryset(queryset)
