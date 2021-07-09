from rest_framework import serializers

from .models import ConfiguresModel
from interfaces.models import InterfacesModel
from testcases.serializers import InterfacesDiyModelSerializer
from utils.validate import Serializers_Validate


# 环境模型序列化器类
class ConfiguresModelSerializer(serializers.ModelSerializer):
    interface = InterfacesDiyModelSerializer(label='用例所属接口和接口项目信息',
                                             help_text='用例所属接口和接口项目信息')

    class Meta:
        # 指定模型类
        model = ConfiguresModel
        # 指定序列化模型类中的字段
        fields = "__all__"
        # 对现有的字段加入额外的校验项
        extra_kwargs = {
            "desc": {
                "write_only": True
            },
            "request": {
                "write_only": True
            }
        }

    def to_internal_value(self, data):
        """数据校验的入口方法"""
        # 前置处理代码块
        # 原本校验功能
        res = super().to_internal_value(data)
        # 后置处理代码块
        # 将interface在反序列话输入时替换成instance
        res["interface"] = InterfacesModel.objects.get(
            id=res["interface"]["iid"])
        return res
