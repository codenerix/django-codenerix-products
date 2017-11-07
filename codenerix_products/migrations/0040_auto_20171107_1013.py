# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-07 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_products', '0039_auto_20171103_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfinal',
            name='packing_cost',
            field=models.FloatField(blank=True, help_text='If it is empty, packing cost is equal to packing cost of product', null=True, verbose_name='Packing cost'),
        ),
        migrations.AddField(
            model_name='productfinal',
            name='weight',
            field=models.FloatField(blank=True, help_text='If it is empty, weight is equal to weight of product', null=True, verbose_name='Weight'),
        ),
    ]
