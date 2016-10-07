from django import template

from roojet.services.models import Optimization, Product
from roojet.core.models import Shop

register = template.Library()

@register.filter 
def get_value(quota):
    if quota.value is None:
    	return 'Unlimited'
    else:
    	return quota.value

@register.filter 
def get_price(price_plan,plan):
    plans = {'Roojet Bronze':'29','Roojet Silver':'79','Roojet Gold':'179'}
    try:
        price = plans[plan]
    except:
        price = '0.00 '
    return price

@register.filter 
def get_shop(plan,request):
	if request.GET.get('shop', '') == '':
		shop_name = request.session.get("shop_name")
	else:
		shop_name = request.GET.get('shop')
	shop = Shop.objects.get(name=shop_name)

	breturn = False
	if shop.plan:
		breturn = int(shop.plan) == plan.id
	return breturn

@register.filter 
def get_product_price(product, id):
	product_id = Product.objects.get(id=id)
	try:
		opti = Optimization.objects.filter(
		            Product__shopify_variant_id=product_id.shopify_variant_id).latest('updated')
		
		opt_price = opti.optimized_price
		if product_id.actual_shopify_price == opt_price:
			return "Price Updated"
		else:
			return '$ %s' %(opt_price)
	except:
		return 0