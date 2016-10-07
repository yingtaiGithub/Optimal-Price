# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_product_original_shopify_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 19, 36, 22, 791833), auto_now_add=True),
            preserve_default=False,
        ),
    ]
