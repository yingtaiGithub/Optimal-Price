# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url, patterns

from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
import importlib
payment_roojet = importlib.import_module('roojet.payment_roojet.views')
core_roojet = importlib.import_module('roojet.core.views')

urlpatterns = [
    url(r'^', include('roojet.core.urls', namespace='core')),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^$', core_roojet.AddShopView.as_view(),
        name="home"),
    url(r'^order/(?P<pk>\d+)/$', payment_roojet.OrderView.as_view(),
        name='order'),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include("roojet.users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('plans.urls')),
    url(r'^payments/', include('payments.urls')),

    # Your stuff: custom urls includes go here


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('loginas.views',
                        url(r"^login/user/(?P<user_id>.+)/$", "user_login",
                            name="loginas-user-login"),
                        )

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request),
        url(r'^403/$', default_views.permission_denied),
        url(r'^404/$', default_views.page_not_found),
        url(r'^500/$', default_views.server_error),
    ]
