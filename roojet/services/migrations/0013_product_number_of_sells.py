# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_product_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_of_sells',
            field=models.IntegerField(default=0),
        ),
    ]
