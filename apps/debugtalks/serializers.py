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
        fields = ("id", "project", "name", "debugtalk")
        # 批量修改read_only=True字段
        read_only_fields = ["id", "project", "name", "debugtalk"]

    def to_representation(self, data):
        res = super().to_representation(data)
        if self.context["view"].action == "retrieve":
            res = {"debugtalk": res["debugtalk"]}
        else:
            res.pop("debugtalk")
        return res


# 项目模型更新序列化器类
class DebugTalksUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = DebugTalksModel
        # 指定序列化模型类中的字段
        fields = ("id", "debugtalk")
