from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserRegisterModelSeralizer(serializers.ModelSerializer):
    """注册接口序列化器类"""

    # 自定义校验函数名称 必须以validate_  开头
    def validate(self, attr: dict):
        """校验两次输入的密码一致"""
        # 校验通过 删除password_confirm 返回校验通过后想传递的值
        if attr["password_confirm"] == attr["password"]:
            attr.pop("password_confirm")
            return attr
        # 校验不通过 必须抛出ValidationError异常
        else:
            raise serializers.ValidationError("两次密码不一致")

    password_confirm = serializers.CharField(label='二次输入密码',
                                             help_text='二次输入密码',
                                             write_only=True)

    class Meta:
        # 指定模型类
        model = User
        # 指定序列化模型类中的字段
        fields = "__all__"
        # 对现有的字段加入额外的校验项
        extra_kwargs = {
            "email": {
                'required':
                True,
                "allow_blank":
                False,
                "validators": [
                    UniqueValidator(queryset=User.objects.all(),
                                    message="邮箱名称已存在")
                ]
            },
            "password": {
                "min_length": 5,
                "max_length": 10,
                "write_only": True
            },
            "username": {
                "min_length": 5,
                "max_length": 20
            }
        }


class UserInforModelSeralizer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = User
        # 指定序列化模型类中的字段
        fields = ("username", "is_superuser", "date_joined", "last_login")
        read_only_fields = ("username", "is_superuser", "date_joined",
                            "last_login")

    def to_representation(self, data):
        res = super().to_representation(data)
        res["role"] = "管理员" if res.pop("is_superuser") else "普通用户"
        return res
