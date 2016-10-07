# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_optimization_type_of_optimization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optimization',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='optimization',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
