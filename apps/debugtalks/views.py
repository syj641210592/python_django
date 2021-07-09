from rest_framework import filters, permissions, mixins, viewsets

from utils.pagination import PageNumberPagination
from .models import DebugTalksModel
from .serializers import DebugTalksModelSerializer, DebugTalksUpdateSerializer


class DebugTalksViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    # 指定模型类
    queryset = DebugTalksModel.objects.all()
    # 指定序列化模型类
    serializer_class = DebugTalksModelSerializer
    # 指定过滤器
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # 指定分页引擎
    pagination_class = PageNumberPagination
    # 指定搜索字段规则
    search_fields = ['=name', '=id']
    # 指定排序字段
    ordering_fields = ['id', 'name']
    # 序列化器参数
    context = {}
    # 鉴权方式
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return response

    def get_serializer_class(self):
        if "update" in self.action:
            return DebugTalksUpdateSerializer
        else:
            return super().get_serializer_class()