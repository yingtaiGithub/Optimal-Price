# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='shop_name',
            field=models.SlugField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='shop_token',
            field=models.CharField(default='', max_length=50),
        ),
    ]
