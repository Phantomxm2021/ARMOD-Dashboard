# Generated by Django 3.1.6 on 2021-04-15 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPageViewKeyBenfitsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('keybenfit_title', models.CharField(default='', max_length=64, unique=True, verbose_name='Key benfit title')),
                ('keybenfit_description', models.CharField(default='', max_length=1024, verbose_name='Key benfit description')),
            ],
            options={
                'verbose_name': 'Keybenfits',
                'verbose_name_plural': 'Keybenfits',
                'db_table': 'armod_key_benfits',
            },
        ),
    ]