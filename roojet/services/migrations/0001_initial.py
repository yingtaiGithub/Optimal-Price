# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Optimization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('optimized_price', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shopify_product_id', models.IntegerField(default=0)),
                ('shopify_variant_id', models.IntegerField(default=0)),
                ('title', models.CharField(default=b'', max_length=250)),
                ('created_at_shopify', models.DateTimeField()),
                ('updated_at_shopify', models.DateTimeField()),
                ('actual_shopify_price', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
        ),
        migrations.AddField(
            model_name='optimization',
            name='Product',
            field=models.ForeignKey(to='services.Product'),
        ),
    ]
