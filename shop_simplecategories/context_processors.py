#!/usr/bin/env python
# vim:fileencoding=utf-8

__author__ = 'zeus'

from models import Category

def root_categories(request):
    return {'ROOT_CATEGORIES': Category.objects.filter(parent_category=None)}