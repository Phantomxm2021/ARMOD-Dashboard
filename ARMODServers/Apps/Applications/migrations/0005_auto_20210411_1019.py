# Generated by Django 3.1.4 on 2021-04-11 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Applications', '0004_auto_20210410_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationsmodel',
            name='packageid',
            field=models.CharField(db_index=True, max_length=64, verbose_name='应用绑定的包名'),
        ),
        migrations.AlterField(
            model_name='applicationsmodel',
            name='userid',
            field=models.IntegerField(db_index=True, default=-1, verbose_name='所属用户ID'),
        ),
    ]
