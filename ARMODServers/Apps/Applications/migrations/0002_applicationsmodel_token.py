# Generated by Django 3.1.6 on 2021-04-08 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationsmodel',
            name='token',
            field=models.CharField(default='', max_length=128, verbose_name='应用用Token'),
        ),
    ]