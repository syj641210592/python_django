from rest_framework import viewsets
from rest_framework import filters

from .models import ProjectsModel
from .serializers import ProjectsModelSerializer
from utils.pagination import PageNumberPagination


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