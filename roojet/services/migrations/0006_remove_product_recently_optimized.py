# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_product_recently_optimized'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='recently_optimized',
        ),
    ]
