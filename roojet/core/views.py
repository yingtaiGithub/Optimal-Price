import re
import json
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib import messages
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
import uuid
import requests
import shopify
from django.core import serializers
from pyactiveresource.connection import UnauthorizedAccess, ClientError, \
        ServerError
from roojet.services.utils import normalize_products, get_historic
from .forms import ShopForm
from .utils import calculate_expected_improvement, \
        calculate_expected_improvement_list, update_shopify_price,\
        activate_shopify_session, get_increased_profit
from plans.models import *
from models import Shop
from roojet.services.models import Product, Optimization, Historic


class ShopRequiredMixin(UserPassesTestMixin):
    user_is_authenticated = False

    def test_func(self, user):
        if user.is_authenticated():
            self.user_is_authenticated = True
            return (user.shop_name != '' and user.shop_token != '')
        else:
            return False

    def no_permissions_fail(self, request=None):
        if self.user_is_authenticated:
            return redirect(reverse('core:add_shop'))
        else:
            return redirect('account_login')


class PlanRequiredMixin(UserPassesTestMixin):
    user_is_authenticated = False
    def test_func(self, user):
        if user.is_authenticated():
            self.user_is_authenticated = True
            return (user.userplan.plan is not None)
        else:
            return False

    def no_permissions_fail(self, request=None):
        if self.user_is_authenticated:
            return redirect('pricing')
        else:
            return redirect('account_login')

class WelcomeView(View):
    template_name = 'core/welcome.html'
    model = Shop
    def get(self, request):
        if request.GET.get('shop', '') == '':
            shop_name = request.session.get("shop_name")
        else:
            shop_name = request.GET.get('shop')

        shop = Shop.objects.get(
            name=shop_name)
        if shop.payment_token == '':
            return redirect("pricing")

        request.session['shop_name'] = shop.name
        request.session['shop_token'] = shop.token
        request.session["api_key"] = settings.SHOPIFY_API_KEY
        activate_shopify_session(request)
        return render(request, self.template_name)

class FaqView(View):
    template_name = 'core/faq.html'
    model = Shop
    def get(self, request):
        if request.GET.get('shop', '') == '':
            shop_name = request.session.get("shop_name")
        else:
            shop_name = request.GET.get('shop')

        shop = Shop.objects.get(
            name=shop_name)
        if shop.payment_token == '':
            return redirect("pricing")

        request.session['shop_name'] = shop.name
        request.session['shop_token'] = shop.token
        request.session["api_key"] = settings.SHOPIFY_API_KEY
        activate_shopify_session(request)
        return render(request, self.template_name)

class DashboardView(View):
    template_name = 'core/dashboard.html'
    model = Shop
    def get(self, request):

        if request.GET.get('shop', '') == '':
            shop_name = request.session.get("shop_name")
        else:
            shop_name = request.GET.get('shop')

        shop = Shop.objects.get(
            name=shop_name)
        if shop.payment_token == '':
            return redirect("pricing")

        request.session['shop_name'] = shop.name
        request.session['shop_token'] = shop.token
        request.session["api_key"] = settings.SHOPIFY_API_KEY
        activate_shopify_session(request)

        try:
            orders = [shopify.Order.find()]
        except UnauthorizedAccess:
            return redirect(reverse('core:add_shop'))
        except ClientError:
            messages.add_message(
                request,
                messages.ERROR,
                'The shop exists but it is not reachable at the moment. Please \
                verify your shopify account.')
            return redirect(reverse('core:add_shop'))
        #orders = []
        host = request.get_host()
        products, max_product_reached = normalize_products(request, host)
        #orders = []
        if not products:
            messages.add_message(
                request,
                messages.ERROR,
                'Apparently you have no products in your shop at Shopify. Please \
                        add a product before using Roojet.')
            return redirect(reverse('core:add_shop'))
        elif products == 'ServerError':
            messages.add_message(
                request,
                messages.ERROR,
                'Shopify is not reachable at the moment. Please \
                        try again later.')
        for product in products:
            try:
                get_historic(
                    shop=shop,
                    orders=orders,
                    product_id=product.shopify_variant_id)
            except:
                pass
                #messages.add_message(
                               #request,
                               #messages.ERROR,
                               #'You are missing shopify variant id for your product, Please \
                                       #update your product before using Roojet.')                
        objects_to_serialize = Historic.objects.filter(
            Product__created_by=shop).order_by('date')
        try:
            total_profit, profit_margin = get_increased_profit(
                products=products,
                historic=objects_to_serialize)
            historic = serializers.serialize("json", objects_to_serialize)
            products_serialized = serializers.serialize(
                "json", products, fields=('pk', 'title'))
        except:
            products_serialized = None
            historic = None
            total_profit = 0
            profit_margin =0
                         
        try:
            shop = shopify.Shop.current()
        except ServerError:
            messages.add_message(
                request,
                messages.ERROR,
                'The shop exists but it is not reachable at the moment. Please \
                verify your shopify account.')
            shop = ''
        
        enough_data = settings.ENOUGH_DATA
        context = {
            'historic': historic,
            'shop': shop,
            'orders': orders,
            'products': products,
            'products_serialized': products_serialized,
            'total_profit': abs(total_profit),
            'profit_margin': profit_margin,
            'enough_data': enough_data,
            'max_product_reached': max_product_reached,
        }
        return render(request, self.template_name, context)


