# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-31 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_products', '0020_auto_20170523_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='show_brand',
            field=models.BooleanField(default=True, verbose_name='Show brand (for menu)'),
        ),
    ]