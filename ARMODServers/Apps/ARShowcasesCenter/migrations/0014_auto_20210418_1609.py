# Generated by Django 3.1.4 on 2021-04-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARShowcasesCenter', '0013_auto_20210418_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arshowcasescentermodel',
            name='showcase_status',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Showcase status'),
        ),
    ]