class ProductExpectedImprovementView(ShopRequiredMixin, View):
    template_name = 'core/expected_improvement.html'

    def get(self, request, **kwargs):
        activate_shopify_session(request)
        try:
            orders = shopify.Order.find()
        except UnauthorizedAccess:
            return redirect(reverse('core:add_shop'))
        except ClientError:
            messages.add_message(
                request,
                messages.ERROR,
                'The shop exists but it is not reachable at the moment. Please \
                verify your shopify account.')
            return redirect(reverse('core:add_shop'))
        points, recommended_price = calculate_expected_improvement(
            orders,
            kwargs.get('product_id', None), variable='profit')
        #  calculate_expected_improvement_list(orders)

        context = {
            'points': points,
            'recommended_price': recommended_price,
        }
        return render(request, self.template_name, context)


class RemoveShopView(View):
    def post(self, request):   
        received_json_data = json.loads(request.body.decode("utf-8")) 
        shop = Shop.objects.get(name=received_json_data.get("myshopify_domain"))
        Product.objects.filter(created_by=shop).delete()
        shop.delete()
        email = 'mavmcquin@gmail.com'
        subject, from_email, to = 'Roojet: App Uninstalled' ,  settings.DEFAULT_FROM_EMAIL, email
        text_content = 'Hello,\n Roojet App has been uninstalled from shop %s ' %(received_json_data.get("myshopify_domain"))
        html_content = '<p>Hello ,<p><br/><p>   <strong>Roojet</strong> App has been uninstalled from shop  %s </p><p>Regards,<br/>The Roojet Team,<br/>' %(received_json_data.get("myshopify_domain"))
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()        
        return HttpResponse(status=200)

class AddShopView(TemplateView):
    template_name = 'core/add_shop.html'

    def get(self, request, **kwargs):
        shop = request.GET.get('shop', '')
        if shop != '':
            request.session['shop_name'] = shop
            shop_obj = Shop.objects.filter(name=shop)
            if shop_obj:
                return redirect(reverse('core:dashboard'))

            state = str(uuid.uuid4())
            session = shopify.Session(
                'https://%s.%s%s' % (shop,
                                     settings.SHOPIFY_URL,
                                     settings.SHOPIFY_AUTHORIZE_SUFIX))

            session.setup(
                api_key=settings.SHOPIFY_API_KEY,
                secret=settings.SHOPIFY_SECRET)
            permission_url = session.create_permission_url(
                settings.SHOPIFY_SCOPES,
                request.build_absolute_uri(
                    reverse('core:shopify_callback')))+'&state='+state

            try:
                response = requests.head(permission_url)
                if response.status_code == 404:
                    return HttpResponseForbidden()
                else:
                    request.session['state'] = state
                    return redirect(permission_url)
            except Exception:
                return HttpResponseForbidden()
            return render(request, self.template_name, context)
        else:
            return HttpResponseForbidden()


