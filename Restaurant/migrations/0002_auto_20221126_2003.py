# Generated by Django 3.2.14 on 2022-11-26 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinning',
            name='select_time_period',
            field=models.CharField(choices=[('9:00-11:00', '1'), ('11:00-13:00', '2'), ('15:00-17:00', '3'), ('17:00-19:00', '4'), ('19:00-21:00', '5'), ('21:00-23:00', '6')], default='1', max_length=20, verbose_name='select_time_period'),
        ),
        migrations.AddField(
            model_name='tableinforamtion',
            name='select_time_period',
            field=models.CharField(choices=[('9:00-11:00', '1'), ('11:00-13:00', '2'), ('15:00-17:00', '3'), ('17:00-19:00', '4'), ('19:00-21:00', '5'), ('21:00-23:00', '6')], default='1', max_length=20, verbose_name='select_time_period'),
        ),
        migrations.AddField(
            model_name='tableorder',
            name='select_time_period',
            field=models.CharField(choices=[('9:00-11:00', '1'), ('11:00-13:00', '2'), ('15:00-17:00', '3'), ('17:00-19:00', '4'), ('19:00-21:00', '5'), ('21:00-23:00', '6')], default='1', max_length=20, verbose_name='select_time_period'),
        ),
        migrations.AlterField(
            model_name='tableinforamtion',
            name='state',
            field=models.CharField(default='empty', max_length=20, verbose_name='state'),
        ),
    ]
