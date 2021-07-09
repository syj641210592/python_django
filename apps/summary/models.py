# from django.db import models

# class SummaryModel(models.Model):
#     user = models.JSONField(verbose_name='用户信息', help_text='用户信息')
#     statistics = models.JSONField(verbose_name='用户信息', help_text='用户信息')

#     # 内部类
#     class Meta:
#         # 数据迁移时, 不创建数据表
#         abstract = True
#         verbose_name = '首页信息'
#         verbose_name_plural = verbose_name

#     def __str__(self):
#         return "首页信息"
