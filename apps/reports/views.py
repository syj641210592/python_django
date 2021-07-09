from rest_framework import filters, permissions, viewsets, mixins
from rest_framework.decorators import action
from django.http.response import FileResponse

from utils.pagination import PageNumberPagination
from .models import ReportsModel
from .serializers import ReportsModelSerializer


class ReportsViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, viewsets.GenericViewSet):
    # 指定模型类
    queryset = ReportsModel.objects.all()
    # 指定序列化模型类
    serializer_class = ReportsModelSerializer
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

    @action(methods=["GET"], detail=True)
    def download(self, ruquest, *args, **kwargs):
        # # 定义新的结果数据
        res = super().retrieve(ruquest, *args, **kwargs)
        response = FileResponse(res.data["html"])
        response['Content-Type'] = 'application/octet-stream'
        response[
            'Content-Disposition'] = f"attachment; filename*=UTF-8 '' {res.data['name'] + '.html'}"
        return response

    def get_serializer_context(self):
        """自定义序列化器传参"""
        self.context = super().get_serializer_context()
        # 该参数在原context["view"].action已经存在, 可以不写
        self.context["action"] = self.action
        return self.context
