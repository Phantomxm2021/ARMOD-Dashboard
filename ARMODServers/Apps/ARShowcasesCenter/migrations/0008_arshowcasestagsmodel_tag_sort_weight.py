# Generated by Django 3.1.6 on 2021-04-14 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARShowcasesCenter', '0007_auto_20210414_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='arshowcasestagsmodel',
            name='tag_sort_weight',
            field=models.IntegerField(db_index=True, default=-1, verbose_name='Sort weight'),
        ),
    ]
