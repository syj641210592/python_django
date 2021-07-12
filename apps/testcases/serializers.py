import json

from rest_framework import serializers

from interfaces.models import InterfacesModel
from projects.models import ProjectsModel
from .models import TestcasesModel
from utils.validate import Serializers_Validate


# 项目模型序列化器类
class InterfacesDiyModelSerializer(serializers.ModelSerializer):
    def validate(self, attr):
        """校验外键字段所属项目和接口id存在"""
        pid = attr["pid"]
        iid = attr["iid"]
        pid_iid_queryset = InterfacesModel.objects.filter(id=iid,
                                                          project_id=pid)
        if not pid_iid_queryset.exists():
            serializers.ValidationError(f"所属项目id:{pid}下接口id:{iid}不存在")
        return attr

    # 获从表取主表的其他信息  必须用从表的外键字段名
    project = serializers.SlugRelatedField(slug_field="name",
                                           label='所属项目名称',
                                           help_text='所属项目名称',
                                           read_only=True)
    pid = serializers.IntegerField(label='所属项目id',
                                   help_text='所属项目id',
                                   write_only=True,
                                   validators=[
                                       Serializers_Validate(
                                           function="object_is_exist",
                                           obj=ProjectsModel)
                                   ])
    iid = serializers.IntegerField(label='所属接口id',
                                   help_text='所属接口id',
                                   write_only=True,
                                   validators=[
                                       Serializers_Validate(
                                           function="object_is_exist",
                                           obj=InterfacesModel)
                                   ])

    class Meta:

        # 指定模型类
        model = InterfacesModel
        # 指定序列化模型类中的字段
        fields = ("name", "project", "pid", "iid")
        # 指定read_only字段
        read_only_fields = ("name", )


# 用例模型序列化器类
class TestcasesModelSerializer(serializers.ModelSerializer):
    interface = InterfacesDiyModelSerializer(label='用例所属接口和接口项目信息',
                                             help_text='用例所属接口和接口项目信息')

    class Meta:
        # 指定模型类
        model = TestcasesModel
        # 指定序列化模型类中的字段
        exclude = ("create_time", "update_time")  # 将所有模型类视图中的字段进行转换
        # 对现有的字段加入额外的校验项
        extra_kwargs = {
            "desc": {
                "write_only": True
            },
            "request": {
                "write_only": True,
                "validators":
                [Serializers_Validate(function="validate_request")]
            },
            "include": {
                "required": False,
                "validators":
                [Serializers_Validate(function="validate_include")]
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

    def to_representation(self, data):
        # 原本校验功能
        res = super().to_representation(data)
        # 将include数据序列化时处理成json个数数据
        if "include" in res:
            res["include"] = json.loads(res["include"])
        return res
