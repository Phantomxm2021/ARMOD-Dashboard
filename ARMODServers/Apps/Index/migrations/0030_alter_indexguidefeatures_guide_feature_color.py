# Generated by Django 3.2 on 2022-02-15 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0029_indexguidefeatures_guide_feature_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexguidefeatures',
            name='guide_feature_color',
            field=models.CharField(default='', max_length=32, verbose_name='guide feature color'),
        ),
    ]