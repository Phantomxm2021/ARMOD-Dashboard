# Generated by Django 3.2 on 2021-05-03 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0010_indexnavbar_navbar_subs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexnavbar',
            name='navbar_subs',
            field=models.JSONField(default=[], verbose_name='Navbar subs'),
        ),
    ]
