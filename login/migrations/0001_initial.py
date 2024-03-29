# Generated by Django 2.2.5 on 2019-09-30 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import login.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('dept', models.CharField(choices=[('comp', 'Computer Engineering'), ('civil', 'Civil Engineering'), ('mech', 'Mechanical Engineering'), ('it', 'Information Technology Engineering'), ('e&tc', 'E&TC Engineering'), ('inst', 'Instrumental Engineering'), ('prod', 'Production Engineering')], max_length=50)),
                ('year', models.CharField(choices=[('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E')], max_length=3)),
                ('sem', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('dept', models.CharField(choices=[('comp', 'Computer Engineering'), ('civil', 'Civil Engineering'), ('mech', 'Mechanical Engineering'), ('it', 'Information Technology Engineering'), ('e&tc', 'E&TC Engineering'), ('inst', 'Instrumental Engineering'), ('prod', 'Production Engineering')], max_length=50)),
                ('year', models.CharField(choices=[('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E')], max_length=3)),
                ('sem', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('name', models.CharField(max_length=80, unique=True)),
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('email_id', models.CharField(max_length=50)),
                ('primary_phone_no', models.CharField(max_length=10)),
                ('secondary_phone_no', models.CharField(max_length=10)),
                ('cc', models.CharField(choices=[('None', 'None'), ('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E')], default='None', max_length=3)),
                ('subjects', djongo.models.fields.ArrayModelField(model_container=login.models.Subjects)),
                ('labs', djongo.models.fields.ArrayModelField(model_container=login.models.Labs)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('roll_no', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('comp', 'Computer Engineering'), ('civil', 'Civil Engineering'), ('mech', 'Mechanical Engineering'), ('it', 'Information Technology Engineering'), ('e&tc', 'E&TC Engineering'), ('inst', 'Instrumental Engineering'), ('prod', 'Production Engineering')], default='comp', max_length=10)),
                ('division', models.CharField(choices=[('A', 'A'), ('B', 'B')], max_length=2)),
                ('year', models.CharField(choices=[('F.E', 'F.E'), ('S.E', 'S.E'), ('T.E', 'T.E'), ('B.E', 'B.E')], default='fe', max_length=3)),
                ('batch', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4')], default='a1', max_length=2)),
                ('email_id', models.EmailField(max_length=100)),
                ('primary_phone_no', models.CharField(max_length=10)),
                ('parents_phone_no', models.CharField(max_length=10)),
                ('teacher_guardian', models.ForeignKey(on_delete=False, to='login.Teacher', to_field='name')),
            ],
        ),
    ]
