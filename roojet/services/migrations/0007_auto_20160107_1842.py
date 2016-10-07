# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_remove_product_recently_optimized'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optimization',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='optimization',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
