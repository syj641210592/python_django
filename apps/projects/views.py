from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action

from configures.models import ConfiguresModel
from debugtalks.models import DebugTalksModel
from interfaces.models import InterfacesModel
from testcases.models import TestcasesModel
from testsuites.models import TestsuitsModel
from utils.pagination import PageNumberPagination
from .models import ProjectsModel
from .serializers import ProjectsModelSerializer, ProjectsDiyModelSerializer


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
            item['testsuits'] = TestsuitsModel.objects.filter(
                project=item["id"]).count()
            item['interfaces'] = InterfacesModel.objects.filter(
                project=item["id"]).count()
            item['testcases'] = TestcasesModel.objects.filter(
                interface__project=item["id"]).count()
            item['configures'] = ConfiguresModel.objects.filter(
                interface__project=item["id"]).count()
        # 返回结果数据
        return respones_data

    @action(methods=["GET"], detail=False)
    def names(self, ruquest, *args, **kwargs):
        # # 定义新的结果数据
        response = super().list(ruquest, *args, **kwargs)
        return response

    @action(methods=["GET"], detail=True)
    def interfaces(self, ruquest, *args, **kwargs):
        # 获取interfaces模型查询结果
        response = super().retrieve(ruquest, *args, **kwargs)
        # 读取结果内的序列化数据
        response.data = response.data.get("project_link_Interface")
        return response

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        action_list = ["names", "interfaces"]
        if self.action in action_list:
            return ProjectsDiyModelSerializer
        else:
            return super().get_serializer_class()

    def get_serializer_context(self):
        return {"action": self.action}

    def paginate_queryset(self, queryset):
        """
        重定义分页引擎
        """
        dry_field = ["names", "interfaces"]
        if self.action in dry_field:
            return None
        else:
            # return self.serializer_class
            return super().paginate_queryset(queryset)
