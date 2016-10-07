from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.views.generic import View
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from urlparse import urlparse
from roojet.users.models import User

from httmock import all_requests, HTTMock
from roojet.services.models import Product
from .utils import calculate_expected_improvement
from .views import ShopRequiredMixin, PlanRequiredMixin
import datetime
from decimal import Decimal
from plans.models import Plan


@all_requests
def moe_mock(url, request):
    return {'status_code': 200,
            'content': {}
            }

# Create your tests here.


# class TestCoreDashboardView(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='test', email='test@test.com', password='top_secret')
#         self.plan = Plan.objects.create(name='test.plan',
#                                         available=True)
#         self.user.userplan.plan = self.plan
#         self.user.userplan.save()
#         self.client.login(username=self.user.username, password='top_secret')

#     def test_dashboard_redirects_if_no_plan_found(self):
#         """
#         Dashboard View should redirect to the pricing page if
#         user has no active plan related to it
#         """
#         user = User.objects.create_user(username='test2',
#                                         email='test2@test.com',
#                                         password='password2')
#         client = Client()
#         client.login(username=user.username, password='password2')
#         response = client.get(reverse('core:dashboard'))
#         self.assertEquals(response.status_code, 302)
#         if user.shop_name and user.shop_token:
#             self.assertEquals(urlparse(response.url).
#                               path, reverse('pricing'))
#         else:
#             self.assertEquals(urlparse(response.url).
#                               path, reverse('core:add_shop'))

