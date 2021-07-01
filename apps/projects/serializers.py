from rest_framework import serializers
from .models import ProjectsModel
from interfaces.models import InterfacesModel


# 项目模型序列化器类
class ProjectsModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = ProjectsModel
        # 指定序列化模型类中的字段
        fields = "__all__"  # 将所有模型类视图中的字段进行转换


# 项目模型序列化器类
class InterfacesNamesModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = InterfacesModel
        # 指定序列化模型类中的字段
        fields = ("id", "name")


# 项目模型序列化器类
class ProjectsDiyModelSerializer(serializers.ModelSerializer):
    # 主表根据从表的外键字段获取从表信息, 并对信息进行序列化校
    project_link_Interface = InterfacesNamesModelSerializer(
        label='项目所属接口信息', help_text='项目所属接口信息', many=True)

    class Meta:
        # 指定模型类
        model = ProjectsModel
        # 指定序列化模型类中的字段
        fields = ("id", "name", "project_link_Interface")
        read_only_fields = ["id", "name", "project_link_Interface"]

    def to_representation(self, data):
        res = super().to_representation(data)
        if self.context["action"] == "names":
            res.pop("project_link_Interface")
        else:
            res = {"project_link_Interface": res["project_link_Interface"]}
        return res
