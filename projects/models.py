from utils.models import BaseModel
from django.db import models


# Create your models here.
class ProjectsModel(BaseModel):
    # 项目负责人
    leader = models.CharField(max_length=10,
                              verbose_name="项目负责人",
                              help_text="项目负责人")
    # 项目是否启动
    is_execute = models.BooleanField(verbose_name="项目是否启动",
                                     help_text="项目是否启动",
                                     default=True)

    # 内部类
    class Meta:
        # 数据表命
        db_table = "tb_projects"
        # 数据排序主键
        ordering = ["id"]
