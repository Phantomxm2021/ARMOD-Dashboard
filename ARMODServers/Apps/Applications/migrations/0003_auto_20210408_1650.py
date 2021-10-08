# Generated by Django 3.1.6 on 2021-04-08 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Applications', '0002_applicationsmodel_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationsmodel',
            name='child_project',
            field=models.IntegerField(default=0, verbose_name='应用下项目数'),
        ),
        migrations.AlterField(
            model_name='applicationsmodel',
            name='token',
            field=models.CharField(default='', max_length=512, verbose_name='应用用Token'),
        ),
    ]
