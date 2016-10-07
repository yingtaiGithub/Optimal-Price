from plans.validators import ModelCountValidator
from plans.quota import get_user_quota
from models import Product
from plans.models import *
from roojet.core.models import Shop


class ProductValidator(ModelCountValidator):
    """
    Validates that the user websites number
    doesn't conflict with the plan he has acquired
    """
    code = 'NUMBER_OF_PRODUCTS'
    model = Product

    def get_queryset(self, shop):
        """
        Queryset contains all the products for a given user
        """
        return self.model.objects.filter(created_by=shop)

    def get_quota_value(self, shop, quota_dict=None):
        """
        Returns quota value for a given user
        """
        if quota_dict is None and shop.plan is not None:
            quota_dict = Plan.objects.get(id=shop.plan).get_quota_dict()
        if quota_dict is not None:
            return quota_dict.get(self.code, None)
        else:
            return None


product_validator = ProductValidator()
