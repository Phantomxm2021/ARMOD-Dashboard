# Generated by Django 3.1.4 on 2021-04-18 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Applications', '0010_auto_20210413_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationsmodel',
            name='app_uid',
            field=models.BigIntegerField(db_index=True, default=-1, primary_key=True, serialize=False, verbose_name='应用Id'),
        ),
        migrations.AlterField(
            model_name='applicationsmodel',
            name='user_uid',
            field=models.BigIntegerField(db_index=True, default=-1, verbose_name='用户Id'),
        ),
    ]