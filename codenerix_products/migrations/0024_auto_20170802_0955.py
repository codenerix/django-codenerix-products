# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-02 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_products', '0023_pack_packoption_packoptiontexten_packoptiontextes_packtexten_packtextes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='code',
            field=models.CharField(max_length=250, unique=True, verbose_name='Code'),
        ),
    ]