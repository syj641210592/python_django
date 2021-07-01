from rest_framework import serializers
from .models import TestsuitsModel
from projects.models import ProjectsModel


# 项目模型序列化器类
class TestsuitsModelSerializer(serializers.ModelSerializer):
    # 外键字段[必须加 因为原本定义的外键字段interface 因为要返回父表信息被占用后 未进行反序列化校验]
    project_id = serializers.PrimaryKeyRelatedField(
        label='所属项目id',
        help_text='所属项目id',
        queryset=ProjectsModel.objects.all())

    # 获从表取主表的其他信息  必须用从表的外键字段名
    project = serializers.SlugRelatedField(
        slug_field="name", queryset=ProjectsModel.objects.all())

    class Meta:
        # 指定模型类
        model = TestsuitsModel
        # 指定序列化模型类中的字段
        exclude = ("desc", "include")  # 将所有模型类视图中的字段进行转换


# 项目模型序列化器类
class TestsuitsDiyModelSerializer(TestsuitsModelSerializer):
    class Meta(TestsuitsModelSerializer.Meta):
        # 指定序列化模型类中的字段
        fields = ("name", "project_id", "include")  # 将所有模型类视图中的字段进行转换
        exclude = ()
