from decimal import Decimal
import shopify
import datetime
from django.contrib import messages
from pyactiveresource.connection import ServerError
from django.core.exceptions import ValidationError
from models import Product, Historic
from roojet.core.models import Shop
from validators import ProductValidator


def normalize_products(request, host=None):
    max_product_reached = False
    try:
        products = shopify.Product.find()
        orders = shopify.Order.find()
    except ServerError:
        return 'ServerError'
    except:
        products = []
        orders = []
    for product in products:
        product_id = int(product.attributes['id'])
        if host is not None:
            pixel_html = '<img src="http://' + host +\
                '/pixel/?product_id='+str(product_id) +\
                '" style="display: none;"/>'
            if product.attributes['body_html'] is None:
                product.attributes['body_html'] = pixel_html
                product.save()
            elif host + '/pixel/?product_id=' not in\
                    product.attributes['body_html']:
                product.attributes['body_html'] = product.attributes[
                 'body_html'] + pixel_html
                product.save()
        for variant in product.attributes['variants']:
            sells = 0
            variant_id = int(variant.attributes['id'])
            for order in orders:
                for item in order.line_items:
                    if item.variant_id is not None and\
                       variant_id == int(item.variant_id):
                        sells += 1

            created = variant.attributes['created_at'][:19]
            created_at_shopify = datetime.datetime.strptime(
              created,
              '%Y-%m-%dT%H:%M:%S')
            updated = variant.attributes['updated_at'][:19]
            updated_at_shopify = datetime.datetime.strptime(
              updated,
              '%Y-%m-%dT%H:%M:%S')
            price = Decimal(str(variant.attributes['price']))
            title = str(product.attributes['title'])
            shop_obj = Shop.objects.get(name=request.session.get('shop_name'))
            if variant.attributes['title'] != 'Default Title':
                title += "/" + str(variant.attributes['title'].encode('ascii', 'ignore'))
            if not Product.objects.filter(created_by=shop_obj,
                                          shopify_variant_id=variant_id):
                try:
                    ProductValidator()(shop_obj, add=1)
                except ValidationError:
                    max_product_reached = True
                    return Product.objects.filter(
                        created_by=shop_obj), max_product_reached

                Product.objects.create(created_by=shop_obj,
                                       shopify_product_id=product_id,
                                       shopify_variant_id=variant_id,
                                       title=str(variant.attributes['title'].encode('utf-8')),

                                       created_at_shopify=created_at_shopify,
                                       updated_at_shopify=updated_at_shopify,
                                       original_shopify_price=price,
                                       actual_shopify_price=price,
                                       number_of_sells=sells)
            else:
                Product.objects.filter(shopify_variant_id=variant_id).update(
                                       title=title,
                                       created_at_shopify=created_at_shopify,
                                       updated_at_shopify=updated_at_shopify,
                                       actual_shopify_price=price,
                                       number_of_sells=sells)
    return Product.objects.filter(created_by=shop_obj).order_by('-number_of_sells'), max_product_reached


def get_historic(shop, orders, product_id):

    orders_per_day = {}
    for order in orders:
        updated = datetime.datetime.strptime(
            order.updated_at[:19],
            '%Y-%m-%dT%H:%M:%S')
        if orders_per_day.get(str(updated.date()), None) is None:
            orders_per_day[str(updated.date())] = []
        orders_per_day[str(updated.date())] += [order]
    for order_day in orders_per_day:
        quantity = 0
        total = 0
        for order in orders_per_day[order_day]:
            for item in order.line_items:
                if item.variant_id is not None and\
                 int(item.variant_id) == int(product_id):
                    quantity += 1
                    total += Decimal(item.price)
                    date = datetime.datetime.strptime(
                        order_day, '%Y-%m-%d').date()
                    historic = Historic.objects.filter(
                        Product__created_by=shop,
                        Product__shopify_variant_id=product_id, date=date)
                    if not historic:
                        Historic.objects.create(
                            Product=Product.
                            objects.get(
                                created_by=shop,
                                shopify_variant_id=product_id),
                            price=Decimal(item.price),
                            quantity=quantity,
                            total=total,
                            date=date)
                    else:
                        obj = Historic.objects.get(
                                Product__created_by=shop,
                                Product__shopify_variant_id=product_id,
                                date=date)
                        obj.quantity = quantity
                        obj.price = item.price
                        obj.total = total
                        obj.save()

