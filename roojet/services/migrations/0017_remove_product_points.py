# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0016_product_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='points',
        ),
    ]