#     def test_dashboard_redirects_if_no_shop_found(self):
#         """
#         Dashboard view should redirect to the shop creation page
#         if user has not added a shop yet but it has a plan related
#         """
#         response = self.client.get(reverse('core:dashboard'))
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(urlparse(response.url).
#                           path, reverse('core:add_shop'))

#     def test_dashboard_redirects_to_login_if_anonymous_user(self):
#         """
#         Make sure that login is required to access dashboard view
#         """
#         response = Client().get(reverse('core:dashboard'))
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(urlparse(response.url).
#                           path, reverse('account_login'))

#     def test_dashboard_view_redirects_with_non_valid_api_values(self):
#         """
#         If user has assigned a shop already but the data is not valid,
#         it should,redirect to the add shop view
#         """
#         self.user.shop_name = 'test-5727'
#         self.user.shop_token = '123123'
#         self.user.save()
#         response = self.client.get(reverse('core:dashboard'))
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(urlparse(response.url).
#                           path, reverse('core:add_shop'))

#     def test_dashboard_redirects_if_shop_expired(self):
#         """
#         If the user's shop has expired,
#         dashboard will redirect and show a message
#         with the error
#         """
#         self.user.shop_name = 'swapps'
#         self.user.shop_token = '123123'
#         self.user.save()
#         response = self.client.get(reverse('core:dashboard'))
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(urlparse(response.url).
#                           path, reverse('core:add_shop'))

#     def test_dashboard_lists_products_with_valid_api_values(self):
#         """
#         If user has valid credentials and data can be retrieved,
#         this view should
#         return 200 and display a list of products
#         """
#         pass

#     def test_add_shop_redirects_to_login_if_anonymoous_user(self):
#         """
#         Make sure that login is required to access add shop view
#         """
#         response = Client().get(reverse('core:add_shop'))
#         self.assertEquals(response.status_code, 302)
#         response = Client().post(reverse('core:add_shop'),
#                                  {'shop_name': 'swapps'})
#         self.assertEquals(response.status_code, 302)

#     def test_valid_and_existent_shop_redirects(self):
#         """
#         shop_name should redirect to shopify site to request
#         authorization to the shop when the shop_name is valid
#         and the shop exists
#         """
#         response = self.client.post(reverse('core:add_shop'),
#                                     {'shop_name': 'swapps'})
#         self.assertEqual(response.status_code, 302)

#     def test_invalid_shop_name_dont_redirect(self):
#         """
#         shop_name should be a slug. If it is not, it should
#         add an error to the form and avoid redirecting to shopify
#         """
#         response = self.client.post(
#             reverse('core:add_shop'),
#             {'shop_name': 'some %!$@#! gibberish'})
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(response.context['form'].is_valid())

#     def test_non_existent_shop_dont_redirect(self):
#         """
#         shop_name should not redirect to an empty shop if it
#         is valid but the shop does not exist
#         """
#         response = self.client.post(
#             reverse('core:add_shop'),
#             {'shop_name': 'some-valid-but-inexistent-name-123456'})
#         self.assertEqual(response.status_code, 200)
#         self.assertFalse(response.context['form'].is_valid())

#     def test_state_is_being_saved_in_session(self):
#         """
#         Before redirecting to shopify, an state is send on the request
#         and persisted on session. It should be returned on the GET request
#         from shopify after the authorization step.
#         """
#         session = self.client.session
#         self.assertTrue(session.get('state', None) is None)
#         response = self.client.post(
#             reverse('core:add_shop'),
#             {'shop_name': 'swapps'})
#         session = self.client.session
#         self.assertTrue(session.get('state', None) is not None)

#     def test_shopify_api_fails_for_direct_access(self):
#         """
#         When returning from shopify site some verifications are
#         required. If any of those fail, app should raise 403 Forbidden
#         """
#         response = self.client.get(reverse('core:shopify_callback'))
#         self.assertEqual(response.status_code, 403)


# class TestProductExpectedImprovementView(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='test', email='test@test.com', password='top_secret',
#             shop_token=u'c47c5147904b7d515913f632915e0a23',
#             shop_name=u'test-5727')
#         self.plan = Plan.objects.create(name='test.plan',
#                                         available=True)
#         self.user.userplan.plan = self.plan
#         self.user.userplan.save()
#         self.product_id = '6427203012'
#         self.client.login(username=self.user.username, password='top_secret')
#         self.product = Product.objects.create(
#             created_by=self.user,
#             shopify_product_id='12345',
#             shopify_variant_id=self.product_id,
#             title='test_product',
#             created_at_shopify=datetime.datetime.now(),
#             updated_at_shopify=datetime.datetime.now(),
#             original_shopify_price=Decimal('10.00'),
#             actual_shopify_price=Decimal('10.00'))

#     def test_view_redirects_anonymous_users(self):
#         """
#         This view requires a shop,
#         which is associated with logged in users only
#         """
#         response = Client().get(
#             reverse('core:product_ei', kwargs={'product_id': self.product_id}))
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(
#             urlparse(response.url).path, reverse('account_login'))

#     def test_view_allows_valid_users(self):
#         """
#         View should allow only authenticated users and users that have a shop.
#         """
#         with HTTMock(moe_mock):
#             test_product = str(self.product.shopify_variant_id)
#             response = self.client.post(reverse(
#                 'core:optimized_price_results'),
#                 {'variable': 'revenue',
#                  test_product: 'Ok'})
#         self.assertEquals(response.status_code, 200)

#     def test_view_requires_shop(self):
#         """
#         View should redirect users that haven't setted an account
#         """
#         client = Client()
#         user = User.objects.create_user(
#             username='test2', email='test@test2.com', password='top_secret',
#             shop_token=u'', shop_name=u'')
#         self.client.login(username=user.username, password='top_secret')
#         response = self.client.get(
#             reverse('core:product_ei', kwargs={'product_id': self.product_id}))
#         self.assertEquals(response.status_code, 302)
#         response_url = urlparse(response.url)
#         self.assertEquals(response_url.path, reverse('core:add_shop'))


# class TestCalculateExpectedImprovement(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='test', email='test@test.com', password='top_secret',
#             shop_token=u'c47c5147904b7d515913f632915e0a23',
#             shop_name=u'test-5727')

#     def test_no_product_id_returns_none(self):
#         """
#         Product id is required to extract history from orders.
#         If it is not provided, method should fail with None values.
#         """
#         output, points = calculate_expected_improvement(self.user, '')
#         self.assertEquals(output, None)
#         self.assertEquals(points, None)


# class TestShopRequiredMixin(TestCase):

#     class SomeView(ShopRequiredMixin, View):

#         def get(self, request):
#             return HttpResponse('success')

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='test', email='test@test.com', password='top_secret')

#     def test_anonymous_user_redirects_login(self):
#         """
#         Mixin redirects to login if user is not authenticated
#         """
#         request = self.factory.get('/some-path/')
#         request.user = AnonymousUser()
#         response = self.SomeView.as_view()(request)
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(
#             urlparse(response.url).path, reverse('account_login'))

#     def test_authenticated_user_without_shop_redirects(self):
#         """
#         Users that are authenticated but do not have a shop
#         should redirect to the add_shop view to create the
#         connection
#         """
#         request = self.factory.get('/some-path/')
#         request.user = self.user
#         response = self.SomeView.as_view()(request)
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(urlparse(
#             response.url).path, reverse('core:add_shop'))

#     def test_authenticated_user_with_shop_success(self):
#         """
#         Users that comply with the 2 conditions should
#         be allowed to access the view.
#         """
#         request = self.factory.get('/some-path/')
#         self.user.shop_name = 'swapps'
#         self.user.shop_token = '123123'
#         request.user = self.user
#         response = self.SomeView.as_view()(request)
#         self.assertEquals(response.status_code, 200)


# class TestPlanRequiredMixin(TestCase):

#     class SomeView(PlanRequiredMixin, View):

#         def get(self, request):
#             return HttpResponse('success')

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='test', email='test@test.com', password='top_secret')

#     def test_anonymous_user_redirects_login(self):
#         """
#         Mixin redirects to login if user is not authenticated
#         """
#         request = self.factory.get('/some-path/')
#         request.user = AnonymousUser()
#         response = self.SomeView.as_view()(request)
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(
#             urlparse(response.url).path, reverse('account_login'))

#     def test_authenticated_user_without_plan_redirects(self):
#         """
#         Users that are authenticated but do not have a plan
#         should redirect to the pricing view to purchase a plan
#         """
#         request = self.factory.get('/some-path/')
#         request.user = self.user
#         response = self.SomeView.as_view()(request)
#         self.assertEquals(response.status_code, 302)
#         self.assertEquals(urlparse(
#             response.url).path, reverse('pricing'))

#     def test_authenticated_user_with_shop_success(self):
#         """
#         Users that comply with the 2 conditions should
#         be allowed to access the view.
#         """
#         self.plan = Plan.objects.create(name='test.plan',
#                                         available=True)
#         self.user.userplan.plan = self.plan
#         self.user.userplan.save()
#         request = self.factory.get('/some-path/')
#         self.user.shop_name = 'swapps'
#         self.user.shop_token = '123123'
#         request.user = self.user
#         response = self.SomeView.as_view()(request)
#         self.assertEquals(response.status_code, 200)
