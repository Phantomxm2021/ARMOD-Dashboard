# Generated by Django 3.2 on 2022-02-16 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Applications', '0011_auto_20210419_0224'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationsModelV2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('app_uid', models.BigIntegerField(db_index=True, default=-1, unique=True, verbose_name='应用Id')),
                ('user_uid', models.BigIntegerField(db_index=True, default=-1, verbose_name='用户Id')),
                ('name', models.CharField(max_length=24, unique=True, verbose_name='应用名称')),
                ('packageid', models.CharField(db_index=True, max_length=64, verbose_name='应用绑定的包名')),
                ('description', models.CharField(default='', max_length=128, verbose_name='应用绑定的包名')),
                ('token', models.CharField(default='', max_length=256, verbose_name='应用用Token')),
                ('app_icon_image', models.CharField(default='', max_length=128, verbose_name='应用绑定的包名')),
                ('child_project', models.IntegerField(default=0, verbose_name='应用下项目数')),
            ],
            options={
                'verbose_name': 'Applications_V2',
                'verbose_name_plural': 'Applications_V2',
                'db_table': 'armod_applications_v2',
            },
        ),
    ]