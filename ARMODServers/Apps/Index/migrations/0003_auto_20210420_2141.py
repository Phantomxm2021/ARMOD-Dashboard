# Generated by Django 3.1.4 on 2021-04-20 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Index', '0002_indexpageviewkeybenfitsmodel_sort_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPageQAModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('sort_id', models.IntegerField(db_index=True, default=0, verbose_name='QA sort id')),
                ('qa_title', models.CharField(default='', max_length=64, unique=True, verbose_name='QA title')),
                ('qa_description', models.CharField(default='', max_length=1024, verbose_name='QA description')),
            ],
            options={
                'verbose_name': 'qas',
                'verbose_name_plural': 'qas',
                'db_table': 'armod_index_qa',
            },
        ),
        migrations.AlterModelOptions(
            name='indexpageviewkeybenfitsmodel',
            options={'verbose_name': 'Index Keybenfits', 'verbose_name_plural': 'Index Keybenfits'},
        ),
        migrations.AddField(
            model_name='indexpageviewkeybenfitsmodel',
            name='keybenfit_video_url',
            field=models.CharField(default='', max_length=256, verbose_name='Key benfit video url'),
        ),
        migrations.AlterField(
            model_name='indexpageviewkeybenfitsmodel',
            name='sort_id',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Key benfit sort id'),
        ),
        migrations.AlterModelTable(
            name='indexpageviewkeybenfitsmodel',
            table='armod_index_key_benfits',
        ),
    ]