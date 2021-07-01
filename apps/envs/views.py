from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action

from utils.pagination import PageNumberPagination
from .models import EnvsModel
from .serializers import EnvsModelSerializer, EnvsDiyModelSerializer


class EnvsViewSet(viewsets.ModelViewSet):
    # 指定模型类
    queryset = EnvsModel.objects.all()
    # 指定序列化模型类
    serializer_class = EnvsModelSerializer
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

    @action(methods=["GET"], detail=False)
    def names(self, ruquest, *args, **kwargs):
        # # 定义新的结果数据
        response = super().list(ruquest, *args, **kwargs)
        return response

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        action_list = ["names"]
        if self.action in action_list:
            return EnvsDiyModelSerializer
        else:
            return super().get_serializer_class()

    def paginate_queryset(self, queryset):
        """
        重定义分页引擎
        """
        dry_field = ["names"]
        if self.action in dry_field:
            return None
        else:
            # return self.serializer_class
            return super().paginate_queryset(queryset)
