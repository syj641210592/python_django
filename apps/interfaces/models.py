from utils.models import BaseModel
from django.db import models


# Create your models here.
class InterfacesModel(BaseModel):
    # 项目测试人员
    tester = models.CharField(max_length=10,
                              verbose_name="项目测试人员",
                              help_text="项目测试人员")
    # 对应的项目id
    project = models.ForeignKey("projects.ProjectsModel",
                                on_delete=models.CASCADE,
                                verbose_name="外键_项目id",
                                help_text="外键_项目id",
                                related_name="project_link_Interface")

    # 内部类
    class Meta:
        # 数据表命
        db_table = "tb_interfaces"
        # 数据表描述信息
        verbose_name = '接口信息'
        verbose_name_plural = verbose_name
        # 数据排序主键
        ordering = ["id"]

    def __str__(self):
        return self.name