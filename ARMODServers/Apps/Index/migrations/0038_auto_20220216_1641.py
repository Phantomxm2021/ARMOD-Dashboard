# Generated by Django 3.2 on 2022-02-16 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0037_alter_indexpageviewkeybenfitsmodel_keybenfit_tags'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='indexheader',
            table='armod_index_header',
        ),
        migrations.AlterModelTable(
            name='indexsocialnavbar',
            table='armod_index_social_navbar',
        ),
    ]