class ShopifyCallbackView(View):
    template_name = "core/shopify_callback.html"
    model = Shop
    def get(self, request):
        state = request.GET.get('state', None)
        session_state = request.session.get('state', None)
        if not state or not session_state or state != session_state:
            return HttpResponseForbidden()
        params = {
            'shop': request.GET.get('shop', None),
            'code': request.GET.get('code', None),
            'timestamp': request.GET.get('timestamp', None),
            'signature': request.GET.get('signature', None),
            'state': request.GET.get('state', None),
            'hmac': request.GET.get('hmac', None),
        }
        session = shopify.Session(
            'https://%s.%s%s' % (request.GET.get('shop', None),
                                 settings.SHOPIFY_URL,
                                 settings.SHOPIFY_AUTHORIZE_SUFIX))

        session.setup(
            api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_SECRET)
        try:
            token = session.request_token(params)
        except shopify.ValidationException:
            return HttpResponseForbidden()
        context = {}
        context["shop"] = request.GET.get('shop', None)
        context["api_key"] = settings.SHOPIFY_API_KEY

        shop = Shop.objects.filter(name=context["shop"])
        request.session['shop_name'] = request.GET.get('shop', None)
        request.session['shop_token'] = token
        if not shop:
            shop_obj = Shop(name=context["shop"],token=token)
            shop_obj.save()
            activate_shopify_session(request)
            webhook = shopify.Webhook()
            webhook.topic = "app/uninstalled"
            webhook.address = "https://app.roojet.com/uninstall/"
            webhook.format = "json"
            success = webhook.save()

        return render(request, self.template_name, context)


class OptimizedPriceResultsView(View):
    template_name = "core/optimized_price_results.html"

    def get(self, request):

        if request.GET.get('shop', '') == '':
            shop_name = request.session.get("shop_name")
        else:
            shop_name = request.GET.get('shop')

        shop = Shop.objects.get(
            name=shop_name)
        if shop.token == '' or shop.name == '':
            messages.add_message(request, messages.ERROR, 'You need to add a \
                    shop before accesing the dashboard.')
            return redirect(reverse('core:add_shop'))

        if shop.payment_token == '':
            messages.add_message(request, messages.INFO, 'You need to subscribe \
                to acess dashboard')
            return redirect("pricing")

        result = request.GET.get('product', None)
        variable = request.GET.get('optimization', None)
        if result is None or variable is None:
            return redirect('core:dashboard')
        activate_shopify_session(request)
        try:
            orders = shopify.Order.find()
        except UnauthorizedAccess:
            return redirect(reverse('core:add_shop'))
        product = get_object_or_404(Product, shopify_variant_id=int(result))
        calculate_expected_improvement_list(shop, orders,
                                            [product.shopify_variant_id],
                                            variable)
        context = {}
        context['optimized_products'] = []

        opti = Optimization.objects.filter(
                Product__shopify_variant_id=product.shopify_variant_id,
                Product__created_by=shop).latest('updated')
        context['optimized_products'] += [opti]

        return render(request, self.template_name, context)

    def post(self, request):
        shop = Shop.objects.get(
            name=request.session.get("shop_name"))

        variable = request.POST.get('variable', None)
        if variable is None:
            return redirect(reverse('core:dashboard'))
        activate_shopify_session(request)
        try:
            orders = shopify.Order.find()
        except UnauthorizedAccess:
            return redirect(reverse('core:add_shop'))
        products = Product.objects.filter(created_by=shop)
        product_ids = []
        for product in products:
            result = request.POST.get(str(product.shopify_variant_id), None)
            if result == 'Ok':
                product_ids.append(product.shopify_variant_id)
        calculate_expected_improvement_list(shop, orders,
                                            product_ids, variable)

        if product_ids == []:
            return redirect(reverse('core:dashboard'))
        context = {}
        context['optimized_products'] = []
        for product in product_ids:
            opti = Optimization.objects.filter(
                Product__shopify_variant_id=product,
                Product__created_by=shop).latest('updated')
            context['optimized_products'] += [opti]

        return render(request, self.template_name, context)


