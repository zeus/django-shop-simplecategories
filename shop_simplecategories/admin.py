#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from shop_simplecategories.models import Category
from django import forms
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin.current import AdminImageWidget
from sorl.thumbnail.fields import ImageField

class ProductWithCategoryForm(forms.ModelForm):
  categories = forms.ModelMultipleChoiceField(
    queryset=Category.objects.all(),
    required=False,
    widget=FilteredSelectMultiple(
      verbose_name=_('categories'),
      is_stacked=False
    )
  )
  def __init__(self, *args, **kwargs):
    super(ProductWithCategoryForm, self).__init__(*args, **kwargs)

    if self.instance and self.instance.pk:
      self.fields['categories'].initial = self.instance.categories.all()

  def save(self, commit=True):
    product = super(ProductWithCategoryForm, self).save(commit=False)

    if commit:
      product.save()

    if product.pk:
      product.categories = self.cleaned_data['categories']
      self.save_m2m()

    return product


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ['', {'fields': ['name', 'slug', 'parent_category', 'order', 'image', 'products']}]
    ]
    list_display = ['admin_thumbnail', 'name', 'parent_category', 'order']
    list_editable = ['order']
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget}
    }

admin.site.register(Category, CategoryAdmin)