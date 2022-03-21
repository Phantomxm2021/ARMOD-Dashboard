# Generated by Django 3.2 on 2022-03-21 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0038_auto_20220216_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexguidefeatures',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexguidefeatures',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexguidefeatures',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='indexguides',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexguides',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexguides',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='indexheader',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexheader',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexheader',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='indexnavbar',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexnavbar',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexnavbar',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='indexpageqamodel',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexpageqamodel',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexpageqamodel',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='indexpageviewkeybenfitsmodel',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexpageviewkeybenfitsmodel',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexpageviewkeybenfitsmodel',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='indexpageviewmainkeybenfitsmodel',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexpageviewmainkeybenfitsmodel',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexpageviewmainkeybenfitsmodel',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='indexsocialnavbar',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='indexsocialnavbar',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='indexsocialnavbar',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
    ]