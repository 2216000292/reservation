# Generated by Django 3.2.14 on 2022-11-26 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0003_tableorder_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableinforamtion',
            name='date',
            field=models.DateField(verbose_name='order date'),
        ),
        migrations.AlterField(
            model_name='tableorder',
            name='date',
            field=models.DateField(verbose_name='order date'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='billing_address',
            field=models.CharField(max_length=256, verbose_name='billing address'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='mailling_address',
            field=models.CharField(max_length=256, verbose_name='mailling address'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='preferred_diner',
            field=models.CharField(max_length=256, verbose_name='preferred diner'),
        ),
    ]
