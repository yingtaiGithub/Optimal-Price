# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160713_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='expire_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='payment_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
