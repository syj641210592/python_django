from rest_framework.validators import UniqueValidator  # 唯一值校验
from rest_framework import serializers

from .models import InterfacesModel
from projects.models import ProjectsModel
from testcases.models import TestcasesModel
from configures.models import ConfiguresModel


# 接口模型序列化器类
class InterfacesModelSerializer(serializers.ModelSerializer):

    # 外键字段[必须加 因为原本定义的外键字段interface 因为要返回父表信息被占用后 未进行反序列化校验]
    project_id = serializers.PrimaryKeyRelatedField(
        label='所属项目id',
        help_text='所属项目id',
        queryset=ProjectsModel.objects.all())

    # 获从表取主表的打印值 models.__str__
    project = serializers.StringRelatedField(label='所属项目名称',
                                             help_text='所属项目名称')

    class Meta:

        # 自定义校验函数名称 必须以validate_  开头
        def validate_name_contains(attr):
            """校验字段输入名称包含接口"""
            # 字段值会自动以attr参数进行传递
            # 校验通过 返回校验通过后想传递的值
            contain_text = "接口"
            if attr.endswith(contain_text):
                return attr
            # 校验不通过 必须抛出ValidationError异常
            else:
                raise serializers.ValidationError("项目名称没有以接口结尾")

        # 指定模型类
        model = InterfacesModel
        # 指定序列化模型类中的字段
        fields = "__all__"  # 将所有模型类视图中的字段进行转换
        # 对现有的字段加入额外的校验项
        extra_kwargs = {
            "name": {
                "min_length":
                3,
                "validators": [
                    UniqueValidator(queryset=InterfacesModel.objects.all(),
                                    message="接口名称不唯一"), validate_name_contains
                ]
            }
        }

    def to_internal_value(self, data):
        # 前置处理代码块
        # 原本校验功能
        res = super().to_internal_value(data)
        # 将project_id校验后的instance数据替换成id值
        res["project_id"] = res["project_id"].id
        # 后置处理代码块
        return res


# 用例自定义字段模型序列化器类
class TestcasesNameModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = TestcasesModel
        # 指定序列化模型类中的字段
        fields = ("id", "name")


# 配置定义字段模型序列化器类
class ConfiguresNameModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = ConfiguresModel
        # 指定序列化模型类中的字段
        fields = ("id", "name")


# 项目模型序列化器类
class InterfacesDiryModelSerializer(serializers.ModelSerializer):
    # 主表根据从表的外键字段获取从表信息, 并对信息进行序列化校
    testcasesmodel_set = TestcasesNameModelSerializer(label='接口所属用例信息',
                                                      help_text='接口所属用例信息',
                                                      many=True)

    configures = ConfiguresNameModelSerializer(label='接口所属配置信息',
                                               help_text='接口所属配置信息',
                                               many=True)

    class Meta:
        # 指定模型类
        model = InterfacesModel
        # 指定序列化模型类中的字段
        fields = ("testcasesmodel_set", "configures")
        read_only_fields = ["testcasesmodel_set", "configures"]

    def to_representation(self, data):
        res = super().to_representation(data)
        if "testcases" in self.context["request"].path:
            res = {"testcasesmodel_set": res["testcasesmodel_set"]}
        else:
            res = {"configures": res["configures"]}
        return res
