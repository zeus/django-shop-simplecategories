#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from cms.models import CMSPlugin
from django.db import models
from shop_simplecategories.models import Category
from django.utils.translation import ugettext_lazy as _

class CategoriesPlugin(CMSPlugin):
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'))