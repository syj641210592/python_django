from rest_framework import viewsets
from rest_framework import filters

from .models import ProjectsModel
from .serializers import ProjectsModelSerializer
from utils.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(methods=["GET"], detail=False)
    def names(self, ruquest, *args, **kwargs):
        # 定义新的结果数据
        name_prjects_list = []
        # 获取所有项目数据
        all_prjects_list = super().list(ruquest, *args, **kwargs)
        # 重定义结果数据
        for project in all_prjects_list.data["results"]:
            name_prjects_dict = {}
            for key, value in project.items():
                if key in ["id", "name"]:
                    name_prjects_dict[key] = value
            name_prjects_list.append(name_prjects_dict)
        return Response(name_prjects_list)

    @action(methods=["GET"], detail=True)
    def interfaces(self, ruquest, *args, **kwargs):
        # 获取projects表id数据
        projects_queryset = self.get_object()
        # 获取id对应的interfaces数据
        interfaces_queryset = projects_queryset.project_link_Interface.all()
        # 修改返回数据
        # 定义新的结果数据
        respones_list = []
        for project in interfaces_queryset:
            respones_dict = {}
            for key, value in project.items():
                if key in ["id", "name"]:
                    respones_dict[key] = value
            respones_list.append(respones_dict)
        return Response(respones_list)