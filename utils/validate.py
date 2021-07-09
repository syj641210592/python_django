import re
import json

from rest_framework import serializers

from configures.models import ConfiguresModel
from testcases.models import TestcasesModel


class Serializers_Validate:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def object_is_exist(self, attr):
        """
        校验数据存在
        object: 模型类
        value: 字段值
        """
        obj = self.kwargs["obj"]
        res = obj.objects.filter(id=attr)
        if not res.exists():
            raise serializers.ValidationError("id不存在")
        return attr

    def validate_include(self, attr):
        """校验include字段数据为json格式, 如果存在需要校验数据内容和数据格式"""
        try:
            # 校验数据格式为json, 内容包含config和testcases, 且config值为整数, testcases为包含整数的列表
            res = re.match(
                r'^\{"config":\s*(\d+|null),\s*"testcases":\s*(\[.*\])\}$',
                attr)
            if not res:
                raise serializers.ValidationError("非有效的json格式数据")
            if not re.match(r"\[\]|\[\d+(,\s*\d+)\]*", res.group(2)):
                raise serializers.ValidationError("非有效的testcases格式数据")
            # 转换成json格式并对config和testcases进行校验
            if res.group(1) == "null":
                res = attr.replace("null", '""')
            if res.group(2) == "[]":
                res = attr.replace("[]", '""')
            res = json.loads(res)
            # 校验config的id存在
            if res["config"]:
                config_id_exist = ConfiguresModel.objects.filter(
                    id=res["config"]).exists()
                if not config_id_exist:
                    raise serializers.ValidationError("所属配置数据id不存在")
            # 校验testcases所属前置用例存在
            if res["testcases"]:
                for pk in res["testcases"]:
                    res = TestcasesModel.objects.filter(id=pk).exists()
                    if not res:
                        raise serializers.ValidationError("所属前置用例id不存在")
            return attr
        except Exception:
            raise serializers.ValidationError("校验include字段失败")

    def validate_request(self, attr):
        """校验request字段格式正确"""
        try:
            # 校验数据格式为json, 内容包含name request validate
            res = re.match(
                r'^\{"test":\s*\{("name":\s*\S*,)("request":\s*\{\S*\},).*("validate":\s*\[\S*\])\}\}$',
                attr)
            if not res:
                raise serializers.ValidationError("非有效的json格式数据")
            # 校验request数据格式包含url, method, json
            res_request = re.match(
                r'"request":\s*\{"url":\s*\S*,\s*"method":\s*\S*\},$',
                res.group(2))
            if not res_request:
                raise serializers.ValidationError("非有效的用例request格式数据")
            # 校验validate数据格式包含check, expected, comparator
            res_request = re.match(
                r'"validate":\s*\[(\{"check":\s*\S*,\s*"expected":\s*\S*,\s*"comparator":\s*\S*\})(,\{"check":\s*\S*,\s*"expected":\s*\S*,\s*"comparator":\s*\S*\})*\]$',
                res.group(3))
            if not res_request:
                raise serializers.ValidationError("非有效的用例validate格式数据")
            return attr
        except serializers.ValidationError as Error:
            raise Error
        except Exception:
            raise serializers.ValidationError("校验request字段失败")

    def __call__(self, attr):
        """
        调用校验方法
        function: 校验函数
        data: 校验参数
        """
        return getattr(self, self.kwargs["function"])(attr)
