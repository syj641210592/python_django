from rest_framework import filters, permissions, viewsets

from utils.pagination import PageNumberPagination
from .models import DebugTalksModel
from .serializers import DebugTalksModelSerializer


class DebugTalksViewSet(viewsets.ModelViewSet):
    # 指定模型类
    queryset = DebugTalksModel.objects.all()
    # 指定序列化模型类
    serializer_class = DebugTalksModelSerializer
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
