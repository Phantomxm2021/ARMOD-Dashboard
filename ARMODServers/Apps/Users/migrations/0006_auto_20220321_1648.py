# Generated by Django 3.2 on 2022-03-21 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20210419_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Create Time'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete Flag'),
        ),
        migrations.AlterField(
            model_name='user',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Update Time'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_uid',
            field=models.BigIntegerField(db_index=True, default=-1, verbose_name='User Id'),
        ),
    ]
