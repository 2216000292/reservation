# Generated by Django 3.2.14 on 2022-11-25 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dinning',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=20, verbose_name='customer')),
                ('date', models.DateField(verbose_name='orderdate')),
                ('title', models.CharField(default='default', max_length=20, verbose_name='title')),
                ('state', models.CharField(default='empty', max_length=20, verbose_name='state')),
            ],
        ),
        migrations.CreateModel(
            name='TableInforamtion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='number')),
                ('date', models.DateField(verbose_name='orderdate')),
                ('customer', models.CharField(default='default', max_length=20, verbose_name='customer')),
                ('state', models.CharField(default='empty', max_length=20, verbose_name='customer')),
                ('table_id', models.IntegerField(default=0, verbose_name='tableId')),
            ],
        ),
        migrations.CreateModel(
            name='TableOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=20, verbose_name='customer')),
                ('price', models.FloatField(default=0.0, verbose_name='shopPrice')),
                ('number', models.IntegerField(verbose_name='number')),
                ('date', models.DateField(verbose_name='orderdate')),
                ('reser_date', models.DateField(verbose_name='reservation_date')),
                ('introduce', models.CharField(default='default', max_length=256, verbose_name='introduce')),
                ('table_ids', models.CharField(default='', max_length=256, verbose_name='table_ids')),
            ],
            options={
                'verbose_name': 'TableOrder',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256, unique=True, verbose_name='username')),
                ('password', models.CharField(default='', max_length=256, verbose_name='password')),
                ('name', models.CharField(max_length=256, verbose_name='Name')),
                ('mailling_address', models.CharField(max_length=256, verbose_name='mailling_address')),
                ('billing_address', models.CharField(max_length=256, verbose_name='billing_address')),
                ('preferred_diner', models.CharField(max_length=256, verbose_name='preferred_diner')),
                ('earned_points', models.FloatField(default=0.0)),
                ('preferred_payment_method', models.CharField(choices=[('cash', 'cash'), ('credit', 'credit'), ('check', 'check')], max_length=256, verbose_name='preferred_payment_method')),
            ],
            options={
                'verbose_name': 'UserInfo',
            },
        ),
    ]