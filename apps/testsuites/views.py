from rest_framework import filters, permissions, viewsets

from utils.pagination import PageNumberPagination
from .models import TestsuitsModel
from .serializers import TestsuitsModelSerializer, TestsuitsDiyModelSerializer


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
