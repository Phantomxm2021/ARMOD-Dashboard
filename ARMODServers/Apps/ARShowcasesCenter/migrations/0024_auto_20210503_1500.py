# Generated by Django 3.1.6 on 2021-05-03 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARShowcasesCenter', '0023_auto_20210503_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arshowcasescentermodel',
            name='showcase_not_index_tags',
            field=models.CharField(default='', max_length=1024, verbose_name='Showcase not index'),
        ),
    ]
