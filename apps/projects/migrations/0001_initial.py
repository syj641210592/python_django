# Generated by Django 3.2.1 on 2021-06-24 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsModel',
            fields=[
                ('id', models.AutoField(help_text='主键', primary_key=True, serialize=False, verbose_name='主键')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('desc', models.TextField(default='', help_text='注释', verbose_name='注释')),
                ('name', models.CharField(help_text='名称', max_length=50, unique=True, verbose_name='名称')),
                ('leader', models.CharField(help_text='项目负责人', max_length=50, verbose_name='负责人')),
                ('tester', models.CharField(help_text='项目测试人员', max_length=50, verbose_name='测试人员')),
                ('programmer', models.CharField(help_text='开发人员', max_length=50, verbose_name='开发人员')),
                ('publish_app', models.CharField(help_text='发布应用', max_length=100, verbose_name='发布应用')),
            ],
            options={
                'verbose_name': '项目信息',
                'verbose_name_plural': '项目信息',
                'db_table': 'tb_projects',
                'ordering': ['id'],
            },
        ),
    ]
