from rest_framework import serializers
from .models import DebugTalksModel


# 项目模型序列化器类
class DebugTalksModelSerializer(serializers.ModelSerializer):
    # 获从表取主表的其他信息  必须用从表的外键字段名
    project = serializers.SlugRelatedField(
        slug_field="name", queryset=DebugTalksModel.objects.all())

    class Meta:
        # 指定模型类
        model = DebugTalksModel
        # 指定序列化模型类中的字段
        fields = ("id", "project", "name")  # 将所有模型类视图中的字段进行转换
        # 序列化字段的深度
        depth = 1  # 解析字段的嵌套深度
