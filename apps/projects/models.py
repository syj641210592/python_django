from utils.models import BaseModel
from django.db import models


# Create your models here.
class ProjectsModel(BaseModel):
    # 项目负责人
    leader = models.CharField('负责人', max_length=50, help_text='项目负责人')
    # 项目测试人员
    tester = models.CharField('测试人员', max_length=50, help_text='项目测试人员')
    # 项目开发人员
    programmer = models.CharField('开发人员', max_length=50, help_text='开发人员')
    # 项目发布名称
    publish_app = models.CharField('发布应用', max_length=100, help_text='发布应用')

    # 内部类
    class Meta:
        # 数据表命
        db_table = "tb_projects"
        # 数据表描述信息
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name
        # 数据排序主键
        ordering = ["id"]

    def __str__(self):
        return self.name
