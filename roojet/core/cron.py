import shopify
import requests
import json
import datetime
import iso8601
import stripe
from runstats import Statistics
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from decimal import *
from django.conf import settings
from django_cron import CronJobBase, Schedule
from pyactiveresource.connection import UnauthorizedAccess, ClientError

from roojet.services.models import Product, Optimization
from .utils import activate_shopify_session, calculate_expected_improvement_list

from roojet.core.models import Shop
from roojet.services.utils import get_historic



def calculate_expected_improvement(shop, orders, product_id=None,
                                   variable='revenue'):
    """
    Calculates expected improvement for the given orders and product.
    By default calculates revenue, but can calculate profit if variable=profit.
    """
    if product_id is None:
        return None, None
    points = []
    dates = []
    items = {}
    get_historic(shop=shop, orders=orders, product_id=product_id)
    print Product.objects.filter(shopify_variant_id=product_id)
    product_cost = Product.objects.get(shopify_variant_id=product_id).cost
    product_current_price = Product.objects.get(
        shopify_variant_id=product_id).actual_shopify_price
    previous_price = -1.0
    max_price = 0
    for order in orders:
        for item in order.line_items:
            order_date = iso8601.parse_date(order.created_at)
            if item.variant_id is not None and\
               int(product_id) == int(item.variant_id):
                price = str(item.price)
                if items.get(price, None) is None:
                    items[price] = {}
                    items[price]['stats'] = Statistics()
                    items[price]['quantity'] = 0
                    items[price]['days'] = 0
                items[price]['stats'].push(item.quantity)
                if variable == 'revenue':
                    items[price]['quantity'] += item.quantity
                else:
                    items[price]['quantity'] += item.quantity*float(price)
                items[price]['last_date'] = order_date
                dates.append([order_date, item.price])
                if previous_price == item.price:
                    days = abs((order_date - items[price]['last_date']).days)
                    items[price]['days'] += days
                else:
                    items[price]['days'] += 1
                previous_price = price
                if float(price) > max_price:
                    max_price = float(price)
                else:
                     max_price = float(price)
    for key, value in items.iteritems():
        if len(value['stats']) > 1:
            variance = value['stats'].variance()
        else:
            variance = 0.1
        try:
            key_point = (float(key)/max_price)*100.0
        except:
            key_point = 0.0

        points.append({"value_var": variance,
                       "value": -value['quantity']//value['days'],
                       "point": [key_point]})

    output = {
        'domain_info': {
            'domain_bounds': [{"max": 100.0, "min": 0.0}],
            'dim': 1
        },
        'gp_historical_info': {
            'points_sampled': points,
        },
    }
    print output
    try:
        next_points = requests.post(settings.MOE_URL + 'gp/next_points/epi',
                                json.dumps(output)).json()
    except:
        pass

    try:
        recommended_price = float(next_points['points_to_sample'][0][0])\
            * (max_price/100.0)
    except KeyError:
        recommended_price = None
    if recommended_price is not None:
        recommended_price = Decimal(recommended_price).\
            quantize(Decimal('.01'),
                     rounding=ROUND_DOWN)
    else:
        recommended_price = Decimal('0.00')
    if recommended_price < product_cost:
        recommended_price = product_current_price
    #if len(points) < settings.ENOUGH_DATA and variable == "profit":
    if variable == "profit":
        if recommended_price < Decimal('100.00'):
            recommended_price = recommended_price * Decimal("1.05")
        else:
            recommended_price = recommended_price * Decimal("1.025")
    Optimization.objects.create(Product=Product.
                                objects.get(
                                    created_by=shop,
                                    shopify_variant_id=product_id),
                                optimized_price=recommended_price,
                                type_of_optimization=variable)



def calculate_expected_improvement_list(shop, orders, items=[],
                                        variable='revenue'):

    """
    Helper function to calculate expected improvement of several items
    at once. Requires a list of ids and the orders.
    """
    output = {}
    for item in items:
        output[item] = calculate_expected_improvement(
            shop, orders, item, variable)
    return output


# def update_shopify_price(shop, price, variant_id):
#     session = shopify.Session(shop.shop_name + ".myshopify.com",
#                               shop.shop_token)
#
#     shopify.ShopifyResource.activate_session(session)
#     product = Product.objects.filter(created_by=shop,
#                                      shopify_variant_id=variant_id)
#     success = False
#     if product and price != Decimal('0.00'):
#         shopify_product = shopify.Variant.find(variant_id)
#         shopify_product.price = str(price)
#         try:
#             success = shopify_product.save()
#         except ServerError:
#             return success
#         except ForbiddenAccess:
#             return 'ForbiddenAccess'
#     shopify.ShopifyResource.clear_session()
#     return success


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60 # every 1 hour
    RETRY_AFTER_FAILURE_MINS = 2

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.MyCronJob'    # a unique code

    def do(self):
        variable = 'profit'
        shops = Shop.objects.all()
        for shop in shops:
            session = shopify.Session(shop.name,shop.token)

            shopify.ShopifyResource.activate_session(session)
            
            try:
                orders = shopify.Order.find()
            except:
                orders = []
            if orders:
                products = Product.objects.filter(created_by=shop)
                product_ids = []
                for product in products:
                    if product.shopify_variant_id:
                        product_ids.append(product.shopify_variant_id)
                calculate_expected_improvement_list(shop, orders,
                                            product_ids, variable)
