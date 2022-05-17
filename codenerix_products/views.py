# -*- coding: utf-8 -*-
#
# django-codenerix-products
#
# Codenerix GNU
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import datetime
import json
import operator
import time
from functools import reduce

from django.db import IntegrityError, transaction
from django.db.models import Q, F, Value, Sum
from django.db.models.functions import Concat
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.forms.utils import ErrorList
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.generic import View
from django.conf import settings

from codenerix.multiforms import MultiForm
from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete, GenDetail, GenDetailModal, GenForeignKey
from codenerix_extensions.files.views import DocumentFileView, ImageFileView
from codenerix_extensions.helpers import get_language_database

from .models import TypeTax, Feature, Attribute, FeatureSpecial, Family, Category, Subcategory, Product, ProductRelationSold, ProductImage, ProductFinalImage
from .models import ProductDocument, ProductFinal, ProductFeature, ProductUnique, ProductFinalAttribute, Brand, FlagshipProduct
from .models import GroupValueFeature, GroupValueAttribute, GroupValueFeatureSpecial, OptionValueFeature, OptionValueAttribute, OptionValueFeatureSpecial
from .models import MODELS, MODELS_SLUG, MODELS_BRANDS, MODELS_PRODUCTS, MODELS_PRODUCTS_FINAL, MODELS_SLIDERS, TYPE_VALUE_LIST, TYPE_VALUE_BOOLEAN, TYPE_VALUE_FREE
from .forms import TypeTaxForm, FeatureForm, AttributeForm, FeatureSpecialForm, FamilyForm, CategoryForm, SubcategoryForm, SubcategoryOwnForm, ProductFormCreate
from .forms import ProductForm, ProductRelationSoldForm, ProductImageForm, ProductFinalImageForm, ProductDocumentForm, ProductFinalFormCreate, ProductFinalFormCreateModal, ProductFinalForm, ProductFeatureForm, ProductUniqueForm
from .forms import ProductFinalAttributeForm, ProductFinalRelatedSubForm, BrandForm, FlagshipProductForm
from .forms import GroupValueFeatureForm, GroupValueAttributeForm, GroupValueFeatureSpecialForm, OptionValueFeatureForm, OptionValueAttributeForm, OptionValueFeatureSpecialForm
from .forms import ProductFinalOption
from .forms import ProductFinalOptionForm, ProductFinalOptionFormWithoutProduct
from .forms import ProductFormCreateCustom


# ###########################################
# import dynamic
query = ""
# forms for multiforms
formsfull = {}

for info in MODELS + MODELS_BRANDS + MODELS_PRODUCTS + MODELS_SLIDERS + MODELS_SLUG + MODELS_PRODUCTS_FINAL:
    field = info[0]
    model = info[1]
    formsfull[model] = [(None, None, None)]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_products.models import {}Text{}\n".format(model, lang_code)
        query += "from codenerix_products.forms import {}TextForm{}".format(model, lang_code)
        exec(query)

        formsfull[model].append((eval("{}TextForm{}".format(model, lang_code.upper())), field, None))


# Mixins
class TranslatedMixin(object):

    @property
    def lang(self):
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == self.request.LANGUAGE_CODE:
                return self.request.LANGUAGE_CODE.lower()
        return settings.LANGUAGES[0][0].lower()


# ###########################################
class GenTypeTaxUrl(object):
    ws_entry_point = '{}/typetaxs'.format(settings.CDNX_PRODUCTS_URL)


# TypeTax
class TypeTaxList(GenTypeTaxUrl, GenList):
    model = TypeTax
    show_details = True
    extra_context = {
        'menu': ['TypeTax', 'people'],
        'bread': [_('TypeTax'), _('People')]
    }


class TypeTaxCreate(GenTypeTaxUrl, GenCreate):
    model = TypeTax
    form_class = TypeTaxForm


class TypeTaxCreateModal(GenCreateModal, TypeTaxCreate):
    pass


class TypeTaxUpdate(GenTypeTaxUrl, GenUpdate):
    model = TypeTax
    form_class = TypeTaxForm


class TypeTaxUpdateModal(GenUpdateModal, TypeTaxUpdate):
    pass


class TypeTaxDelete(GenTypeTaxUrl, GenDelete):
    model = TypeTax


class TypeTaxDetails(GenTypeTaxUrl, GenDetail):
    model = TypeTax
    groups = TypeTaxForm.__groups_details__()


class TypeTaxForeign(GenTypeTaxUrl, GenForeignKey):
    model = TypeTax
    label = "{name}"

    def custom_choice(self, obj, info):
        info['tax'] = obj.tax
        return info

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(name__icontains=search)

        qs = queryset.filter(qsobject)
        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenFeatureUrl(object):
    ws_entry_point = '{}/features'.format(settings.CDNX_PRODUCTS_URL)


# Feature
class FeatureList(GenFeatureUrl, GenList):
    model = Feature
    extra_context = {
        'menu': ['Feature', 'people'],
        'bread': [_('Feature'), _('People')]
    }


class FeatureCreate(GenFeatureUrl, ImageFileView, MultiForm, GenCreate):
    model = Feature
    form_class = FeatureForm
    forms = formsfull["Feature"]


class FeatureCreateModal(GenCreateModal, FeatureCreate):
    pass


class FeatureUpdate(GenFeatureUrl, ImageFileView, MultiForm, GenUpdate):
    model = Feature
    form_class = FeatureForm
    forms = formsfull["Feature"]


class FeatureUpdateModal(GenUpdateModal, FeatureUpdate):
    pass


class FeatureDelete(GenFeatureUrl, GenDelete):
    model = Feature


class FeatureForeign(GenFeatureUrl, GenForeignKey):
    model = Feature
    label = "{<LANGUAGE_CODE>__description}"
    clear_fields = ['value_free', 'value_bool', 'value_list', ]

    def custom_choice(self, obj, info):
        info['_clear_'] = ['value_free', 'value_bool', 'value_list', ]
        info['type'] = obj.type_value
        return info

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(family__code__icontains=search)
        qsobject |= Q(category__code__icontains=search)

        for lang in settings.LANGUAGES_DATABASES:
            qsobject |= Q(**{"{}__description__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"family__{}__name__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"category__{}__name__icontains".format(lang.lower()): search})

        qs = queryset.filter(qsobject)

        product_pk = filters.get('product_pk', None)

        if product_pk:
            qs = qs.filter(
                Q(category__products__pk=product_pk),
                Q(family__products__pk=product_pk)
            )

        qsobject = Q(**{"family__isnull": True})
        qsobject |= Q(**{"category__isnull": True})
        qs = queryset.filter(qsobject)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenAttributeUrl(object):
    ws_entry_point = '{}/attributes'.format(settings.CDNX_PRODUCTS_URL)


# Attribute
class AttributeList(GenAttributeUrl, GenList):
    model = Attribute
    extra_context = {
        'menu': ['Attribute', 'people'],
        'bread': [_('Attribute'), _('People')]
    }


class AttributeCreate(GenAttributeUrl, ImageFileView, MultiForm, GenCreate):
    model = Attribute
    form_class = AttributeForm
    forms = formsfull["Attribute"]


class AttributeCreateModal(GenCreateModal, AttributeCreate):
    pass


class AttributeUpdate(GenAttributeUrl, ImageFileView, MultiForm, GenUpdate):
    model = Attribute
    form_class = AttributeForm
    forms = formsfull["Attribute"]


class AttributeUpdateModal(GenUpdateModal, AttributeUpdate):
    pass


class AttributeDelete(GenAttributeUrl, GenDelete):
    model = Attribute


class AttributeForeign(GenAttributeUrl, GenForeignKey):
    model = Attribute
    label = "{<LANGUAGE_CODE>__description}"
    clear_fields = ['value_free', 'value_bool', 'value_list', ]

    def custom_choice(self, obj, info):
        info['_clear_'] = ['value_free', 'value_bool', 'value_list', ]
        info['type'] = obj.type_value
        return info

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(family__code__icontains=search)
        qsobject |= Q(category__code__icontains=search)

        for lang in settings.LANGUAGES_DATABASES:
            qsobject |= Q(**{"{}__description__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"family__{}__name__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"category__{}__name__icontains".format(lang.lower()): search})
        qs = queryset.filter(qsobject)

        product_pk = filters.get('product_pk', None)

        if product_pk:
            qs = qs.filter(
                category__products__products_final__pk=product_pk,
                family__products__products_final__pk=product_pk
            )
        qsobject = Q(**{"family__isnull": True})
        qsobject |= Q(**{"category__isnull": True})
        qs = queryset.filter(qsobject)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenFeatureSpecialUrl(object):
    ws_entry_point = '{}/featurespecials'.format(settings.CDNX_PRODUCTS_URL)


# FeatureSpecial
class FeatureSpecialList(GenFeatureSpecialUrl, GenList):
    model = FeatureSpecial
    extra_context = {
        'menu': ['FeatureSpecial', 'people'],
        'bread': [_('FeatureSpecial'), _('People')]
    }


class FeatureSpecialCreate(GenFeatureSpecialUrl, ImageFileView, MultiForm, GenCreate):
    model = FeatureSpecial
    form_class = FeatureSpecialForm
    forms = formsfull["FeatureSpecial"]


class FeatureSpecialCreateModal(GenCreateModal, FeatureSpecialCreate):
    pass


class FeatureSpecialUpdate(GenFeatureSpecialUrl, ImageFileView, MultiForm, GenUpdate):
    model = FeatureSpecial
    form_class = FeatureSpecialForm
    forms = formsfull["FeatureSpecial"]


class FeatureSpecialUpdateModal(GenUpdateModal, FeatureSpecialUpdate):
    pass


class FeatureSpecialDelete(GenFeatureSpecialUrl, GenDelete):
    model = FeatureSpecial


class FeatureSpecialForeign(GenFeatureSpecialUrl, GenForeignKey):
    model = FeatureSpecial
    label = "{<LANGUAGE_CODE>__description}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(family__code__icontains=search)
        qsobject |= Q(category__code__icontains=search)

        for lang in settings.LANGUAGES_DATABASES:
            qsobject |= Q(**{"{}__description__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"family__{}__name__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"category__{}__name__icontains".format(lang.lower()): search})
        qs = queryset.filter(qsobject)

        product_pk = filters.get('product_pk', None)

        if product_pk:
            qs = qs.filter(
                category__products__products_final__pk=product_pk,
                family__products__products_final__pk=product_pk
            )

        qsobject = Q(**{"family__isnull": True})
        qsobject |= Q(**{"category__isnull": True})
        qs = queryset.filter(qsobject)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenFamilyUrl(object):
    ws_entry_point = '{}/familys'.format(settings.CDNX_PRODUCTS_URL)


# Family
class FamilyList(GenFamilyUrl, GenList):
    model = Family
    extra_context = {
        'menu': ['Product', 'family'],
        'bread': [_('Product'), _('Family')]
    }


class FamilyCreate(GenFamilyUrl, ImageFileView, MultiForm, GenCreate):
    model = Family
    form_class = FamilyForm
    forms = formsfull["Family"]


class FamilyCreateModal(GenCreateModal, FamilyCreate):
    pass


class FamilyUpdate(GenFamilyUrl, ImageFileView, MultiForm, GenUpdate):
    model = Family
    form_class = FamilyForm
    forms = formsfull["Family"]


