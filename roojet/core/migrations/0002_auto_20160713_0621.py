# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='payment_token',
            field=models.CharField(default=b'', max_length=250),
        ),
        migrations.AddField(
            model_name='shop',
            name='plan',
            field=models.CharField(default=b'', max_length=250),
        ),
    ]
