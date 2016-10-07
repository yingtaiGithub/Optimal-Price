# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import ListView, RedirectView, UpdateView,\
                                 TemplateView, View
from django.shortcuts import redirect
from braces.views import LoginRequiredMixin

from .models import User
from django.core.mail import EmailMultiAlternatives
from roojet.services.models import Product
from django.conf import settings


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_detail.html'

    def post(self, request, **kwargs):
        request.user.shop_name = ''
        request.user.shop_token = ''
        request.user.save()
        Product.objects.filter(
            created_by=request.user).delete()
        return redirect('core:dashboard')

    def get_context_data(self, **kwargs):
        context = {}
        context['object'] = self.request.user
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail")


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'email']
    template_name = 'users/user_form.html'

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail")

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class RemoveShopView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        return redirect('core:dashboard')

    def post(self, request, **kwargs):
        shopname = request.user.shop_name
        request.user.shop_name = ''
        request.user.shop_token = ''
        request.user.save()
        Product.objects.filter(
            created_by=request.user).delete()
        email = 'mavmcquin@gmail.com'
        subject, from_email, to = 'Roojet: Dashboard Uninstalled' ,  settings.DEFAULT_FROM_EMAIL, email
        text_content = 'Hello,\n %s has uninstalled shop %s from his Roojet dashboard ' %(request.user.username, shopname)
        html_content = '<p>Hello ,<p><br/><p>  %s has uninstalled shop %s from his  <strong>Roojet</strong>  dashboard </p><p>Regards,<br/>The Roojet Team,<br/>' %(request.user.username, shopname)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()        
        return redirect('core:dashboard')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
