# Generated by Django 3.1.6 on 2021-04-13 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ARShowcasesCenterModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('app_uid', models.IntegerField(db_index=True, default=-1, unique=True, verbose_name='App uid')),
                ('user_uid', models.IntegerField(db_index=True, default=-1, verbose_name='User uid')),
                ('arexperience_uid', models.IntegerField(db_index=True, default=-1, verbose_name='ARExperience uid')),
                ('showcase_uid', models.IntegerField(db_index=True, default=-1, unique=True, verbose_name='Showcase uid')),
                ('showcase_name', models.CharField(default='', max_length=64, unique=True, verbose_name='Showcase name')),
                ('showcase_status', models.IntegerField(default=1, verbose_name='Showcase status')),
                ('showcase_icon', models.CharField(default='', max_length=128, verbose_name='Showcase icon')),
                ('showcase_header', models.CharField(default='', max_length=128, verbose_name='Showcase header')),
                ('showcase_preview', models.CharField(default='', max_length=1024, verbose_name='Showcase previews(json)')),
                ('showcase_description', models.CharField(default='', max_length=1024, verbose_name='Showcase description')),
                ('showcase_tags', models.CharField(default='', max_length=512, verbose_name='Showcase tags')),
            ],
            options={
                'verbose_name': 'Showcases',
                'verbose_name_plural': 'Showcases',
                'db_table': 'armod_showcases_center',
            },
        ),
        migrations.CreateModel(
            name='ARShowcasesCenterTagsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('showcase_uid', models.IntegerField(db_index=True, default=-1, verbose_name='Showcases uid')),
                ('tag_name', models.CharField(db_index=True, default='', max_length=16, unique=True, verbose_name='Tag name')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]