import json

from rest_framework import filters, permissions, viewsets
from rest_framework.response import Response

from utils.pagination import PageNumberPagination
from .models import ConfiguresModel
from interfaces.models import InterfacesModel
from .serializers import ConfiguresModelSerializer
from utils import handle_datas


class ConfiguresViewSet(viewsets.ModelViewSet):
    # 指定模型类
    queryset = ConfiguresModel.objects.all()
    # 指定序列化模型类
    serializer_class = ConfiguresModelSerializer
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
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request)

        # 处理请求头数据
        config_headers = config_request['config']['request'].get('headers')
        config_headers_list = handle_datas.handle_data4(config_headers)

        # 处理全局变量数据
        config_variables = config_request['config'].get('variables')
        config_variables_list = handle_datas.handle_data2(config_variables)

        data = {
            "header": config_headers_list,
            "globalVar": config_variables_list
        }

        return Response(data)