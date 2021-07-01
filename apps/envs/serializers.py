from rest_framework import serializers
from .models import EnvsModel


# 环境模型序列化器类
class EnvsModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = EnvsModel
        # 指定序列化模型类中的字段
        fields = "__all__"  # 将所有模型类视图中的字段进行转换


# 环境模型序列化器类
class EnvsDiyModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = EnvsModel
        # 指定序列化模型类中的字段
        fields = ("id", "name")
