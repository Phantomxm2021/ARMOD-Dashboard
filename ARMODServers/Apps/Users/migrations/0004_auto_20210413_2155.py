# Generated by Django 3.1.4 on 2021-04-13 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20210411_2148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Users', 'verbose_name_plural': 'Users'},
        ),
    ]