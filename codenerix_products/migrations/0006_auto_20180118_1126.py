# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-18 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_products', '0005_auto_20180118_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brandtexten',
            name='name',
            field=models.CharField(default='test', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brandtextes',
            name='name',
            field=models.CharField(default='test', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productfinaltexten',
            name='name',
            field=models.CharField(default='test', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productfinaltextes',
            name='name',
            field=models.CharField(default='test', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producttexttexten',
            name='name',
            field=models.CharField(default='test', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producttexttextes',
            name='name',
            field=models.CharField(default='test', max_length=250, verbose_name='Name'),
            preserve_default=False,
        ),
    ]
