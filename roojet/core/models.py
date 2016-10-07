from django.db import models
from django.conf import settings

class Shop(models.Model):
    name = models.CharField(max_length=250, default='')
    token = models.CharField(max_length=250, default='')
    installed_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    plan = models.CharField(max_length=250, default='')
    payment_token = models.CharField(max_length=250, default='')
    payment_date = models.DateField(blank=True, null=True)
    expire_date = models.DateField(blank=True, null=True)