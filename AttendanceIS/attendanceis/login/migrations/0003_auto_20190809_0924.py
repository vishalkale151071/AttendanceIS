# Generated by Django 2.2.4 on 2019-08-09 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20190808_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='cc',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='tg',
            field=models.BooleanField(default=False),
        ),
    ]
