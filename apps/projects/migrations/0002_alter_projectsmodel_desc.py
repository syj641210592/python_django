# Generated by Django 3.2.1 on 2021-06-25 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectsmodel',
            name='desc',
            field=models.TextField(blank=True, default='', help_text='注释', null=True, verbose_name='注释'),
        ),
    ]
