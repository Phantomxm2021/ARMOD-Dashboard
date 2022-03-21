# Generated by Django 3.2 on 2022-02-01 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARExperiences', '0015_alter_arexperiencemodel_arexperience_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ARExperienceModelTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('arexperience_uid', models.BigIntegerField(blank=True, db_index=True, null=True, verbose_name='AR体验项目的ID')),
                ('name', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='项目名称')),
                ('app_uid', models.BigIntegerField(db_index=True, default=-1, verbose_name='所属应用的Id')),
                ('status', models.IntegerField(db_index=True, default=1, verbose_name='项目状态')),
                ('description', models.CharField(default='', max_length=128, verbose_name='项目描述')),
            ],
            options={
                'verbose_name': 'ARExperiencesTest',
                'verbose_name_plural': 'ARExperiencesTest',
                'db_table': 'armod_arexperiences_test',
            },
        ),
    ]