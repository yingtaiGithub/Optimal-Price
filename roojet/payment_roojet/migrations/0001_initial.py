# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0002_auto_20151111_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('variant', models.CharField(max_length=255)),
                ('status', models.CharField(default='waiting', max_length=10, choices=[('waiting', 'Waiting for confirmation'), ('preauth', 'Pre-authorized'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('refunded', 'Refunded'), ('error', 'Error'), ('input', 'Input')])),
                ('fraud_status', models.CharField(default='unknown', max_length=10, verbose_name='fraud check', choices=[('unknown', 'Unknown'), ('accept', 'Passed'), ('reject', 'Rejected'), ('review', 'Review')])),
                ('fraud_message', models.TextField(default='', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=255, blank=True)),
                ('currency', models.CharField(max_length=10)),
                ('total', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('delivery', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('tax', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('description', models.TextField(default='', blank=True)),
                ('billing_first_name', models.CharField(max_length=256, blank=True)),
                ('billing_last_name', models.CharField(max_length=256, blank=True)),
                ('billing_address_1', models.CharField(max_length=256, blank=True)),
                ('billing_address_2', models.CharField(max_length=256, blank=True)),
                ('billing_city', models.CharField(max_length=256, blank=True)),
                ('billing_postcode', models.CharField(max_length=256, blank=True)),
                ('billing_country_code', models.CharField(max_length=2, blank=True)),
                ('billing_country_area', models.CharField(max_length=256, blank=True)),
                ('billing_email', models.EmailField(max_length=254, blank=True)),
                ('customer_ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('extra_data', models.TextField(default='', blank=True)),
                ('message', models.TextField(default='', blank=True)),
                ('token', models.CharField(default='', max_length=36, blank=True)),
                ('captured_amount', models.DecimalField(default='0.0', max_digits=9, decimal_places=2)),
                ('order', models.ForeignKey(to='plans.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
