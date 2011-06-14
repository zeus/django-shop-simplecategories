#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'


from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import CategoriesPlugin
from django.utils.translation import ugettext_lazy as _

class CategoryPlugin(CMSPluginBase):
    model = CategoriesPlugin
    name = _('Categories')
    render_template = "cms/plugins/categories.html"
    text_enabled = True

    def render(self, context, instance, placeholder):
        context.update({'category_list': instance.categories.all()})
        return context

plugin_pool.register_plugin(CategoryPlugin)
