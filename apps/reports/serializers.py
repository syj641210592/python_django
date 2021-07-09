import json

from rest_framework import serializers

from .models import ReportsModel


# 项目模型序列化器类
class ReportsModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 校验summary字段数据为json
        def validate_summary_is_json(attr):
            try:
                res = json.loads(attr)
                if res:
                    return attr
                else:
                    raise json.decoder.JSONDecodeError
            except Exception:
                raise serializers.ValidationError("非json格式数据")

        # 指定模型类
        model = ReportsModel
        # 指定序列化模型类中的字段
        exclude = ("update_time", )
        # 补充字段属性
        extra_kwargs = {
            # 说明信息可不输出
            "desc": {
                "write_only": True
            },
            # summary字段添加json格式校验
            "summary": {
                "validators": {validate_summary_is_json}
            }
        }

    def to_representation(self, data):
        res = super().to_representation(data)
        res["result"] = "Pass" if res["result"] else "Fail"
        res["summary"] = json.loads(res["summary"])
        if self.context["view"].action == "download":
            res = {"html": res["html"], "name": res["name"]}
        else:
            res.pop("html")
        return res
