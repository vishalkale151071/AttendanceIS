# Generated by Django 2.2.6 on 2019-10-12 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='department',
            field=models.CharField(choices=[('comp', 'Computer Engineering'), ('civil', 'Civil Engineering'), ('mech', 'Mechanical Engineering'), ('it', 'Information Technology Engineering'), ('e&tc', 'E&TC Engineering'), ('inst', 'Instrumental Engineering'), ('prod', 'Production Engineering')], default='comp', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='cc',
            field=models.CharField(choices=[('N/A', 'N/A'), ('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E')], default='None', max_length=3),
        ),
    ]
