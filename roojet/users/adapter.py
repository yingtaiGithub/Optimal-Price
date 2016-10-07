from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import get_adapter as get_account_adapter, DefaultAccountAdapter
from allauth.account.utils import get_login_redirect_url
from django.shortcuts import redirect
from django.contrib.auth import login as django_login
from django.http import HttpResponseRedirect
from roojet.mailerlite import api

from plans.models import *

class AccountAdapter(DefaultAccountAdapter):
     
     def get_login_redirect_url(self, request):
          user = request.user
          plan_price = request.POST.get('plan','')
          try:
               api_obj = api.Api(api_key='5032e1f6e3115b11282511b328b2f197')
               new_subscriber = api_obj.subscribe(
                                 list_id=2981205,
                                 email=user.email,
                                 name=user.name,
                                 fields=None,
                                 resubscribe=0
                             ) 
               
          except:
               new_subscriber = None
          if plan_price:
               plans = {'Roojet Bronze':'29','Roojet Silver':'79','Roojet Gold':'179'}
               
               plan_id = plan_price.split('/')[4]
               plan_price = PlanPricing.objects.get(id=plan_id)
               price = plans[plan_price.plan.name]
               order_obj = Order(user=request.user, plan=plan_price.plan,amount=price,currency="USD", pricing=plan_price.pricing)
               order_obj.save()
               redirect_url = '/order/%s/' %(order_obj.id)
               return redirect_url
          else:
               return '/board/'
          
     