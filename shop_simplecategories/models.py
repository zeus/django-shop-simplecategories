# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.db import models
from shop.models.productmodel import Product
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField, get_thumbnail
from sorl.thumbnail.helpers import ThumbnailError
from django.conf import settings
import uuid
import os

class CategoryManager(models.Manager):
    def root_categories(self):
        return self.filter(parent_category__isnull=True)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(getattr(settings, 'CATEGORY_IMAGE_UPLOAD_TO', 'categories/'), filename)

class Category(models.Model):
    """
    This should be a node in a tree (mptt?) structure representing categories
    of products.
    Ideally, this should be usable as a tag cloud too (tags are just categories
    that are not in a tree structure). The display logic should be handle on a
    per-site basis
    """

    class Meta(object):
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ['order']

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    parent_category = models.ForeignKey('self',
                                        related_name="children",
                                        null=True, blank=True,
                                        verbose_name=_('Parent category'),
                                        )

    products = models.ManyToManyField(Product, related_name='categories',
                                      blank=True, null=True,
                                      verbose_name=_('Products'),
                                      )
    order = models.IntegerField(verbose_name=_('Ordering'), default=0)
    image = ImageField(verbose_name=_('Cover'), upload_to=get_file_path, null=True, blank=True)
    objects = CategoryManager()

    description = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

    def get_products(self):
        """
        Gets the products belonging to this category (not recursively)
        """
        return self.products.all()

    def get_child_categories(self):
        return Category.objects.filter(parent_category=self)

    def get_parents_as_tree(self, max_depth=10):
        root_cats = []
        current_category = self
        while max_depth:
            max_depth -= 1
            # Collect siblings
            level_categories = list(
                Category.objects.filter(parent_category=current_category.parent_category)
            )
            # Set active level
            for c in level_categories:
                if current_category == c:
                    c.active = True
                    if root_cats:
                        c.sub_categories = root_cats
                    break
            root_cats = level_categories
            if not current_category.parent_category:
                break
            current_category = current_category.parent_category
        return root_cats

    def get_parents_as_list(self, max_depth=10):
        def rec(arr):
            output = []
            for i in arr:
                output.append(i)
                if hasattr(i, 'sub_categories'):
                    subs = rec(i.sub_categories)
                    i.IN = True
                    subs[-1].OUT = True
                    output += subs
            return output
        return rec(self.get_parents_as_tree(max_depth))

    def admin_thumbnail(self):
        try:
            return '<img src="%s">' % get_thumbnail(self.image, '50x50', crop='center').url
        except IOError:
            return 'IOError'
        except ThumbnailError, ex:
            return 'ThumbnailError, %s' % ex.message

    admin_thumbnail.short_description = _('Thumbnail')
    admin_thumbnail.allow_tags = True

