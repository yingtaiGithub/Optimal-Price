# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_historic'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='visits',
            field=models.IntegerField(default=0),
        ),
    ]