class FamilyUpdateModal(GenUpdateModal, FamilyUpdate):
    pass


class FamilyDelete(GenFamilyUrl, GenDelete):
    model = Family


# ###########################################
class GenCategoryUrl(object):
    ws_entry_point = '{}/categorys'.format(settings.CDNX_PRODUCTS_URL)


# Category
class CategoryList(GenCategoryUrl, GenList):
    model = Category
    show_details = True
    extra_context = {
        'menu': ['Category', 'people'],
        'bread': [_('Category'), _('People')]
    }


class CategorySubListPro(CategoryList):
    show_details = False
    linkadd = False

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(providercategories=pk)
        return limit


class CategoryCreate(GenCategoryUrl, MultiForm, GenCreate):
    model = Category
    form_class = CategoryForm
    forms = formsfull["Category"]


class CategoryCreateModal(GenCreateModal, CategoryCreate):
    pass


class CategoryUpdate(GenCategoryUrl, MultiForm, GenUpdate):
    model = Category
    show_details = True
    form_class = CategoryForm
    forms = formsfull["Category"]


class CategoryUpdateModal(GenUpdateModal, CategoryUpdate):
    pass


class CategoryUpdateModalPro(CategoryUpdateModal):
    linkdelete = False


class CategoryDelete(GenCategoryUrl, GenDelete):
    model = Category


class CategoryDetails(GenCategoryUrl, GenDetail):
    model = Category
    groups = CategoryForm.__groups_details__()
    template_model = "codenerix_products/category_details.html"

    tabs = [
        {
            'id': 'Subcategory',
            'name': _('Subcategories'),
            'ws': 'CDNX_products_subcategory_sublist',
            'rows': 'base'
        },
    ]
    exclude_fields = []


class CategoryDetailModalPro(GenDetailModal, CategoryDetails):
    pass


