# Generated by Django 3.1.4 on 2021-04-21 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARShowcasesCenter', '0016_auto_20210419_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arshowcasescentermodel',
            name='showcase_uid',
            field=models.BigIntegerField(db_index=True, default=-1, unique=True, verbose_name='Showcase uid'),
        ),
    ]