class UpdateProductsView(View):

    def get(self, request):
        return redirect('core:dashboard')

    def post(self, request):
        if request.GET.get('shop', '') == '':
            shop_name = request.session.get("shop_name")
        else:
            shop_name = request.GET.get('shop')

        shop = Shop.objects.get(
            name=shop_name)
        if shop.token == '' or shop.name == '':
            messages.add_message(request, messages.ERROR, 'You need to add a \
                    shop before accesing the dashboard.')
            return redirect(reverse('core:add_shop'))

        if shop.payment_token == '':
            messages.add_message(request, messages.INFO, 'You need to subscribe \
                to acess dashboard')
            return redirect("pricing")

        products = Product.objects.filter(created_by=shop)
        for product in products:
            result = request.POST.get(str(product.shopify_variant_id), None)
            if result == 'Ok':
                opti = Optimization.objects.filter(
                    Product__shopify_variant_id=product.shopify_variant_id,
                    Product__created_by=shop).latest('updated')
                update_status = update_shopify_price(
                    shop=shop,
                    price=opti.optimized_price,
                    variant_id=product.shopify_variant_id)
                if update_status == 'ForbiddenAccess':
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Apparently your shop do not allow to be modified by us. Please \
                        readd it and accept the conditions once again \
                        to use our application.')
                    return redirect('core:add_shop')
                if update_status is False:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Shopify is not reachable at the moment. Please \
                        try again later.')
                    return redirect('core:dashboard')
        messages.add_message(
            request,
            messages.SUCCESS,
            'Your products have been updated')
        return redirect('core:dashboard')


class TrackingPixelView(View):

    def get(self, request):
        data = {}
        variant_id = request.GET.get('variant_id', None)
        product_id = request.GET.get('product_id', None)
        if variant_id is not None:
            try:
                products = Product.objects.filter(
                    shopify_variant_id=variant_id)
                for product in products:
                    product.visits += 1
                    product.save()
            except:
                pass
        if product_id is not None:
            product_id = re.sub("[^0-9^.]", "", product_id)
            products = Product.objects.filter(
                shopify_product_id=int(product_id))
            for product in products:
                product.visits += 1
                product.save()
            data = {'message':'success'}
        return HttpResponse(json.dumps(data), content_type='application/json')


class AddCostView(View):

    def post(self, request, *args, **kwargs):
        cost = request.POST.get('cost', None)
        shop = Shop.objects.get(
            name=self.request.session.get('shop_name'))
        obj = get_object_or_404(Product,
                                shopify_variant_id=self.kwargs['shopify_variant_id'],
                                created_by=shop.id)

        obj.cost = cost
        obj.save()
        return HttpResponse(json.dumps({'message':'success'}), content_type='application/json')




class CreateOrderPlan(View):
    model = Order
    
    def get(self, request, *args, **kwargs):
        plan_id = self.kwargs.get('pk')
        plan_price = get_object_or_404(PlanPricing.objects.all().select_related('plan', 'pricing'),
                                              Q(pk=self.kwargs['pk']) & Q(plan__available=True) & (
                                                  Q(plan__customized=self.request.user) | Q(
                                                      plan__customized__isnull=True)))
        plans = {'Roojet Bronze':'29','Roojet Silver':'79','Roojet Gold':'179'}
        order_obj = Order(user=self.request.user, plan=plan_price.plan,amount=plans[plan_price.plan.name],currency="USD", pricing=plan_price.pricing)
        order_obj.save()
        redirect_url = '/order/%s/' %(order_obj.id)        
        return redirect(redirect_url)


