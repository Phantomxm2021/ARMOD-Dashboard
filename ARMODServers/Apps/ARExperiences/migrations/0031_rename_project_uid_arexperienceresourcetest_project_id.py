# Generated by Django 3.2 on 2022-02-03 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ARExperiences', '0030_auto_20220203_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arexperienceresourcetest',
            old_name='project_uid',
            new_name='project_id',
        ),
    ]
