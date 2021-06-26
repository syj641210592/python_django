from rest_framework import serializers
from .models import ProjectsModel


# 项目模型序列化器类
class ProjectsModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = ProjectsModel
        # 指定序列化模型类中的字段
        fields = "__all__"  # 将所有模型类视图中的字段进行转换
        # 序列化字段的深度
        depth = 1  # 解析字段的嵌套深度


# 项目模型序列化器类
class ProjectsDryModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = ProjectsModel
        # 指定序列化模型类中的字段
        fields = ("id", "name")
