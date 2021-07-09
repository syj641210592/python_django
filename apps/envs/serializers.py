from rest_framework import serializers
from .models import EnvsModel
from utils.validate import Serializers_Validate


# 环境模型序列化器类
class EnvsModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = EnvsModel
        # 指定序列化模型类中的字段
        exclude = ("update_time", )  # 将所有模型类视图中的字段进行转换


# 环境模型序列化器类
class EnvsDiyModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = EnvsModel
        # 指定序列化模型类中的字段
        fields = ("id", "name")


class EnvsIdModelSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(label="环境id",
                                      help_text="环境id",
                                      validators=[
                                          Serializers_Validate(
                                              function="object_is_exist",
                                              obj=EnvsModel)
                                      ])

    class Meta:
        # 指定模型类
        model = EnvsModel
        # 指定序列化模型类中的字段
        fields = ("env_id", )
