from rest_framework.validators import UniqueValidator  # 唯一值校验
from rest_framework import serializers

from .models import InterfacesModel
from projects.models import ProjectsModel
from testcases.models import TestcasesModel
from configures.models import ConfiguresModel


# 接口模型序列化器类
class InterfacesModelSerializer(serializers.ModelSerializer):
    # 自定义校验函数名称 必须以validate_  开头
    def validate_foreignKey_exist(attr):
        """校验外键id必须存在"""
        # 获取主表所有信息
        quertset = ProjectsModel.objects.filter(id=attr)
        if not quertset:
            raise serializers.ValidationError(f"外键id:{attr}项目不存在")
        else:
            return attr

    # 外键字段[必须加 因为原本定义的外键字段interface 因为要返回父表信息被占用后 未进行反序列化校验]
    project_id = serializers.PrimaryKeyRelatedField(
        label='所属项目id',
        help_text='所属项目id',
        queryset=ProjectsModel.objects.all())

    # 获从表取主表的其他信息  必须用从表的外键字段名
    project = serializers.SlugRelatedField(
        slug_field="name", queryset=ProjectsModel.objects.all())

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
                raise serializers.ValidationError(f"项目名称没有以{contain_text}结尾")

        # 指定模型类
        model = InterfacesModel
        # 指定序列化模型类中的字段
        fields = "__all__"  # 将所有模型类视图中的字段进行转换
        # 序列化字段的深度
        depth = 1  # 解析字段的嵌套深度
        # 对现有的字段加入额外的校验项
        extra_kwargs = {
            "name": {
                "min_length": 3,
                "validators": {
                    UniqueValidator(queryset=InterfacesModel.objects.all(),
                                    message="接口名称已存在"), validate_name_contains
                }
            }
        }


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
        if "testcases" in self.context["url"]:
            res = {"testcasesmodel_set": res["testcasesmodel_set"]}
        else:
            res = {"configures": res["configures"]}
        return res
