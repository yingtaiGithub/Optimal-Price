# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_product_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='recently_optimized',
            field=models.BooleanField(default=False),
        ),
    ]
