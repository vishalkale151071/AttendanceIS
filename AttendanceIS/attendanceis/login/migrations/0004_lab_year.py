# Generated by Django 2.2.5 on 2019-09-24 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20190924_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='year',
            field=models.CharField(choices=[('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E')], default='T.E', max_length=3),
            preserve_default=False,
        ),
    ]
