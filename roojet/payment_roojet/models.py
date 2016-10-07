from django.core.urlresolvers import reverse
from django.db import models
from payments.models import BasePayment

from plans.models import Order


class Payment(BasePayment):
    order = models.ForeignKey(Order)

    def get_failure_url(self):
        return reverse('order_payment_failure', kwargs={'pk': self.order.pk})

    def get_success_url(self):
        if self.order.status != 2:
            # Ensures that we process order only once
            self.order.status = Order.STATUS[1][0]
            self.order.complete_order()
        return reverse('order_payment_success', kwargs={'pk': self.order.pk})
