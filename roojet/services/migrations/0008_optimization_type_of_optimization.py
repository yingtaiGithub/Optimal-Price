# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20160107_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='optimization',
            name='type_of_optimization',
            field=models.CharField(default=b'revenue', max_length=7, choices=[(b'revenue', b'revenue'), (b'profit', b'profit')]),
        ),
    ]
