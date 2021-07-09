import json

from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TestcasesModel
from .serializers import TestcasesModelSerializer
from envs.serializers import EnvsIdModelSerializer
from utils import comment
from utils import handle_datas
from utils.pagination import PageNumberPagination


class TestcasesViewSet(viewsets.ModelViewSet):
    # 指定模型类
    queryset = TestcasesModel.objects.all()
    # 指定序列化模型类
    serializer_class = TestcasesModelSerializer
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

    def retrieve(self, ruquest, *args, **kwargs):
        # 获取instance数据
        instance = self.get_object()
        try:
            testcase_include = json.loads(instance.include)
            testcase_request = json.loads(instance.request)
        except Exception:
            return Response({
                'msg': '解析include和request数据出错',
                'status': 400
            },
                            status=400)

        testcase_request_data = testcase_request.get('test').get('request')
        # 获取json参数
        json_data = testcase_request_data.get('json')
        json_data_str = json.dumps(json_data, ensure_ascii=False)

        # 获取extract参数
        extract_data = testcase_request.get('test').get('extract')
        extract_data = handle_datas.handle_data3(extract_data)

        # 获取validate参数
        validate_data = testcase_request.get('test').get('validate')
        validate_data = handle_datas.handle_data1(validate_data)

        # 获取variables参数
        variables_data = testcase_request.get('test').get('variables')
        variables_data = handle_datas.handle_data2(variables_data)

        # 获取parameters参数
        parameters_data = testcase_request.get('test').get('parameters')
        parameters_data = handle_datas.handle_data3(parameters_data)

        # 获取setup_hooks参数
        setup_hooks_data = testcase_request.get('test').get('setup_hooks')
        setup_hooks_data = handle_datas.handle_data5(setup_hooks_data)

        # 获取teardown_hooks参数
        teardown_hooks_data = testcase_request.get('test').get(
            'teardown_hooks')
        teardown_hooks_data = handle_datas.handle_data5(teardown_hooks_data)

        data = {
            "author":
            instance.author,
            "testcase_name":
            instance.name,
            "selected_configure_id":
            testcase_include.get('config'),
            "selected_interface_id":
            instance.interface_id,
            "selected_project_id":
            instance.interface.project_id,
            "selected_testcase_id":
            testcase_include.get('testcases'),
            "method":
            testcase_request_data.get('method'),
            "url":
            testcase_request_data.get('url'),
            "param":
            handle_datas.handle_data4(testcase_request_data.get('params')),
            "header":
            handle_datas.handle_data4(testcase_request_data.get('headers')),
            "variable":
            handle_datas.handle_data2(testcase_request_data.get('data')),
            "jsonVariable":
            json_data_str,
            "extract":
            extract_data,
            "validate":
            validate_data,
            # 用例的当前配置（variables）
            "globalVar":
            variables_data,
            "parameterized":
            parameters_data,
            "setupHooks":
            setup_hooks_data,
            "teardownHooks":
            teardown_hooks_data
        }

        return Response(data, status=200)

    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        # 创建用例级别测试启动实例
        path_dict = comment.http_run_env_get(self)
        path_dict["querysets"] = [path_dict["instance"]]
        response = comment.http_run(path_dict)
        return response

    def get_serializer_class(self):
        """
        重定义模型序列化器类指定
        """
        if self.action == "run":
            return EnvsIdModelSerializer
        else:
            return super().get_serializer_class()