class CategoryForeign(GenCategoryUrl, GenForeignKey):
    model = Category
    label = "{<LANGUAGE_CODE>__name} ({code})"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        query = [Q(code__icontains=search), ]
        for lang in settings.LANGUAGES_DATABASES:
            query.append(Q(**{"{}__name__icontains".format(lang.lower()): search}))

        qs = queryset.filter(
            reduce(operator.or_, query)
        )
        family = filters.get('FeatureForm_family', None)
        if family is None:
            family = filters.get('AttributeForm_family', None)
        if family is None:
            family = filters.get('FeatureSpecialForm_family', None)
        if family is None:
            family = filters.get('ProductForm_family', None)
        if family is None:
            family = filters.get('ProductFormCreate_family', None)
        if family is None:
            family = filters.get('ProductFormCreateCustom_family', None)

        if family:
            qs = qs.filter(family__pk=family)

        return qs[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenSubcategoryUrl(object):
    ws_entry_point = '{}/subcategorys'.format(settings.CDNX_PRODUCTS_URL)


# Subcategory
class SubcategoryList(GenSubcategoryUrl, GenList):
    model = Subcategory
    extra_context = {
        'menu': ['Subcategory', 'people'],
        'bread': [_('Subcategory'), _('People')]
    }
    default_ordering = ['order']


class SubcategoryCreate(GenSubcategoryUrl, MultiForm, GenCreate):
    model = Subcategory
    form_class = SubcategoryForm
    forms = formsfull["Subcategory"]


class SubcategoryCreateModalAll(GenCreateModal, SubcategoryCreate):
    pass


class SubcategoryCreateModal(GenCreateModal, SubcategoryCreate):
    form_class = SubcategoryOwnForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__category_pk = kwargs.get('cpk', None)
        return super(SubcategoryCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form, multiform):
        if self.__category_pk:
            category = Category.objects.get(pk=self.__category_pk)
            self.request.category = category
            form.instance.category = category

        return super(SubcategoryCreateModal, self).form_valid(form, multiform)


class SubcategoryUpdate(MultiForm, GenSubcategoryUrl, GenUpdate):
    model = Subcategory
    form_class = SubcategoryForm
    forms = formsfull["Subcategory"]


class SubcategoryUpdateModal(GenUpdateModal, SubcategoryUpdate):
    form_class = SubcategoryOwnForm


class SubcategoryDelete(GenSubcategoryUrl, GenDelete):
    model = Subcategory


class SubcategoryForeign(GenSubcategoryUrl, GenForeignKey):
    model = Subcategory
    label = "{<LANGUAGE_CODE>__name} ({code})"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        query = [Q(code__icontains=search), ]
        for lang in settings.LANGUAGES_DATABASES:
            query.append(Q(**{"{}__name__icontains".format(lang.lower()): search}))

        qs = queryset.filter(
            reduce(operator.or_, query)
        )
        category = filters.get('ProductForm_category', None)
        if category is None:
            category = filters.get('ProductFormCreate_category', None)
        if category is None:
            category = filters.get('ProductFormCreateCustom_category', None)

        if category:
            qs = qs.filter(category__pk=category)

        return qs[:settings.LIMIT_FOREIGNKEY]


class SubcategoryDetail(GenSubcategoryUrl, GenDetail):
    model = Subcategory
    groups = SubcategoryForm.__groups_details__()


class SubcategoryDetailModal(GenDetailModal, SubcategoryDetail):
    pass


class SubcategorySubList(GenSubcategoryUrl, GenList):
    model = Subcategory

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(category__pk=pk)
        return limit


# ###########################################
class GenProductUrl(object):
    ws_entry_point = '{}/products'.format(settings.CDNX_PRODUCTS_URL)


# Product
class ProductList(TranslatedMixin, GenProductUrl, GenList):
    model = Product
    show_details = True
    extra_context = {
        'menu': ['Product', 'people'],
        'bread': [_('Product'), _('People')]
    }
    gentrans = {
        'AddProductAndProductFinal': _("Add product & product final"),
    }
    annotations = {
        'stock_original': Sum("products_final__products_unique__stock_original"),
        'stock_real': Sum("products_final__products_unique__stock_real"),
        'stock_locked': Sum("products_final__products_unique__stock_locked"),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('category', _("Category")))
        fields.append(('subcategory', _("Subcategory")))
        fields.append(('code', _("Code")))
        fields.append(('{}__name'.format(self.lang), _("Name")))
        fields.append(('public', _("Public")))
        fields.append(('tax', _("Tax")))
        fields.append(('price_base', _("Price base")))
        fields.append(('of_sales', _("Of sales")))
        fields.append(('of_purchase', _("Of purchase")))
        fields.append(('force_stock', _("Force stock")))
        fields.append(('feature_special', _("Feature special")))
        fields.append(('stock_original', _("Stock Original")))
        fields.append(('stock_real', _("Stock Real")))
        fields.append(('stock_locked', _("Stock Locked")))
        return fields

    def __searchF__(self, info):
        lang = get_language_database()

        fields = {}
        fields['{}__name'.format(lang)] = (_('Name'), lambda x, lang=lang: Q(**{'{}__name__icontains'.format(lang): x}), 'input')
        fields['category'] = (_('Category'), lambda x, lang=lang: Q(**{'category__{}__name__icontains'.format(lang): x}), 'input')
        fields['subcategory'] = (_('Subcategory'), lambda x, lang=lang: Q(**{'subcategory__{}__name__icontains'.format(lang): x}), 'input')
        return fields


class ProductCreate(GenProductUrl, MultiForm, GenCreate):
    model = Product
    form_class = ProductFormCreate
    show_details = True
    forms = formsfull['ProductText']

    def get_initial(self):
        super(ProductCreate, self).get_initial()
        self.initial['tax'] = TypeTax.objects.filter(default=True).first()
        self.initial['force_stock'] = getattr(settings, 'CDNX_PRODUCTS_FORCE_STOCK', True)
        return self.initial


class ProductCreateModal(GenCreateModal, ProductCreate):
    pass


class ProductUpdate(GenProductUrl, MultiForm, GenUpdate):
    model = Product
    form_class = ProductForm
    show_details = True
    forms = formsfull['ProductText']


class ProductUpdateModal(GenUpdateModal, ProductUpdate):
    pass


class ProductDelete(GenProductUrl, GenDelete):
    model = Product


class ProductDetails(GenProductUrl, GenDetail):
    model = Product
    groups = ProductForm.__groups_details__()
    template_model = "codenerix_products/product_details.html"
    tabs = [
        {'id': 'Feature', 'name': _('Features'), 'ws': 'CDNX_products_productfeatures_sublist', 'rows': 'base'},
        {'id': 'Document', 'name': _('Documents'), 'ws': 'CDNX_products_productdocuments_sublist', 'rows': 'base'},
        {'id': 'Images', 'name': _('Images'), 'ws': 'CDNX_products_productimages_sublist', 'rows': 'base'},
        {'id': 'ProductFinal', 'name': _('Products Final'), 'ws': 'CDNX_products_productfinals_sublist', 'rows': 'base', 'static_partial_row': 'codenerix_products/productfinals_sublist_rows.html'},
    ]
    exclude_fields = ["related", ]


class ProductForeign(GenForeignKey):
    model = Product
    label = '{code} - {<LANGUAGE_CODE>__name} - {<LANGUAGE_CODE>__slug}'

    def get_foreign(self, queryset, search, filters):
        # Filter with search string
        qsobject = Q(model__icontains=search)

        for lang in settings.LANGUAGES_DATABASES:
            qsobject |= Q(**{"{}__name__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"{}__description_short__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"family__{}__name__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"category__{}__name__icontains".format(lang.lower()): search})
            qsobject |= Q(**{"subcategory__{}__name__icontains".format(lang.lower()): search})

        queryset = queryset.filter(qsobject)

        return queryset[:settings.LIMIT_FOREIGNKEY]


# ###########################################
class GenBrandUrl(object):
    ws_entry_point = '{}/brands'.format(settings.CDNX_PRODUCTS_URL)


# Marca
class BrandList(TranslatedMixin, GenBrandUrl, GenList):
    model = Brand
    extra_context = {
        'menu': ['Product', 'brand'],
        'bread': [_('Product'), _('Brand')]
    }
    default_ordering = ['order']

    def __fields__(self, info):
        fields = []
        fields.append(('name:{}__name'.format(self.lang), _("Name")))
        fields.append(('slug:{}__slug'.format(self.lang), _("Slug")))
        fields.append(('outstanding', _("Outstanding")))
        fields.append(('show_menu', _("Show menu")))
        fields.append(('order', _("Order")))
        return fields


class BrandCreate(GenBrandUrl, ImageFileView, MultiForm, GenCreate):
    model = Brand
    form_class = BrandForm
    forms = formsfull["Brand"]


class BrandCreateModal(GenCreateModal, BrandCreate):
    pass


class BrandUpdate(GenBrandUrl, ImageFileView, MultiForm, GenUpdate):
    model = Brand
    form_class = BrandForm
    forms = formsfull["Brand"]


class BrandUpdateModal(GenUpdateModal, BrandUpdate):
    pass


class BrandDelete(GenBrandUrl, GenDelete):
    model = Brand


# ###########################################
class GenProductRelationSoldUrl(object):
    ws_entry_point = '{}/productrelationsolds'.format(settings.CDNX_PRODUCTS_URL)


# ProductRelationSold
class ProductRelationSoldList(GenProductRelationSoldUrl, GenList):
    model = ProductRelationSold
    extra_context = {
        'menu': ['ProductRelationSold', 'people'],
        'bread': [_('ProductRelationSold'), _('People')]
    }


class ProductRelationSoldCreate(GenProductRelationSoldUrl, GenCreate):
    model = ProductRelationSold
    form_class = ProductRelationSoldForm


class ProductRelationSoldCreateModal(GenCreateModal, ProductRelationSoldCreate):
    pass


class ProductRelationSoldUpdate(GenProductRelationSoldUrl, GenUpdate):
    model = ProductRelationSold
    form_class = ProductRelationSoldForm


class ProductRelationSoldUpdateModal(GenUpdateModal, ProductRelationSoldUpdate):
    pass


class ProductRelationSoldDelete(GenProductRelationSoldUrl, GenDelete):
    model = ProductRelationSold


# ###########################################
class GenProductImageUrl(object):
    ws_entry_point = '{}/productimages'.format(settings.CDNX_PRODUCTS_URL)


# ProductImage
class ProductImageList(GenProductImageUrl, GenList):
    model = ProductImage
    extra_context = {
        'menu': ['ProductImage', 'people'],
        'bread': [_('ProductImage'), _('People')]
    }


class ProductImageCreate(GenProductImageUrl, ImageFileView, MultiForm, GenCreate):
    model = ProductImage
    form_class = ProductImageForm
    forms = formsfull["ProductImage"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__group_pk = kwargs.get('cpk', None)
        return super(ProductImageCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__group_pk:
            product = Product.objects.get(pk=self.__group_pk)
            self.request.product = product
            form.instance.product = product

        return super(ProductImageCreate, self).form_valid(form, forms)


class ProductImageCreateModal(GenCreateModal, ProductImageCreate):
    pass


class ProductImageUpdate(GenProductImageUrl, ImageFileView, MultiForm, GenUpdate):
    model = ProductImage
    form_class = ProductImageForm
    forms = formsfull["ProductImage"]


class ProductImageUpdateModal(GenUpdateModal, ProductImageUpdate):
    pass


class ProductImageDelete(GenProductImageUrl, GenDelete):
    model = ProductImage


class ProductImageSubList(GenProductImageUrl, GenList):
    model = ProductImage
    annotations = {
        'image_path': Concat(Value(settings.MEDIA_URL), 'image'),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(product__pk=pk)
        return limit

    def __fields__(self, info):
        fields = []
        fields.append(('order', _("Order")))
        fields.append(('public', _("Public")))
        fields.append(('principal', _("Principal")))
        fields.append(('image', _("Image"), None, None, 'image:width:66px'))
        return fields


class ProductImageDetails(GenProductImageUrl, GenDetail):
    model = ProductImage
    groups = ProductImageForm.__groups_details__()


class ProductImageDetailsModal(GenDetailModal, ProductImageDetails):
    pass


# ###########################################
class GenProductDocumentUrl(object):
    ws_entry_point = '{}/productdocuments'.format(settings.CDNX_PRODUCTS_URL)


# ProductDocument
class ProductDocumentList(GenProductDocumentUrl, GenList):
    model = ProductDocument
    extra_context = {
        'menu': ['ProductDocument', 'people'],
        'bread': [_('ProductDocument'), _('People')]
    }


class ProductDocumentCreate(GenProductDocumentUrl, DocumentFileView, MultiForm, GenCreate):
    model = ProductDocument
    form_class = ProductDocumentForm
    forms = formsfull["ProductDocument"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__group_pk = kwargs.get('cpk', None)
        return super(ProductDocumentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__group_pk:
            product = Product.objects.get(pk=self.__group_pk)
            self.request.product = product
            form.instance.product = product

        return super(ProductDocumentCreate, self).form_valid(form, forms)


class ProductDocumentCreateModal(GenCreateModal, ProductDocumentCreate):
    pass


class ProductDocumentUpdate(GenProductDocumentUrl, DocumentFileView, MultiForm, GenUpdate):
    model = ProductDocument
    form_class = ProductDocumentForm
    forms = formsfull["ProductDocument"]


class ProductDocumentUpdateModal(GenUpdateModal, ProductDocumentUpdate):
    pass


class ProductDocumentDelete(GenProductDocumentUrl, GenDelete):
    model = ProductDocument


class ProductDocumentSubList(GenProductDocumentUrl, GenList):
    model = ProductDocument

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(product__pk=pk)
        return limit


class ProductDocumentDetails(GenProductDocumentUrl, GenDetail):
    model = ProductDocument
    groups = ProductDocumentForm.__groups_details__()


class ProductDocumentDetailsModal(GenDetailModal, ProductDocumentDetails):
    pass


# ###########################################
class GenProductFinalUrl(object):
    ws_entry_point = '{}/productfinals'.format(settings.CDNX_PRODUCTS_URL)


# ProductFinal
class ProductFinalList(GenProductFinalUrl, GenList):
    model = ProductFinal
    show_details = True
    extra_context = {
        'menu': ['ProductFinal', 'people'],
        'bread': [_('ProductFinal'), _('People')]
    }
    gentrans = {
        'AddProductAndProductFinal': _("Add product & product final"),
    }
    annotations = {
        'stock_original': Sum("products_unique__stock_original"),
        'stock_real': Sum("products_unique__stock_real"),
        'stock_locked': Sum("products_unique__stock_locked"),
    }

    def __fields__(self, info):
        lang = get_language_database()
        fields = []
        fields.append(('product__family__{}__name'.format(lang), _("Family")))
        fields.append(('product__category__{}__name'.format(lang), _("Category")))
        fields.append(('product__subcategory__{}__name'.format(lang), _("Subcategory")))
        fields.append(('code', _("Code")))
        fields.append(('product__code', _("Product Code")))
        fields.append(('{}__name'.format(lang), _("Product")))
        fields.append(('{}__public'.format(lang), _("Public")))
        fields.append(('price', _("Price")))
        fields.append(('is_pack', _("Is pack")))
        fields.append(('sample', _("Sample")))
        fields.append(('stock_original', _("Stock Original")))
        fields.append(('stock_real', _("Stock Real")))
        fields.append(('stock_locked', _("Stock Locked")))
        return fields


class ProductFinalCreate(GenProductFinalUrl, MultiForm, GenCreate):
    model = ProductFinal
    form_class = ProductFinalFormCreate
    show_details = True
    forms = formsfull['ProductFinal']
    # hide_foreignkey_button = True


class ProductFinalCreateModal(GenCreateModal, ProductFinalCreate):
    def dispatch(self, *args, **kwargs):
        self.__product_pk = kwargs.get('cpk', None)
        if self.__product_pk:
            self.form_class = ProductFinalFormCreateModal
        return super(ProductFinalCreateModal, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__product_pk:
            product = Product.objects.get(pk=self.__product_pk)
            self.request.product = product
            form.instance.product = product

        return super(ProductFinalCreateModal, self).form_valid(form, forms)


class ProductCreateCustom(MultiForm, GenCreate):
    model = Product
    form_class = ProductFormCreateCustom
    show_details = False
    forms = formsfull['ProductText']

    def get_initial(self):
        super(ProductCreateCustom, self).get_initial()
        self.initial['tax'] = TypeTax.objects.filter(default=True).first()
        self.initial['force_stock'] = getattr(settings, 'CDNX_PRODUCTS_FORCE_STOCK', True)
        return self.initial

    def form_valid(self, form, forms):
        pass_to_final = form.cleaned_data.get('pass_to_final')
        ean13 = form.cleaned_data.get('ean13')
        if pass_to_final:
            try:
                with transaction.atomic():
                    result = super(ProductCreateCustom, self).form_valid(form, forms)
                    self.object.pass_to_productfinal(ean13=ean13)
            except IntegrityError as e:
                errors = form._errors.setdefault("code", ErrorList())
                errors.append(e)
                temp_forms = [tform[0] for tform in forms]
                return self.form_invalid(form, temp_forms, 1, 1)
            return result
        else:
            return super(ProductCreateCustom, self).form_valid(form, forms)


class ProductFinalUpdate(GenProductFinalUrl, MultiForm, GenUpdate):
    model = ProductFinal
    show_details = True
    form_class = ProductFinalForm
    forms = formsfull['ProductFinal']


class ProductFinalUpdateModal(GenUpdateModal, ProductFinalUpdate):
    pass


class ProductFinalDelete(GenProductFinalUrl, GenDelete):
    model = ProductFinal


class ProductFinalDetails(GenProductFinalUrl, GenDetail):
    model = ProductFinal
    groups = ProductFinalForm.__groups_details__()
    template_model = "codenerix_products/productfinal_details.html"
    tabs = [
        {'id': 'Attributes', 'name': _('Attributes'), 'ws': 'CDNX_products_productfinalattributes_sublist', 'rows': 'base'},
        {'id': 'Images', 'name': _('Images'), 'ws': 'CDNX_products_productfinalimages_sublist', 'rows': 'base'},
        {'id': 'FeatureSpecial', 'name': _('Feature Special'), 'ws': 'CDNX_products_productuniques_sublist', 'rows': 'base'},
        {'id': 'Product', 'name': _('Product related'), 'ws': 'CDNX_products_productfinalrelateds_sublist', 'rows': 'base'},
        {'id': 'Accesory', 'name': _('Product accesory'), 'ws': 'CDNX_products_productfinalaccesory_sublist', 'rows': 'base'},
        {'id': 'Options', 'name': _('Product options'), 'ws': 'CDNX_products_productfinaloptions_sublist', 'rows': 'base'},
    ]
    exclude_fields = ['related', 'related_accesory']


class ProductFinalDetailsModal(GenProductDocumentUrl, GenDetailModal, ProductFinalDetails):
    pass


class ProductFinalFullinfo(GenProductFinalUrl, GenDetail):
    model = ProductFinal
    groups = ProductFinalForm.__groups_details__()
    template_model = "codenerix_products/productfinal_details.html"
    exclude_fields = ['related', 'related_accesory']
    json = True


class ProductFinalSubList(GenProductFinalUrl, GenList):
    model = ProductFinal

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(product__pk=pk)
        return limit

    def __fields__(self, info):
        fields = []
        fields.append(('id', _("Identifier")))
        fields.append(('products_final_attr', _("Attributes")))
        fields.append(('outstanding', _("Outstanding")))
        fields.append(('most_sold', _("Most sold")))
        for lang in settings.LANGUAGES_DATABASES:
            fields.append(('{}__public'.format(lang.lower()), _("Public {}".format(lang))))
        return fields

    def json_builder(self, answer, context):
        answer['table']['head']['url_products'] = settings.CDNX_PRODUCTS_URL
        answer['table']['head']['columns_lang'] = ["{}__public".format(lang.lower()) for lang in settings.LANGUAGES_DATABASES]
        return answer


class ProductFinalEAN13Foreign(GenForeignKey):
    model = ProductFinal
    label = "{ean13} - {code} - {product__code}"

    def custom_choice(self, obj, info):
        info['price'] = float(obj.price)
        info['tax'] = float(obj.product.tax.tax)
        return info

    def get_foreign(self, queryset, search, filters):
        qs = queryset.filter(
            Q(ean13__icontains=search) | Q(code__icontains=search) | Q(product__code__icontains=search)
        ).all()
        box = filters.get('box', None)
        if box:
            qs = qs.filter(products_unique__box__pk=box)
        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


class ProductFinalForeign(GenProductFinalUrl, GenForeignKey):
    model = ProductFinal
    label = "{product}"

    def __filter_product__(self, search, conditional=None):
        queryset = ProductFinal.objects.filter(sample=False)
        if search != '*':
            qsobject = Q(product__code__icontains=search)
            qsobject |= Q(product__family__code__icontains=search)
            qsobject |= Q(product__category__code__icontains=search)

            for lang in settings.LANGUAGES_DATABASES:
                qsobject |= Q(**{"product__{}__description_short__icontains".format(lang.lower()): search})
                qsobject |= Q(**{"product__family__{}__name__icontains".format(lang.lower()): search})
                qsobject |= Q(**{"product__category__{}__name__icontains".format(lang.lower()): search})

            qs = queryset.filter(qsobject)
            if conditional:
                qs.filter(**conditional)
        elif conditional:
            qs = queryset.filter(**conditional)

        answer = {}
        answer['rows'] = []
        answer['clear'] = ['price', 'type_tax']
        answer['readonly'] = ['price', 'type_tax']
        if self.request.GET.get('def', "0") == "1":
            answer['rows'].append({
                'price': 0,
                'price_base': 0,
                'description': '',
                'type_tax': '0',
                'tax': 0,
                'label': "---------",
                'id': None,
                # 'options': None,
            })
        for product in qs.distinct()[:settings.LIMIT_FOREIGNKEY]:
            pack = []
            lang = get_language_database()
            if product.productfinals_option.filter(active=True).exists():
                for option in product.productfinals_option.filter(active=True):
                    pack.append({
                        'id': option.pk,
                        'label': getattr(option, lang).name,
                        'products': list(option.products_pack.all().values('pk').annotate(name=F('{}__name'.format(lang))))
                    })
            answer['rows'].append({
                'price': str(product.price),
                'price_base': str(product.product.price_base),
                'description': product.__unicode__(),
                'type_tax': product.product.tax.pk,
                'type_tax__pk': product.product.tax.pk,
                'tax': product.product.tax.tax,
                'label': u"{}".format(product.__unicode__()),
                'id': product.pk,
                'packs:__JSON_DATA__': json.dumps(pack),
            })

        try:
            json_answer = json.dumps(answer)
        except TypeError:
            raise TypeError("The structure can not be encoded to JSON")
        # Return the new answer
        return HttpResponse(json_answer, content_type='application/json')


class ProductFinalForeignSales(ProductFinalForeign):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)
        return self.__filter_product__(search, {'product__of_sales': True, 'productfinals_option__isnull': True})


class ProductFinalForeignPackSales(ProductFinalForeign):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)
        return self.__filter_product__(search, {'product__of_sales': True, 'productfinals_option__isnull': False})


class ProductFinalForeignAllSales(ProductFinalForeign):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)
        return self.__filter_product__(search, {'product__of_sales': True})


class ProductFinalForeignPurchases(ProductFinalForeign):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)
        return self.__filter_product__(search, {'product__of_purchase': True, 'productfinals_option__isnull': True})


class ProductFinalForeignPackPurchases(ProductFinalForeign):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)
        return self.__filter_product__(search, {'product__of_purchase': True, 'productfinals_option__isnull': False})


class ProductFinalForeignAllPurchases(ProductFinalForeign):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        search = kwargs.get('search', None)
        return self.__filter_product__(search, {'product__of_purchase': True})


# ------- sublista de productos relacionados -------
class ProductFinalRelatedSubList(GenProductFinalUrl, GenList):
    model = ProductFinal

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(productsrelated__pk=pk)
        return limit


class ProductFinalRelatedSubUpdateModal(GenProductFinalUrl, GenUpdateModal):
    model = ProductFinal
    form_class = ProductFinalRelatedSubForm
    linkdelete = False

    def form_valid(self, form):
        new_product = form.cleaned_data.get('new_product')

        if form.instance.pk != new_product.pk and not form.instance.related.filter(pk=new_product.pk):
            form.instance.related.add(new_product)

        return super(ProductFinalRelatedSubUpdateModal, self).form_valid(form)


class ProductFinalRelatedSubDelete(View):
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        product_delete_pk = kwargs.get('pk', None)
        product_pk = kwargs.get('tpk', None)

        if product_pk and product_delete_pk:
            product_delete = ProductFinal.objects.filter(pk=product_delete_pk).first()
            product = ProductFinal.objects.filter(pk=product_pk).first()
            if product and product_delete:
                product.related.remove(product_delete)

        return redirect(reverse_lazy("status", kwargs={'status': 'accept', 'answer': urlsafe_base64_encode(json.dumps({'__pk__': None, '__str__': 'OK'}))}))


# ------- sublista de accesorios productos -------
class ProductFinalAccesorySubList(GenProductFinalUrl, GenList):
    model = ProductFinal

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(productsrelatedaccesory__pk=pk)
        return limit


class ProductFinalAccesorySubUpdateModal(GenProductFinalUrl, GenUpdateModal):
    model = ProductFinal
    form_class = ProductFinalRelatedSubForm
    linkdelete = False

    def form_valid(self, form):
        new_product = form.cleaned_data.get('new_product')

        if form.instance.pk != new_product.pk and not form.instance.related_accesory.filter(pk=new_product.pk):
            form.instance.related_accesory.add(new_product)

        return super(ProductFinalAccesorySubUpdateModal, self).form_valid(form)


class ProductFinalAccesorySubDelete(View):
    @method_decorator(login_required)
    def post(self, *args, **kwargs):
        product_delete_pk = kwargs.get('pk', None)
        product_pk = kwargs.get('tpk', None)

        if product_pk and product_delete_pk:
            product_delete = ProductFinal.objects.filter(pk=product_delete_pk).first()
            product = ProductFinal.objects.filter(pk=product_pk).first()
            if product and product_delete:
                product.related_accesory.remove(product_delete)

        return redirect(reverse_lazy("status", kwargs={'status': 'accept', 'answer': urlsafe_base64_encode(json.dumps({'__pk__': None, '__str__': 'OK'}))}))


# ###########################################
class GenProductFinalImageUrl(object):
    ws_entry_point = '{}/productfinalimages'.format(settings.CDNX_PRODUCTS_URL)


# ProductImage
class ProductFinalImageList(GenProductFinalImageUrl, GenList):
    model = ProductFinalImage
    extra_context = {
        'menu': ['ProductImage', 'people'],
        'bread': [_('ProductImage'), _('People')]
    }


class ProductFinalImageCreate(GenProductFinalImageUrl, ImageFileView, MultiForm, GenCreate):
    model = ProductFinalImage
    form_class = ProductFinalImageForm
    forms = formsfull["ProductFinalImage"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__group_pk = kwargs.get('cpk', None)
        return super(ProductFinalImageCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__group_pk:
            product_final = ProductFinal.objects.get(pk=self.__group_pk)
            self.request.product_final = product_final
            form.instance.product_final = product_final

        return super(ProductFinalImageCreate, self).form_valid(form, forms)


class ProductFinalImageCreateModal(GenCreateModal, ProductFinalImageCreate):
    pass


class ProductFinalImageUpdate(GenProductFinalImageUrl, ImageFileView, MultiForm, GenUpdate):
    model = ProductFinalImage
    form_class = ProductFinalImageForm
    forms = formsfull["ProductImage"]


class ProductFinalImageUpdateModal(GenUpdateModal, ProductFinalImageUpdate):
    pass


class ProductFinalImageDelete(GenProductFinalImageUrl, GenDelete):
    model = ProductFinalImage


class ProductFinalImageSubList(GenProductFinalImageUrl, GenList):
    model = ProductFinalImage
    annotations = {
        'image_path': Concat(Value(settings.MEDIA_URL), 'image'),
    }

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(product_final__pk=pk)
        return limit

    def __fields__(self, info):
        fields = []
        fields.append(('order', _("Order")))
        fields.append(('public', _("Public")))
        fields.append(('principal', _("Principal")))
        fields.append(('image', _("Image"), None, None, 'image:width:66px'))
        return fields


class ProductFinalImageDetails(GenProductFinalImageUrl, GenDetail):
    model = ProductFinalImage
    groups = ProductFinalImageForm.__groups_details__()


class ProductFinalImageDetailsModal(GenDetailModal, ProductFinalImageDetails):
    pass


# ###########################################
class GenProductFinalAttributeUrl(object):
    ws_entry_point = '{}/productfinalattributes'.format(settings.CDNX_PRODUCTS_URL)


# ProductFinalAttribute
class ProductFinalAttributeList(GenProductFinalAttributeUrl, GenList):
    model = ProductFinalAttribute
    show_details = True
    extra_context = {
        'menu': ['ProductFinalAttribute', 'people'],
        'bread': [_('ProductFinalAttribute'), _('People')]
    }


class ProductFinalAttributeCreate(GenProductFinalAttributeUrl, GenCreate):
    model = ProductFinalAttribute
    form_class = ProductFinalAttributeForm
    form_ngcontroller = "CDNXPRODUCTSFormProductAttributeCtrl"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_pk = kwargs.get('cpk', None)
        return super(ProductFinalAttributeCreate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ProductFinalAttributeCreate, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['product_pk'] = self.__product_pk
        return form_kwargs

    def form_valid(self, form):
        attribute = form.cleaned_data['attribute']

        if attribute.type_value == TYPE_VALUE_BOOLEAN:
            value = int(form.cleaned_data['value_bool'])
        elif attribute.type_value == TYPE_VALUE_FREE:
            value = form.cleaned_data['value_free']
        elif attribute.type_value == TYPE_VALUE_LIST:
            value = form.cleaned_data['value_list']
            if not OptionValueAttribute.objects.filter(
                pk=value, group__attributes=attribute
            ).exists():
                errors = form._errors.setdefault("value", ErrorList())
                errors.append(_('Option invalid'))
                return super(ProductFeatureCreate, self).form_invalid(form)
        else:
            value = None

        if value is None:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(_('Value invalid'))
            return super(ProductFeatureCreate, self).form_invalid(form)

        self.request.value = value
        form.instance.value = value

        if self.__product_pk:
            product = ProductFinal.objects.get(pk=self.__product_pk)
            self.request.product = product
            form.instance.product = product

        return super(ProductFinalAttributeCreate, self).form_valid(form)

    def form_validXXX(self, form):
        if self.__product_pk:
            product = ProductFinal.objects.get(pk=self.__product_pk)
            self.request.product = product
            form.instance.product = product

        return super(ProductFinalAttributeCreate, self).form_valid(form)


class ProductFinalAttributeCreateModal(GenCreateModal, ProductFinalAttributeCreate):
    pass


class ProductFinalAttributeUpdate(GenProductFinalAttributeUrl, GenUpdate):
    model = ProductFinalAttribute
    form_class = ProductFinalAttributeForm
    form_ngcontroller = "CDNXPRODUCTSFormProductAttributeCtrl"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_pk = kwargs.get('cpk', None)
        return super(ProductFinalAttributeUpdate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ProductFinalAttributeUpdate, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['product_pk'] = self.__product_pk
        if form_kwargs['instance'].attribute.type_value == TYPE_VALUE_FREE:
            form_kwargs['value_free'] = form_kwargs['instance'].value
        elif form_kwargs['instance'].attribute.type_value == TYPE_VALUE_BOOLEAN:
            form_kwargs['value_bool'] = form_kwargs['instance'].value
        elif form_kwargs['instance'].attribute.type_value == TYPE_VALUE_LIST:
            form_kwargs['value_list'] = form_kwargs['instance'].value
        return form_kwargs

    def form_valid(self, form):
        attribute = form.cleaned_data['attribute']

        if attribute.type_value == TYPE_VALUE_BOOLEAN:
            value = int(form.cleaned_data['value_bool'])
        elif attribute.type_value == TYPE_VALUE_FREE:
            value = form.cleaned_data['value_free']
        elif attribute.type_value == TYPE_VALUE_LIST:
            value = form.cleaned_data['value_list']
            if not OptionValueAttribute.objects.filter(
                pk=value, group__attributes=attribute
            ).exists():
                errors = form._errors.setdefault("value", ErrorList())
                errors.append(_('Option invalid'))
                return super(ProductFinalAttributeUpdate, self).form_invalid(form)
        else:
            value = None

        if value is None:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(_('Value invalid'))
            return super(ProductFinalAttributeUpdate, self).form_invalid(form)

        self.request.value = value
        form.instance.value = value
        return super(ProductFinalAttributeUpdate, self).form_valid(form)


class ProductFinalAttributeUpdateModal(GenUpdateModal, ProductFinalAttributeUpdate):
    pass


class ProductFinalAttributeDelete(GenProductFinalAttributeUrl, GenDelete):
    model = ProductFinalAttribute


class ProductFinalAttributeSubList(GenProductFinalAttributeUrl, GenList):
    model = ProductFinalAttribute
    default_ordering = ['attribute', ]

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(product__pk=pk)
        return limit


class ProductFinalAttributeDetails(GenProductFinalAttributeUrl, GenDetail):
    model = ProductFinalAttribute
    groups = ProductFinalAttributeForm.__groups_details__()
    exclude_fields = ["product", "product_pk", ]


class ProductFinalAttributeDetailsModal(GenDetailModal, ProductFinalAttributeDetails):
    pass


# ###########################################
class GenProductFeatureUrl(object):
    ws_entry_point = '{}/productfeatures'.format(settings.CDNX_PRODUCTS_URL)


# ProductFeature
class ProductFeatureList(GenList):
    model = ProductFeature
    extra_context = {
        'menu': ['ProductFeature', 'people'],
        'bread': [_('ProductFeature'), _('People')]
    }


class ProductFeatureCreate(GenCreate):
    model = ProductFeature
    form_class = ProductFeatureForm
    form_ngcontroller = "CDNXPRODUCTSFormProductFeatureCtrl"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_pk = kwargs.get('cpk', None)
        return super(ProductFeatureCreate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ProductFeatureCreate, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['product_pk'] = self.__product_pk
        return form_kwargs

    def form_valid(self, form):
        feature = form.cleaned_data['feature']

        if feature.type_value == TYPE_VALUE_BOOLEAN:
            value = int(form.cleaned_data['value_bool'])
        elif feature.type_value == TYPE_VALUE_FREE:
            value = form.cleaned_data['value_free']
        elif feature.type_value == TYPE_VALUE_LIST:
            value = form.cleaned_data['value_list']
            if not OptionValueFeature.objects.filter(
                pk=value, group__features=feature
            ).exists():
                errors = form._errors.setdefault("value", ErrorList())
                errors.append(_('Option invalid'))
                return super(ProductFeatureCreate, self).form_invalid(form)
        else:
            value = None

        if value is None:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(_('Value invalid'))
            return super(ProductFeatureCreate, self).form_invalid(form)

        self.request.value = value
        form.instance.value = value

        if self.__product_pk:
            product = Product.objects.get(pk=self.__product_pk)
            self.request.product = product
            form.instance.product = product

        return super(ProductFeatureCreate, self).form_valid(form)


class ProductFeatureCreateModal(GenCreateModal, ProductFeatureCreate):
    pass


class ProductFeatureUpdate(GenUpdate):
    model = ProductFeature
    form_class = ProductFeatureForm
    form_ngcontroller = "CDNXPRODUCTSFormProductFeatureCtrl"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_pk = kwargs.get('cpk', None)
        return super(ProductFeatureUpdate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ProductFeatureUpdate, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['product_pk'] = self.__product_pk
        if form_kwargs['instance'].feature.type_value == TYPE_VALUE_FREE:
            form_kwargs['value_free'] = form_kwargs['instance'].value
        elif form_kwargs['instance'].feature.type_value == TYPE_VALUE_BOOLEAN:
            form_kwargs['value_bool'] = form_kwargs['instance'].value
        elif form_kwargs['instance'].feature.type_value == TYPE_VALUE_LIST:
            form_kwargs['value_list'] = form_kwargs['instance'].value
        return form_kwargs

    def form_valid(self, form):
        feature = form.cleaned_data['feature']

        if feature.type_value == TYPE_VALUE_BOOLEAN:
            value = int(form.cleaned_data['value_bool'])
        elif feature.type_value == TYPE_VALUE_FREE:
            value = form.cleaned_data['value_free']
        elif feature.type_value == TYPE_VALUE_LIST:
            value = form.cleaned_data['value_list']
            if not OptionValueFeature.objects.filter(
                pk=value, group__features=feature
            ).exists():
                errors = form._errors.setdefault("value", ErrorList())
                errors.append(_('Option invalid'))
                return super(ProductFeatureUpdate, self).form_invalid(form)
        else:
            value = None

        if value is None:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(_('Value invalid'))
            return super(ProductFeatureUpdate, self).form_invalid(form)

        self.request.value = value
        form.instance.value = value
        return super(ProductFeatureUpdate, self).form_valid(form)


class ProductFeatureUpdateModal(GenUpdateModal, ProductFeatureUpdate):
    pass


class ProductFeatureDelete(GenDelete):
    model = ProductFeature


class ProductFeatureSubList(GenList):
    model = ProductFeature

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(product__pk=pk)
        return limit


class ProductFeatureDetails(GenProductFeatureUrl, GenDetail):
    model = ProductFeature
    groups = ProductFeatureForm.__groups_details__()


class ProductFeatureDetailsModal(GenDetailModal, ProductFeatureDetails):
    pass


# ###########################################
class GenProductUniqueUrl(object):
    ws_entry_point = '{}/productuniques'.format(settings.CDNX_PRODUCTS_URL)


# ProductUnique
class ProductUniqueList(GenProductUniqueUrl, GenList):
    model = ProductUnique
    extra_context = {
        'menu': ['ProductUnique', 'people'],
        'bread': [_('ProductUnique'), _('People')]
    }


class ProductUniqueCreate(GenProductUniqueUrl, GenCreate):
    model = ProductUnique
    form_class = ProductUniqueForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_pk = kwargs.get('cpk', None)
        return super(ProductUniqueCreate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ProductUniqueCreate, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['product_pk'] = self.__product_pk
        return form_kwargs

    def form_valid(self, form):
        if self.__product_pk:
            product_final = ProductFinal.objects.get(pk=self.__product_pk)
            self.request.product_final = product_final
            form.instance.product_final = product_final

        try:
            return super(ProductUniqueCreate, self).form_valid(form)
        except ValidationError as e:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(e)
            return super(ProductUniqueCreate, self).form_invalid(form)
        except IntegrityError:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(_("Value existing"))
            return super(ProductUniqueCreate, self).form_invalid(form)


class ProductUniqueCreateModal(GenCreateModal, ProductUniqueCreate):
    pass


class ProductUniqueUpdate(GenProductUniqueUrl, GenUpdate):
    model = ProductUnique
    form_class = ProductUniqueForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_pk = kwargs.get('cpk', None)
        return super(ProductUniqueUpdate, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ProductUniqueUpdate, self).get_form_kwargs(*args, **kwargs)
        form_kwargs['product_pk'] = self.__product_pk
        return form_kwargs

    def form_valid(self, form):
        try:
            return super(ProductUniqueUpdate, self).form_valid(form)
        except ValidationError as e:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(e)
            return super(ProductUniqueUpdate, self).form_invalid(form)
        except IntegrityError:
            errors = form._errors.setdefault("value", ErrorList())
            errors.append(_("Value existing"))
            return super(ProductUniqueUpdate, self).form_invalid(form)


class ProductUniqueUpdateModal(GenUpdateModal, ProductUniqueUpdate):
    pass


class ProductUniqueDelete(GenProductUniqueUrl, GenDelete):
    model = ProductUnique


class ProductUniqueSubList(GenProductUniqueUrl, GenList):
    model = ProductUnique

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(product_final__pk=pk)
        return limit


class ProductUniqueDetails(GenProductUniqueUrl, GenDetail):
    model = ProductUnique
    groups = ProductUniqueForm.__groups_details__()


class ProductUniqueDetailsModal(GenDetailModal, ProductUniqueDetails):
    pass


class ProductUniqueCodeForeign(GenForeignKey):
    model = ProductUnique
    label = "{value}"

    def get_foreign(self, queryset, search, filters):
        product_final = "1"
        qs = queryset.filter(product_final__pk=product_final, value__icontains=search).all()
        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


class ProductUniqueForeign(GenForeignKey):
    model = ProductUnique
    label = "{value}"

    def get_foreign(self, queryset, search, filters):
        # Filter with search string

        queryset = queryset.all()
        product_final = filters.get('product', None)

        if product_final:
            pf = ProductFinal.objects.filter(pk=product_final).first()
            if pf:
                if pf.product.feature_special:
                    if pf.product.feature_special.type_value == TYPE_VALUE_FREE:
                        queryset = queryset.filter(Q(value__icontains=search))
                    elif pf.product.feature_special.type_value == TYPE_VALUE_LIST:
                        for lang_code in settings.LANGUAGES_DATABASES:
                            queryset = queryset.filter(
                                Q(**{
                                    'pf__product__feature_special__list_value__options_value_feature_special__{}__option_value__icontains'.format(lang_code.lower()): search
                                })
                            )

            queryset = queryset.filter(
                Q(product_final__pk=product_final)
            )
        return queryset


# ############################################
class GenGroupValueFeatureUrl(object):
    ws_entry_point = '{}/groupvaluefeatures'.format(settings.CDNX_PRODUCTS_URL)


# GroupValueFeature
class GroupValueFeatureList(GenGroupValueFeatureUrl, GenList):
    model = GroupValueFeature
    show_details = True
    extra_context = {
        'menu': ['GroupValueFeature', 'people'],
        'bread': [_('GroupValueFeature'), _('People')]
    }


class GroupValueFeatureCreate(GenGroupValueFeatureUrl, GenCreate):
    model = GroupValueFeature
    show_details = True
    form_class = GroupValueFeatureForm


class GroupValueFeatureCreateModal(GenCreateModal, GroupValueFeatureCreate):
    pass


class GroupValueFeatureUpdate(GenGroupValueFeatureUrl, GenUpdate):
    model = GroupValueFeature
    show_details = True
    form_class = GroupValueFeatureForm


class GroupValueFeatureUpdateModal(GenUpdateModal, GroupValueFeatureUpdate):
    """
    Next version, update and sublist
    """
    # template_model = "codenerix_products/groupvaluefeature_formmodal.html"
    tabs = [
        {
            'id': 'Values',
            'name': _('List values'),
            'ws': 'CDNX_products_OptionValueFeatures_sublist_modal',
            'wsbase': 'CDNX_products_OptionValueFeatures_list',
            'rows': 'base'
        },
    ]


class GroupValueFeatureDelete(GenGroupValueFeatureUrl, GenDelete):
    model = GroupValueFeature


class GroupValueFeatureDetails(GenGroupValueFeatureUrl, GenDetail):
    model = GroupValueFeature
    groups = GroupValueFeatureForm.__groups_details__()
    template_model = "codenerix_products/groupvaluefeature_details.html"
    tabs = [
        {
            'id': 'Values',
            'name': _('List values'),
            'ws': 'CDNX_products_OptionValueFeatures_sublist',
            'wsbase': 'CDNX_products_OptionValueFeatures_list',
            'rows': 'base'
        },
    ]


# ############################################
class GenGroupValueAttributeUrl(object):
    ws_entry_point = '{}/groupvalueattributes'.format(settings.CDNX_PRODUCTS_URL)


# GroupValueAttribute
class GroupValueAttributeList(GenGroupValueAttributeUrl, GenList):
    model = GroupValueAttribute
    show_details = True
    extra_context = {
        'menu': ['GroupValueAttribute', 'people'],
        'bread': [_('GroupValueAttribute'), _('People')]
    }


class GroupValueAttributeCreate(GenGroupValueAttributeUrl, GenCreate):
    model = GroupValueAttribute
    show_details = True
    form_class = GroupValueAttributeForm


class GroupValueAttributeCreateModal(GenCreateModal, GroupValueAttributeCreate):
    pass


class GroupValueAttributeUpdate(GenGroupValueAttributeUrl, GenUpdate):
    model = GroupValueAttribute
    show_details = True
    form_class = GroupValueAttributeForm


class GroupValueAttributeUpdateModal(GenUpdateModal, GroupValueAttributeUpdate):
    """
    Next version, update and sublist
    """
    # template_model = "codenerix_products/groupvalueattribute_formmodal.html"
    tabs = [
        {
            'id': 'Values',
            'name': _('List values'),
            'ws': 'CDNX_products_OptionValueAttributes_sublist_modal',
            'wsbase': 'CDNX_products_OptionValueAttributes_list',
            'rows': 'base'
        },
    ]


class GroupValueAttributeDelete(GenGroupValueAttributeUrl, GenDelete):
    model = GroupValueAttribute


class GroupValueAttributeDetails(GenGroupValueAttributeUrl, GenDetail):
    model = GroupValueAttribute
    groups = GroupValueAttributeForm.__groups_details__()
    template_model = "codenerix_products/GroupValueAttribute_details.html"
    tabs = [
        {
            'id': 'Values',
            'name': _('List values'),
            'ws': 'CDNX_products_OptionValueAttributes_sublist',
            'wsbase': 'CDNX_products_OptionValueAttributes_list',
            'rows': 'base'
        },
    ]


# ############################################
class GenGroupValueFeatureSpecialUrl(object):
    ws_entry_point = '{}/groupvaluefeaturespecials'.format(settings.CDNX_PRODUCTS_URL)


# GroupValueFeatureSpecial
class GroupValueFeatureSpecialList(GenGroupValueFeatureSpecialUrl, GenList):
    model = GroupValueFeatureSpecial
    show_details = True
    extra_context = {
        'menu': ['GroupValueFeatureSpecial', 'people'],
        'bread': [_('GroupValueFeatureSpecial'), _('People')]
    }


class GroupValueFeatureSpecialCreate(GenGroupValueFeatureSpecialUrl, GenCreate):
    model = GroupValueFeatureSpecial
    form_class = GroupValueFeatureSpecialForm


class GroupValueFeatureSpecialCreateModal(GenCreateModal, GroupValueFeatureSpecialCreate):
    pass


class GroupValueFeatureSpecialUpdate(GenGroupValueFeatureSpecialUrl, GenUpdate):
    model = GroupValueFeatureSpecial
    show_details = True
    form_class = GroupValueFeatureSpecialForm


class GroupValueFeatureSpecialUpdateModal(GenUpdateModal, GroupValueFeatureSpecialUpdate):
    """
    Next version, update and sublist
    """
    # template_model = "codenerix_products/groupvaluefeaturespecial_formmodal.html"
    tabs = [
        {
            'id': 'Values',
            'name': _('List values'),
            'ws': 'CDNX_products_OptionValueFeatureSpecials_sublist_modal',
            'wsbase': 'CDNX_products_OptionValueFeatureSpecials_list',
            'rows': 'base'
        },
    ]


class GroupValueFeatureSpecialDelete(GenGroupValueFeatureSpecialUrl, GenDelete):
    model = GroupValueFeatureSpecial


class GroupValueFeatureSpecialDetails(GenGroupValueFeatureSpecialUrl, GenDetail):
    model = GroupValueFeatureSpecial
    groups = GroupValueFeatureSpecialForm.__groups_details__()
    template_model = "codenerix_products/GroupValueFeatureSpecial_details.html"
    tabs = [
        {
            'id': 'Values',
            'name': _('List values'),
            'ws': 'CDNX_products_OptionValueFeatureSpecials_sublist',
            'wsbase': 'CDNX_products_OptionValueFeatureSpecials_list',
            'rows': 'base'
        },
    ]


# ############################################
class GenOptionValueFeatureUrl(object):
    ws_entry_point = '{}/optionvaluefeatures'.format(settings.CDNX_PRODUCTS_URL)


# OptionValueFeature
class OptionValueFeatureList(GenOptionValueFeatureUrl, GenList):
    model = OptionValueFeature
    extra_context = {
        'menu': ['OptionValueFeature', 'people'],
        'bread': [_('OptionValueFeature'), _('People')]
    }


class OptionValueFeatureCreate(GenOptionValueFeatureUrl, MultiForm, GenCreate):
    model = OptionValueFeature
    form_class = OptionValueFeatureForm
    forms = formsfull["OptionValueFeature"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__group_pk = kwargs.get('gpk', None)
        return super(OptionValueFeatureCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__group_pk:
            group = GroupValueFeature.objects.get(pk=self.__group_pk)
            self.request.group = group
            form.instance.group = group

        return super(OptionValueFeatureCreate, self).form_valid(form, forms)


class OptionValueFeatureCreateModal(GenCreateModal, OptionValueFeatureCreate):
    pass


class OptionValueFeatureUpdate(GenOptionValueFeatureUrl, MultiForm, GenUpdate):
    model = OptionValueFeature
    form_class = OptionValueFeatureForm
    forms = formsfull["OptionValueFeature"]


class OptionValueFeatureUpdateModal(GenUpdateModal, OptionValueFeatureUpdate):
    pass


class OptionValueFeatureDelete(GenOptionValueFeatureUrl, GenDelete):
    model = OptionValueFeature


class OptionValueFeatureSubList(GenOptionValueFeatureUrl, GenList):
    model = OptionValueFeature

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(group__pk=pk)
        return limit


class OptionValueFeatureSubListModal(OptionValueFeatureSubList):
    json = False
    template_model = "codenerix_products/optionvaluefeature_sublist.html"


class OptionValueFeatureDetails(GenOptionValueFeatureUrl, GenDetail):
    model = OptionValueFeature
    groups = OptionValueFeatureForm.__groups_details__()


class OptionValueFeatureDetailsModal(GenDetailModal, OptionValueFeatureDetails):
    pass


class OptionValueFeatureForeign(GenOptionValueFeatureUrl, GenForeignKey):
    model = OptionValueFeature
    label = "{<LANGUAGE_CODE>__description}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.all()
        # product_pk = filters.get('product_pk', None)
        feature_pk = filters.get('feature', None)

        # if product_pk:
        #     qs = qs.filter(group__features__product_features__product__pk=product_pk)
        if feature_pk:
            qs = qs.filter(group__features__pk=feature_pk)

        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


# ############################################
class GenOptionValueAttributeUrl(object):
    ws_entry_point = '{}/optiovalueattributes'.format(settings.CDNX_PRODUCTS_URL)


# OptionValueAttribute
class OptionValueAttributeList(GenOptionValueAttributeUrl, GenList):
    model = OptionValueAttribute
    extra_context = {
        'menu': ['OptionValueAttribute', 'people'],
        'bread': [_('OptionValueAttribute'), _('People')]
    }


class OptionValueAttributeCreate(GenOptionValueAttributeUrl, MultiForm, GenCreate):
    model = OptionValueAttribute
    form_class = OptionValueAttributeForm
    forms = formsfull["OptionValueAttribute"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__group_pk = kwargs.get('gpk', None)
        return super(OptionValueAttributeCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__group_pk:
            group = GroupValueAttribute.objects.get(pk=self.__group_pk)
            self.request.group = group
            form.instance.group = group

        return super(OptionValueAttributeCreate, self).form_valid(form, forms)


class OptionValueAttributeCreateModal(GenCreateModal, OptionValueAttributeCreate):
    pass


class OptionValueAttributeUpdate(GenOptionValueAttributeUrl, MultiForm, GenUpdate):
    model = OptionValueAttribute
    form_class = OptionValueAttributeForm
    forms = formsfull["OptionValueAttribute"]


class OptionValueAttributeUpdateModal(GenUpdateModal, OptionValueAttributeUpdate):
    pass


class OptionValueAttributeDelete(GenOptionValueAttributeUrl, GenDelete):
    model = OptionValueAttribute


class OptionValueAttributeSubList(GenOptionValueAttributeUrl, GenList):
    model = OptionValueAttribute

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(group__pk=pk)
        return limit


class OptionValueAttributeSubListModal(OptionValueAttributeSubList):
    json = False
    template_model = "codenerix_products/optionvalueattribute_sublist.html"


class OptionValueAttributeDetails(GenOptionValueAttributeUrl, GenDetail):
    model = OptionValueAttribute
    groups = OptionValueAttributeForm.__groups_details__()


class OptionValueAttributeDetailsModal(GenDetailModal, OptionValueAttributeDetails):
    pass


class OptionValueAttributeForeign(GenOptionValueAttributeUrl, GenForeignKey):
    model = OptionValueAttribute
    label = "{<LANGUAGE_CODE>__description}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.all()
        # product_pk = filters.get('product_pk', None)
        attribute_pk = filters.get('attribute', None)

        # if product_pk:
        #     qs = qs.filter(group__features__product_features__product__pk=product_pk)
        if attribute_pk:
            qs = qs.filter(group__attributes__pk=attribute_pk)

        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


# ############################################
class GenOptionValueFeatureSpecialUrl(object):
    ws_entry_point = '{}/optionvaluefeaturespecials'.format(settings.CDNX_PRODUCTS_URL)


# OptionValueFeatureSpecial
class OptionValueFeatureSpecialList(GenOptionValueFeatureSpecialUrl, GenList):
    model = OptionValueFeatureSpecial
    extra_context = {
        'menu': ['OptionValueFeatureSpecial', 'people'],
        'bread': [_('OptionValueFeatureSpecial'), _('People')]
    }


class OptionValueFeatureSpecialCreate(GenOptionValueFeatureSpecialUrl, MultiForm, GenCreate):
    model = OptionValueFeatureSpecial
    form_class = OptionValueFeatureSpecialForm
    forms = formsfull["OptionValueFeatureSpecial"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__group_pk = kwargs.get('gpk', None)
        return super(OptionValueFeatureSpecialCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form, forms):
        if self.__group_pk:
            group = GroupValueFeatureSpecial.objects.get(pk=self.__group_pk)
            self.request.group = group
            form.instance.group = group

        return super(OptionValueFeatureSpecialCreate, self).form_valid(form, forms)


class OptionValueFeatureSpecialCreateModal(GenCreateModal, OptionValueFeatureSpecialCreate):
    pass


class OptionValueFeatureSpecialUpdate(GenOptionValueFeatureSpecialUrl, MultiForm, GenUpdate):
    model = OptionValueFeatureSpecial
    form_class = OptionValueFeatureSpecialForm
    forms = formsfull["OptionValueFeatureSpecial"]


class OptionValueFeatureSpecialUpdateModal(GenUpdateModal, OptionValueFeatureSpecialUpdate):
    pass


class OptionValueFeatureSpecialDelete(GenOptionValueFeatureSpecialUrl, GenDelete):
    model = OptionValueFeatureSpecial


class OptionValueFeatureSpecialSubList(GenOptionValueFeatureSpecialUrl, GenList):
    model = OptionValueFeatureSpecial

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['file_link'] = Q(group__pk=pk)
        return limit


class OptionValueFeatureSpecialSubListModal(OptionValueFeatureSpecialSubList):
    json = False
    template_model = "codenerix_products/optionvaluefeaturespecial_sublist.html"


class OptionValueFeatureSpecialDetails(GenOptionValueFeatureSpecialUrl, GenDetail):
    model = OptionValueFeatureSpecial
    groups = OptionValueFeatureSpecialForm.__groups_details__()


class OptionValueFeatureSpecialDetailsModal(GenDetailModal, OptionValueFeatureSpecialDetails):
    pass


class OptionValueFeatureSpecialForeign(GenOptionValueFeatureSpecialUrl, GenForeignKey):
    model = OptionValueFeatureSpecial
    label = "{<LANGUAGE_CODE>__description}"

    def get_foreign(self, queryset, search, filters):
        qs = queryset.all()
        # product_pk = filters.get('product_pk', None)
        feature_pk = filters.get('feature', None)

        # if product_pk:
        #     qs = qs.filter(group__features__product_features__product__pk=product_pk)
        if feature_pk:
            qs = qs.filter(group__features__pk=feature_pk)

        return qs.distinct()[:settings.LIMIT_FOREIGNKEY]


# ############################################
class GenFlagshipProductUrl(object):
    ws_entry_point = '{}/flagshipproducts'.format(settings.CDNX_PRODUCTS_URL)


# Flagship Product
class FlagshipProductList(GenFlagshipProductUrl, GenList):
    model = FlagshipProduct
    default_ordering = ['-public', '-pk']
    extra_context = {
        'menu': ['FlagshipProduct', 'people'],
        'bread': [_('FlagshipProduct'), _('People')]
    }


class FlagshipProductCreate(GenFlagshipProductUrl, ImageFileView, MultiForm, GenCreate):
    model = FlagshipProduct
    form_class = FlagshipProductForm
    forms = formsfull["FlagshipProduct"]


class FlagshipProductCreateModal(GenCreateModal, FlagshipProductCreate):
    pass


class FlagshipProductUpdate(GenFlagshipProductUrl, ImageFileView, MultiForm, GenUpdate):
    model = FlagshipProduct
    form_class = FlagshipProductForm
    forms = formsfull["FlagshipProduct"]


class FlagshipProductUpdateModal(GenUpdateModal, FlagshipProductUpdate):
    pass


class FlagshipProductDelete(GenFlagshipProductUrl, GenDelete):
    model = FlagshipProduct


class ListProducts(GenList):
    public = True
    model = ProductFinal
    gentrans = {
        'buy': _("Buy"),
        'new': _("New"),
        'wishlist': _("Wish list"),
        'shoppingcart': _("Shopping cart"),
    }

    def __fields__(self, info):
        fields = []
        fields.append(('name:es__name', _("Name")))
        fields.append(('slug:es__slug', _("Slug")))
        fields.append(('product__products_image__image', _("Image")))
        fields.append(('product__products_image__principal', _("Principal")))
        fields.append(('productfinals_image__image', _("Image")))
        fields.append(('productfinals_image__principal', _("Principal")))
        fields.append(('price', _("Price")))
        # fields.append(('price_old:price', _("Price")))
        fields.append(('offer', _("Offer")))
        fields.append(('created', _("Created")))
        fields.append(('reviews_value', _("Reviews")))
        fields.append(('reviews_count', _("Reviews count")))
        return fields

    def __limitQ__(self, info):
        limits = {}
        pk = self.kwargs.get('pk', None)
        type_list = self.kwargs.get('type', None)
        # get language
        lang = None
        for x in settings.LANGUAGES:
            if x[0] == self.request.LANGUAGE_CODE:
                lang = self.request.LANGUAGE_CODE.lower()

        if lang is None:
            lang = settings.LANGUAGES[0][0].lower()

        if pk and type_list:
            # aplicamos los filtros recibidos
            params = ast.literal_eval(info.request.GET.get("json"))

            slug_subcategory = None
            if "subcategory" in params and params["subcategory"]:
                if params["subcategory"] != '*':
                    slug_subcategory = params["subcategory"]

            slug_type = None
            if "brand" in params and params["brand"]:
                if params["brand"] != '*':
                    slug_type = params["brand"]

            slug_family = None
            if "family" in params and params["family"]:
                if params["family"] != '*':
                    slug_family = params["family"]

            only_with_stock = None
            # filtramos dependiendo de la url original que estemos visitando
            if type_list == 'SUB':
                only_with_stock = Category.objects.filter(subcategory__pk=pk, show_only_product_stock=True).exists()
                limits['type_list'] = Q(product__subcategory__pk=pk)

            elif type_list == 'CAT':
                limits['type_list'] = Q(product__category__pk=pk)

            elif type_list == 'FAM':
                limits['type_list'] = Q(product__family__pk=pk)

            elif type_list == 'BRAND':
                limits['type_list'] = Q(product__brand__pk=pk)

            elif type_list == 'SEARCH':
                only_with_stock = settings.CDNX_PRODUCTS_SHOW_ONLY_STOCK

            else:
                raise Exception("Pendiente de definir")

            if slug_subcategory:
                limits['by_sucategory'] = Q(**{"product__subcategory__{}__slug".format(lang): slug_subcategory})

            if slug_type:
                limits['by_brand'] = Q(**{"product__brand__{}__slug".format(lang): slug_type})

            if slug_family:
                limits['by_family'] = Q(**{"product__family__{}__slug".format(lang): slug_family})

            # aplicamos los filtros recibidos
            params = ast.literal_eval(info.request.GET.get("json"))
            if "filters" in params and params["filters"]:
                filters = params["filters"]
                if 'brand' in filters and filters['brand']:
                    limits["product__brand"] = Q(product__brand__in=filters['brand'])
                if 'feature' in filters and filters['feature']:
                    for feature in filters['feature']:
                        if feature and filters['feature'][feature]:
                            limits['product__product_features__feature'] = Q(product__product_features__feature__pk=feature, product__product_features__value__in=filters['feature'][feature])
                if 'attribute' in filters and filters['attribute']:
                    for attribute in filters['attribute']:
                        if attribute and filters['attribute'][attribute]:
                            limits['products_final_attr__attribute'] = Q(
                                products_final_attr__attribute__pk=attribute,
                                products_final_attr__value__in=filters['attribute'][attribute]
                            )

                if 'subcategory' in filters and filters['subcategory']:
                    for subcategory in filters['subcategory']:
                        limits['product__subcategory'] = Q(
                            product__subcategory__pk__in=[int(x) for x in filters['subcategory']]
                        )

                if 'query' in filters and filters['query']:
                    filters_txt = [
                        "{}__name__icontains".format(lang),
                        "{}__slug__icontains".format(lang),
                        "code__icontains",
                        "product__code__icontains",
                        "product__model__icontains",
                        "product__{}__name__icontains".format(lang),
                        "product__{}__slug__icontains".format(lang),
                        "product__brand__{}__name__icontains".format(lang),
                        "product__brand__{}__slug__icontains".format(lang),
                        "product__category__{}__name__icontains".format(lang),
                        "product__category__{}__slug__icontains".format(lang),
                        "product__subcategory__{}__name__icontains".format(lang),
                        "product__subcategory__{}__slug__icontains".format(lang),
                    ]
                    queryset_custom = None
                    for filter_txt in filters_txt:
                        queryset_custom_and = None
                        for word in filters['query'].split():
                            if queryset_custom_and:
                                queryset_custom_and &= Q(**{filter_txt: word})
                            else:
                                queryset_custom_and = Q(**{filter_txt: word})
                        if queryset_custom:
                            queryset_custom |= queryset_custom_and
                        else:
                            queryset_custom = queryset_custom_and

                    limits['query'] = queryset_custom

                if 'price_from' in filters and filters['price_from']:
                    try:
                        price_from = filters['price_from']
                        if price_from is not None:
                            limits['products_final__price_from'] = Q(price__gte=float(price_from))
                    except ValueError:
                        pass

                if 'price_to' in filters and filters['price_to']:
                    try:
                        price_to = filters['price_to']
                        if price_to is not None:
                            limits['products_final__price_to'] = Q(price__lte=float(price_to))
                    except ValueError:
                        pass

                if ('force_image' not in filters):
                    limits['image'] = (Q(product__products_image__principal=True) | Q(productfinals_image__principal=True))
                elif ('force_image' in filters and filters['force_image'] == 1):
                    limits['image'] = (Q(product__products_image__principal=True) | Q(productfinals_image__principal=True))

            if only_with_stock is None:
                only_with_stock = settings.CDNX_PRODUCTS_SHOW_ONLY_STOCK

            if only_with_stock and hasattr(self.model, 'product_stocks'):
                limits['force_stock'] = reduce(operator.or_, (
                    Q(product__force_stock=True, product_stocks__quantity__gt=0),
                    Q(product__force_stock=False)
                ))

        return limits

    def render_to_response(self, context, **response_kwargs):
        context = super(ListProducts, self).render_to_response(context, **response_kwargs)

        datas = context._container[0]
        if type(datas) == bytes:
            datas = datas.decode('utf-8')
        answer = json.loads(datas)
        products = []
        for product in answer['table']['body']:
            temp = product.copy()
            # image principal
            pos_image_ppal = [i for i, x in enumerate(product['productfinals_image__principal']) if x == 'True']
            if len(pos_image_ppal) == 0:
                pos_image_ppal = [i for i, x in enumerate(product['product__products_image__principal']) if x == 'True']
                if pos_image_ppal:
                    image = temp['product__products_image__image'][pos_image_ppal[0]]
                else:
                    image = None
            else:
                image = temp['productfinals_image__image'][pos_image_ppal[0]]
            temp['image'] = image
            # is new?
            created = None
            for date_format in getattr(settings, 'DATETIME_INPUT_FORMATS', []):
                try:
                    created = datetime.datetime.strptime(temp['created'], date_format)
                    break
                except ValueError:
                    pass
            if created and (abs(int(time.time() - time.mktime(created.timetuple())))) / (3600 * 24) <= settings.CDNX_PRODUCTS_NOVELTY_DAYS:
                temp['new'] = 1
            else:
                temp['new'] = 0

            attrs = []
            for attr in ProductFinalAttribute.objects.filter(product__pk=product['pk']):
                attrs.append(attr.__unicode__(show_attribute=False))
            if attrs:
                temp['name'] += ' '
                temp['name'] += ' '.join(attrs)
            # clean info
            temp.pop('product__products_image__image')
            temp.pop('product__products_image__principal')
            temp.pop('created')

            products.append(temp)

        answer['table']['body'] = products
        context._container[0] = json.dumps(answer).encode()
        return context


class ListProductsBase(GenList):
    public = True
    model = Product
    gentrans = {
        'buy': _("Buy"),
        'new': _("New"),
        'wishlist': _("Wish list"),
        'shoppingcart': _("Shopping cart"),
    }

    def __fields__(self, info):
        lang = get_language_database()

        fields = []
        fields.append(('name:{}__name'.format(lang), _("Name")))
        fields.append(('slug:{}__slug'.format(lang), _("Slug")))
        fields.append(('products_image__image', _("Image")))
        fields.append(('products_image__principal', _("Principal")))
        # fields.append(('productfinals_image__image', _("Image")))
        # fields.append(('productfinals_image__principal', _("Principal")))
        # fields.append(('price', _("Price")))
        # fields.append(('price_old:price', _("Price")))
        # fields.append(('offer', _("Offer")))
        fields.append(('created', _("Created")))
        # fields.append(('reviews_value', _("reviews_value")))
        # fields.append(('reviews_count', _("reviews_count")))
        return fields

    def __limitQ__(self, info):
        limits = {}
        pk = self.kwargs.get('pk', None)
        type_list = self.kwargs.get('type', None)
        # get language
        lang = get_language_database()

        if pk and type_list:
            # aplicamos los filtros recibidos
            params = ast.literal_eval(info.request.GET.get("json"))

            slug_subcategory = None
            if "subcategory" in params and params["subcategory"]:
                if params["subcategory"] != '*':
                    slug_subcategory = params["subcategory"]

            slug_type = None
            if "brand" in params and params["brand"]:
                if params["brand"] != '*':
                    slug_type = params["brand"]

            slug_family = None
            if "family" in params and params["family"]:
                if params["family"] != '*':
                    slug_family = params["family"]

            only_with_stock = None
            # filtramos dependiendo de la url original que estemos visitando
            if type_list == 'SUB':
                only_with_stock = Category.objects.filter(subcategory__pk=pk, show_only_product_stock=True).exists()
                limits['type_list'] = Q(subcategory__pk=pk)

            elif type_list == 'CAT':
                limits['type_list'] = Q(category__pk=pk)

            elif type_list == 'FAM':
                limits['type_list'] = Q(family__pk=pk)

            elif type_list == 'BRAND':
                limits['type_list'] = Q(brand__pk=pk)

            elif type_list == 'SEARCH':
                only_with_stock = settings.CDNX_PRODUCTS_SHOW_ONLY_STOCK

            else:
                raise Exception("Pendiente de definir")

            if slug_subcategory:
                limits['by_sucategory'] = Q(**{"subcategory__{}__slug".format(lang): slug_subcategory})

            if slug_type:
                limits['by_brand'] = Q(**{"brand__{}__slug".format(lang): slug_type})

            if slug_family:
                limits['by_family'] = Q(**{"family__{}__slug".format(lang): slug_type})

            # aplicamos los filtros recibidos
            params = ast.literal_eval(info.request.GET.get("json"))
            if "filters" in params and params["filters"]:
                filters = params["filters"]
                if 'brand' in filters and filters['brand']:
                    limits["product__brand"] = Q(brand__in=filters['brand'])
                if 'feature' in filters and filters['feature']:
                    for feature in filters['feature']:
                        if feature and filters['feature'][feature]:
                            limits['product_features__feature'] = Q(product_features__feature__pk=feature, product_features__value__in=filters['feature'][feature])
                """
                if 'attribute' in filters and filters['attribute']:
                    for attribute in filters['attribute']:
                        if attribute and filters['attribute'][attribute]:
                            limits['products_final_attr__attribute'] = Q(
                                products_final_attr__attribute__pk=attribute,
                                products_final_attr__value__in=filters['attribute'][attribute]
                            )
                """
                if 'subcategory' in filters and filters['subcategory']:
                    for subcategory in filters['subcategory']:
                        limits['product__subcategory'] = Q(
                            subcategory__pk__in=[int(x) for x in filters['subcategory']]
                        )

                if 'query' in filters and filters['query']:
                    filters_txt = [
                        "{}__name__icontains".format(lang),
                        "{}__slug__icontains".format(lang),
                        "code__icontains",
                        # "product__code__icontains",
                        # "product__model__icontains",
                        # "product__{}__name__icontains".format(lang),
                        # "product__{}__slug__icontains".format(lang),
                        "brand__{}__name__icontains".format(lang),
                        "brand__{}__slug__icontains".format(lang),
                        "family__{}__name__icontains".format(lang),
                        "family__{}__slug__icontains".format(lang),
                        "category__{}__name__icontains".format(lang),
                        "category__{}__slug__icontains".format(lang),
                        "subcategory__{}__name__icontains".format(lang),
                        "subcategory__{}__slug__icontains".format(lang),
                    ]
                    queryset_custom = None
                    for filter_txt in filters_txt:
                        queryset_custom_and = None
                        for word in filters['query'].split():
                            if queryset_custom_and:
                                queryset_custom_and &= Q(**{filter_txt: word})
                            else:
                                queryset_custom_and = Q(**{filter_txt: word})
                        if queryset_custom:
                            queryset_custom |= queryset_custom_and
                        else:
                            queryset_custom = queryset_custom_and

                    limits['query'] = queryset_custom

                """
                if 'price_from' in filters and filters['price_from']:
                    try:
                        price_from = filters['price_from']
                        if price_from is not None:
                            limits['products_final__price_from'] = Q(price__gte=float(price_from))
                    except ValueError:
                        pass

                if 'price_to' in filters and filters['price_to']:
                    try:
                        price_to = filters['price_to']
                        if price_to is not None:
                            limits['products_final__price_to'] = Q(price__lte=float(price_to))
                    except ValueError:
                        pass
                """
                if ('force_image' not in filters):
                    limits['image'] = Q(products_image__principal=True)
                elif ('force_image' in filters and filters['force_image'] == 1):
                    limits['image'] = Q(products_image__principal=True)

            if only_with_stock is None:
                only_with_stock = settings.CDNX_PRODUCTS_SHOW_ONLY_STOCK

            """
            if only_with_stock and hasattr(self.model, 'product_stocks'):
                limits['force_stock'] = reduce(operator.or_, (
                    Q(product__force_stock=True, product_stocks__quantity__gt=0),
                    Q(product__force_stock=False)
                ))
            """
            limits['public'] = Q(public=True)
            limits['distinct'] = True

        return limits

    def render_to_response(self, context, **response_kwargs):
        context = super(ListProductsBase, self).render_to_response(context, **response_kwargs)
        datas = context._container[0]
        if type(datas) == bytes:
            datas = datas.decode('utf-8')
        answer = json.loads(datas)
        products = []
        for product in answer['table']['body']:
            temp = product.copy()
            # image principal
            pos_image_ppal = [i for i, x in enumerate(product['products_image__principal']) if x == 'True']

            if len(pos_image_ppal) == 0:
                image = None
            else:
                image = temp['products_image__image'][pos_image_ppal[0]]
            temp['image'] = image
            # is new?
            created = None
            for date_format in getattr(settings, 'DATETIME_INPUT_FORMATS', []):
                try:
                    created = datetime.datetime.strptime(temp['created'], date_format)
                    break
                except ValueError:
                    pass
            if created and (abs(int(time.time() - time.mktime(created.timetuple())))) / (3600 * 24) <= settings.CDNX_PRODUCTS_NOVELTY_DAYS:
                temp['new'] = 1
            else:
                temp['new'] = 0

            attrs = {}
            for pfa in ProductFinalAttribute.objects.filter(product__product__pk=product['pk']).order_by(
                'attribute__order'
            ):
                if pfa.product not in attrs:
                    attrs[pfa.product.pk] = []

                if pfa.attribute.type_value == TYPE_VALUE_BOOLEAN:
                    value = bool(pfa.value) and _('True') or _('False')
                elif pfa.attribute.type_value == TYPE_VALUE_FREE:
                    value = pfa.value
                elif pfa.attribute.type_value == TYPE_VALUE_LIST:
                    lang = get_language_database()
                    field = '{}__description'.format(lang)
                    ov = OptionValueAttribute.objects.filter(
                        group=pfa.attribute.list_value,
                        pk=int(pfa.value)
                    ).values(
                        field
                    ).first()
                    if ov:
                        value = ov[field]
                    else:
                        value = None
                if value:
                    attrs[pfa.product.pk].append(value)

            temp['attrs'] = attrs
            # clean info
            temp.pop('products_image__image')
            temp.pop('products_image__principal')
            temp.pop('created')

            products.append(temp)

        answer['table']['body'] = products
        context._container[0] = json.dumps(answer).encode()
        return context


# ###########################################
class GenProductFinalOptionUrl(object):
    ws_entry_point = '{}/ProductFinalOptions'.format(settings.CDNX_PRODUCTS_URL)


# ProductFinalOption
class ProductFinalOptionList(GenProductFinalOptionUrl, GenList):
    model = ProductFinalOption
    extra_context = {'menu': ['products', 'ProductFinalOption'], 'bread': [_('Products'), _('ProductFinalOption')]}


class ProductFinalOptionCreate(GenProductFinalOptionUrl, MultiForm, GenCreate):
    model = ProductFinalOption
    form_class = ProductFinalOptionForm
    forms = formsfull["ProductFinalOption"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_final_pk = kwargs.get('cpk', None)
        if self.__product_final_pk:
            self.form_class = ProductFinalOptionFormWithoutProduct
        return super(ProductFinalOptionCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form, multiform):
        if self.__product_final_pk:
            pf = ProductFinal.objects.get(pk=self.__product_final_pk)
            self.request.product_final = pf
            form.instance.product_final = pf

        return super(ProductFinalOptionCreate, self).form_valid(form, multiform)


class ProductFinalOptionCreateModal(GenCreateModal, ProductFinalOptionCreate):
    pass


class ProductFinalOptionUpdate(GenProductFinalOptionUrl, MultiForm, GenUpdate):
    model = ProductFinalOption
    form_class = ProductFinalOptionForm
    forms = formsfull["ProductFinalOption"]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.__product_final_pk = kwargs.get('cpk', None)
        if self.__product_final_pk:
            self.form_class = ProductFinalOptionFormWithoutProduct
        return super(ProductFinalOptionUpdate, self).dispatch(*args, **kwargs)


class ProductFinalOptionUpdateModal(GenUpdateModal, ProductFinalOptionUpdate):
    pass


class ProductFinalOptionDelete(GenProductFinalOptionUrl, GenDelete):
    model = ProductFinalOption


class ProductFinalOptionSubList(GenProductFinalOptionUrl, GenList):
    model = ProductFinalOption
    extra_context = {'menu': ['products', 'ProductFinalOption'], 'bread': [_('Products'), _('ProductFinalOption')]}

    def __limitQ__(self, info):
        limit = {}
        pk = info.kwargs.get('pk', None)
        limit['link'] = Q(product_final__pk=pk)
        return limit


class ProductFinalOptionDetails(GenProductFinalOptionUrl, GenDetail):
    model = ProductFinalOption
    groups = ProductFinalOptionForm.__groups_details__()


class ProductFinalOptionDetailModal(GenDetailModal, ProductFinalOptionDetails):
    pass
