# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20160107_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shopify_product_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='shopify_variant_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
