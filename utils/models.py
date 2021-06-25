from django.db import models


# Create your models here.
class BaseModel(models.Model):
    # 对应模型内的数据主键id, 自增
    id = models.AutoField(primary_key=True,
                          verbose_name="主键",
                          help_text="主键",
                          blank=False,
                          null=False)
    # 对应模型内的数据创建时间
    create_time = models.DateTimeField(verbose_name="创建时间",
                                       help_text="创建时间",
                                       auto_now_add=True)
    # 对应模型内的数据更新时间
    update_time = models.DateTimeField(verbose_name="更新时间",
                                       help_text="更新时间",
                                       auto_now=True)
    # 对应模型内的数据注释
    desc = models.TextField(verbose_name="注释",
                            help_text="注释",
                            default="",
                            blank=True,
                            null=True)
    # 对应模型内的数据名称
    name = models.CharField(verbose_name="名称",
                            help_text="名称",
                            unique=True,
                            max_length=50)

    # 内部类
    class Meta:
        # 数据迁移时, 不创建数据表
        abstract = True
