import stripe
import datetime
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, render
from payments import RedirectNeeded, get_payment_model
from plans.models import Order
from plans.views import OrderView as ParentOrderView
from plans.views import OrderPaymentReturnView as ParentReturnView
from roojet.mailerlite import api
#from roojet.users.models import Customer

class OrderView(ParentOrderView):
    model = Order
    template_name = 'plans/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        payment, created = get_payment_model().objects.get_or_create(
            order__pk=self.object.pk,
            defaults={
                    'variant': 'default',
                    'description': 'Plan Purchase',
                    'order': self.object,
                    'total': self.object.total(),
                    'tax': self.object.tax_total(),
                    'currency': self.object.currency
                })
        context['payment_form'] = payment.get_form()
        context['payment'] = payment
        return context

    def post(self, request, **kwargs):
        user = self.request.user
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        try:
            data =  self.request.POST.copy()
            stripe.api_key = " sk_live_V4Uj8MdAqwQgomKKSZfUddes"
            s_tokn = data.get('stripeToken','')
            plan_ids = {'Roojet Bronze':'010','Roojet Silver':'020','Roojet Gold':'030'}
            plan_id = plan_ids.get(self.object.plan.name,'')
            customer = stripe.Customer.create(
              source=s_tokn,
              plan=plan_id,
              email=user.email
            )   
            if customer:
                #customer_obj = Customer(user=request.user, customer=customer.id)
                #customer_obj.save()
                #customer.pgadmin.create(plan=plan_id)
                user.userplan.plan= self.object.plan
                user.userplan.active = True
                expire_date = datetime.datetime.today()+ datetime.timedelta(days=10)
                user.userplan.expire = expire_date
                user.userplan.save()
                api_obj = api.Api(api_key='5032e1f6e3115b11282511b328b2f197')
                try:
                    subscribe_obj = api_obj.delete_subscriber(2981205,user.email)
                except:
                    subscribe_obj = None
                new_subscriber = api_obj.subscribe(
                                list_id=3389361,
                                email=user.email,
                                name=user.name,
                                fields=None,
                                resubscribe=0
                            )                 
                messages.success(self.request,
                                _('Thank you for placing a payment. \
                                   It will be processed as soon as possible.'))                
                return redirect(reverse('core:dashboard'))
        except RedirectNeeded as redirect_to:
            return redirect(str(redirect_to))
        return render(request, self.template_name, context)


class OrderPaymentReturnView(ParentReturnView):
    """
    This view is a fallback from any payments processor. It allows just to set
    additional message context and redirect to Order view itself.
    """
    model = Order
    status = None

    def render_to_response(self, context, **response_kwargs):
        if self.status == 'success':
            messages.success(self.request,
                             _('Thank you for placing a payment. \
                                It will be processed as soon as possible.'))
        return redirect(reverse('core:dashboard'))


