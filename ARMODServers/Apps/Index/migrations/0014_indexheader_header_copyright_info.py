# Generated by Django 3.2 on 2021-05-04 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0013_auto_20210504_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexheader',
            name='header_copyright_info',
            field=models.CharField(blank=True, default='', max_length=16, verbose_name='Header copryright info'),
        ),
    ]