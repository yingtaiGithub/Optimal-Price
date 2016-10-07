from django.conf import settings
import requests
import json
import shopify
import datetime
from runstats import Statistics
from decimal import *
import iso8601
from pyactiveresource.connection import ServerError, ForbiddenAccess
from roojet.services.models import Optimization, Product
from roojet.services.utils import get_historic


def activate_shopify_session(request):

    session = shopify.Session(request.session.get('shop_name'),
                              request.session.get('shop_token'))

    shopify.ShopifyResource.activate_session(session)


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
    for key, value in items.iteritems():
        if len(value['stats']) > 1:
            variance = value['stats'].variance()
        else:
            variance = 0.1

        points.append({"value_var": variance,
                       "value": -value['quantity']//value['days'],
                       "point": [(float(key)/max_price)*100.0]})

    output = {
        'domain_info': {
            'domain_bounds': [{"max": 100.0, "min": 0.0}],
            'dim': 1
        },
        'gp_historical_info': {
            'points_sampled': points,
        },
    }
    next_points = requests.post(settings.MOE_URL + 'gp/next_points/epi',
                                json.dumps(output)).json()

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
    if len(points) < settings.ENOUGH_DATA and variable == "profit":
        if recommended_price < Decimal('100.00'):
            recommended_price = recommended_price * Decimal("1.05")
        else:
            recommended_price = recommended_price * Decimal("1.025")
    today_optimizations = Optimization.objects.filter(
                  Product__created_by=shop,
                  Product__shopify_variant_id=product_id,
                  updated=datetime.datetime.today,
                  type_of_optimization=variable)
    if not today_optimizations:
        Optimization.objects.create(Product=Product.
                                    objects.get(
                                        created_by=shop,
                                        shopify_variant_id=product_id),
                                    optimized_price=recommended_price,
                                    type_of_optimization=variable)
    else:
        Optimization.objects.filter(
                  Product__created_by=shop,
                  Product__shopify_variant_id=product_id,
                  updated=datetime.datetime.today,
                  type_of_optimization=variable).update(
                  optimized_price=recommended_price)


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


def update_shopify_price(shop, price, variant_id):
    session = shopify.Session(shop.name,
                              shop.token)

    shopify.ShopifyResource.activate_session(session)
    product = Product.objects.filter(created_by=shop,
                                     shopify_variant_id=variant_id)
    success = False
    if product and price != Decimal('0.00'):
        shopify_product = shopify.Variant.find(variant_id)
        shopify_product.price = str(price)
        try:
            success = shopify_product.save()
        except ServerError:
            return success
        except ForbiddenAccess:
            return 'ForbiddenAccess'
    shopify.ShopifyResource.clear_session()
    return success


def get_increased_profit(products, historic):
    total_profit = 0
    total_profit_margin = 0
    total_old_profit_margin = 0
    for product in products:
        try:
            product_profit_margin = ((product.actual_shopify_price-product.cost)/product.actual_shopify_price)*100
        except DecimalException:
            product_profit_margin = 0
        try:
            old_product_profit_margin = ((product.original_shopify_price-product.cost)/product.original_shopify_price)*100
        except DecimalException:
            old_product_profit_margin = 0
        total_profit_margin += product_profit_margin
        total_old_profit_margin += old_product_profit_margin

        historic_of_product = historic.filter(Product=product).order_by('date')
        for hist in historic_of_product:
            if hist.date >= product.created.date():
                hist_profit = (
                    hist.price-product.original_shopify_price)*hist.quantity
                total_profit += hist_profit

    try:
        average_profit_margin = total_profit_margin/len(products)
        average_old_profit_margin = total_old_profit_margin/len(products)
        profit_margin = abs(((average_profit_margin/average_old_profit_margin) - 1)*100)
    except DecimalException:
        average_profit_margin = 0
        average_old_profit_margin = 0
        profit_margin = 0
    return total_profit, profit_margin
