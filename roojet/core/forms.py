from django import forms
from roojet.services.models import Product


class ShopForm(forms.Form):
    shop_name = forms.SlugField()


class ProductForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        choice_list = []
        products = Product.objects.filter(created_by=request.user)
        for product in products:
            choice_list.append((product.pk, product.title))
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['p'] = forms.ChoiceField(choices=choice_list)

