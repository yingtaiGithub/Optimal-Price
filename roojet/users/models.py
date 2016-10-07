# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from plans.signals import activate_user_plan


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name"), blank=True, max_length=255)
    shop_name = models.SlugField(max_length=50, default='')
    shop_token = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail')


def user_signed_up_(sender, instance, created, **kwargs):
    """
    Whenever a user signs up, they should be added
    to the default plan.
    """
    activate_user_plan.send(sender=sender, user=instance)

signals.post_save.connect(user_signed_up_, sender=User, weak=False,
                          dispatch_uid='models.user_signed_up_')

#class Customer(models.Model):
    #user = models.ForeignKey(User)
    #customer = models.CharField(max_length=200, null=False, blank=False)
    
    #def __str__(self):
        #return self.user.username    