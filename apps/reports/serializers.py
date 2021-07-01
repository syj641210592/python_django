import pickle, json

from rest_framework import serializers
from .models import ReportsModel


# 项目模型序列化器类
class ReportsModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 指定模型类
        model = ReportsModel
        # 指定序列化模型类中的字段
        exclude = ("desc", "update_time")  # 排除特定模型类视图中的字段进行转换

    def to_representation(self, data):
        res = super().to_representation(data)
        res["result"] = "Pass" if res["result"] else "Fail"
        if self.context["view"].action == "download":
            res = {"html": res["html"], "name": res["name"]}
        else:
            res.pop("html")
        return res
