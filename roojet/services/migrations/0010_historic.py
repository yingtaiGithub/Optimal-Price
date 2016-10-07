# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20160108_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=12, decimal_places=2)),
                ('quantity', models.IntegerField(default=0)),
                ('total', models.DecimalField(max_digits=12, decimal_places=2)),
                ('date', models.DateField()),
                ('Product', models.ForeignKey(to='services.Product')),
            ],
        ),
    ]
