# Generated by Django 2.2.4 on 2019-08-08 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='cc',
            field=models.CharField(default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='tg',
            field=models.CharField(default='1', max_length=1),
        ),
    ]
