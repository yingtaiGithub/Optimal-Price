# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='actual_shopify_price',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
