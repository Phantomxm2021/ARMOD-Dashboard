# Generated by Django 3.2 on 2022-02-15 15:27

import Apps.Index.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0034_indexpageqamodel_qa_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexnavbar',
            name='navbar_subs',
            field=models.JSONField(blank=True, default=Apps.Index.models.getJSONFieldDefault, verbose_name='Navbar subs'),
        ),
    ]