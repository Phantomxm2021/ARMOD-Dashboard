# Generated by Django 3.2 on 2022-02-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARExperiences', '0028_remove_arexperienceresourcetest_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arexperienceresourcetest',
            name='arexperience_uid',
            field=models.BigIntegerField(db_index=True, null=True, unique=True, verbose_name='所属项目的Id'),
        ),
    ]
