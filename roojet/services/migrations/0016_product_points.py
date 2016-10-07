# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_product_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