class PriceUpdatesView(View):

    def post(self, request, *args, **kwargs):
        result = request.POST.get('product', None)
        variable = request.POST.get('optimization', None)
        shop = Shop.objects.get(
            name=self.request.session.get('shop_name'))
        if result is None or variable is None:
            return redirect('core:dashboard')
        activate_shopify_session(request)
        try:
             orders = shopify.Order.find()
        except UnauthorizedAccess:
             return redirect(reverse('core:add_shop'))
        product = get_object_or_404(Product, shopify_variant_id=int(result))
        #calculate_expected_improvement_list(shop, orders,
                                            #[product.shopify_variant_id],
                                            #variable)
        opti = Optimization.objects.filter(
                    Product__shopify_variant_id=product.shopify_variant_id,
                    Product__created_by=shop).latest('updated')
        update_status = update_shopify_price(
                    shop=shop,
                    price=opti.optimized_price,
                    variant_id=product.shopify_variant_id)
        price = opti.optimized_price
        if update_status == 'ForbiddenAccess':
            messages.add_message(
                request,
                messages.ERROR,
                'Apparently your shop do not allow to be modified by us. Please \
                readd it and accept the conditions once again \
                to use our application.')
            return redirect('core:add_shop')
        elif update_status is False:
            #messages.add_message(
                #request,
                #messages.ERROR,
                #'Shopify is not reachable at the moment. Please \
                #try again later.')
            message = 'Shopify is not reachable at the moment. Please \
                try again later.'
            message_tag = 'error'
            opti_price = '$ %s' %(float(opti.optimized_price))
            actual_price = '$ %s' %(float(product.actual_shopify_price))
            #return redirect('core:dashboard')
        else:
            #messages.add_message(
                #request,
                #messages.SUCCESS,
                #'Your products have been updated')
            #return redirect('core:dashboard')
            message = 'Your products have been updated'
            message_tag = 'success'
            #if product.actual_shopify_price == price:
            opti_price = 'Price Updated'
            #else:
            actual_price = '$ %s' %(float(opti.optimized_price))
                
        return HttpResponse(json.dumps({'message':message,'opti':opti_price,'tag':message_tag,'product_id':product.id,'actual_price':actual_price}), content_type='application/json')


class ShopifySubscribe(View):
    template_name = "core/subscribe_callback.html"
    def get(self, request, *args, **kwargs):
        plan_pricing = get_object_or_404(PlanPricing, id=kwargs.get('pk'))
        try:
            params = {
                "name": plan_pricing.plan.name,
                "price": float(plan_pricing.price),
                "trial_days": 10,
                "return_url": request.build_absolute_uri("/payment_callback/"),
                "terms": "test terms",
                "test": True
            }
            activate_shopify_session(request)

            charge = shopify.RecurringApplicationCharge.create(params)
            attrs = charge.attributes
            context = {}
            context['confirm_url'] = attrs["confirmation_url"]
            return render(request, self.template_name, context)            
        except Exception as e:
            msg = "Error in creating a charge for you. Kindly contact admin"
            messages.add_message(request, messages.ERROR, msg)

        return redirect("pricing")


class PaymentCallback(View):
    template_name = "core/shopify_callback.html"
    def get(self, request, *args, **kwargs):
        activate_shopify_session(request)
        shop_obj = Shop.objects.get(name=request.session.get('shop_name'))
        charge_id = request.GET.get('charge_id')
        payment_data = shopify.RecurringApplicationCharge.get(charge_id)
        status = payment_data['status']
        if status == 'accepted':
            charge = shopify.RecurringApplicationCharge(payment_data)
            charge.activate()
            plan_pricing = PlanPricing.objects.get(price=payment_data['price'])
            shop_obj.plan = plan_pricing.plan.id
            shop_obj.payment_token = charge.id
            shop_obj.payment_date = datetime.today()
            expire_date = datetime.today() + timedelta(days=10)
            shop_obj.expire_date = expire_date
            shop_obj.save()
        context = {}
        context["shop"] = shop_obj.name
        context["api_key"] = settings.SHOPIFY_API_KEY
        return render(request, self.template_name, context)            
