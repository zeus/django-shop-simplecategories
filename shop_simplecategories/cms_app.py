#!/usr/bin/env python
# vim:fileencoding=utf-8

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class ShopCategoriesApp(CMSApp):
    name = _("Shop categories App")
    urls = ["shop_simplecategories.urls"]

apphook_pool.register(ShopCategoriesApp)