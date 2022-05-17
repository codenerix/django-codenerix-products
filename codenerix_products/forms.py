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

from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.utils import ErrorList
from django.conf import settings

from codenerix.forms import GenModelForm
from codenerix.widgets import MultiStaticSelect, DynamicSelect
from codenerix_extensions.helpers import get_language_database

from .models import TypeTax
from .models import Feature, Attribute, FeatureSpecial, ProductFinalAttribute
from .models import Family, Category, Subcategory, Brand
from .models import Product, ProductFinal, FlagshipProduct
from .models import ProductRelationSold, ProductImage, ProductDocument, ProductFeature, ProductUnique, ProductFinalImage
from .models import GroupValueFeature, GroupValueAttribute, GroupValueFeatureSpecial, OptionValueFeature, OptionValueAttribute, OptionValueFeatureSpecial
from .models import MODELS, MODELS_SLUG, MODELS_BRANDS, MODELS_PRODUCTS, MODELS_PRODUCTS_FINAL, MODELS_SLIDERS, TYPE_VALUES, TYPE_VALUE_LIST, TYPE_VALUE_BOOLEAN, TYPE_VALUE_FREE
from .models import ProductFinalOption


class TypeTaxForm(GenModelForm):
    class Meta:
        model = TypeTax
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['name', 6],
                ['tax', 3],
                ['default', 3],
                ['recargo_equivalencia', 4],

            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['name', 6],
                ['tax', 3],
                ['default', 3],
                ['recargo_equivalencia', 4],
            )
        ]
        return g


class FeatureForm(GenModelForm):
    class Meta:
        model = Feature
        exclude = ['name_file', ]
        autofill = {
            'FeatureForm_category': ['select', 3, 'CDNX_products_categorys_foreign', 'FeatureForm_family', ],
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['family', 3],
                ['category', 3],
                ['order', 3],
                ['public', 3],
                ['type_price', 3],
                ['price', 3],
                ['type_value', 3],
                ['list_value', 3],
                ['image', 6],
            )
        ]
        return g

    def clean(self):
        cleaned_data = super(FeatureForm, self).clean()
        type_value = cleaned_data.get("type_value")
        list_value = cleaned_data.get("list_value")

        if type_value == TYPE_VALUES[2][0] and list_value is None:
            self._errors["type_value"] = ErrorList([_("Debe elegir un lista de valores")])


class AttributeForm(GenModelForm):
    class Meta:
        model = Attribute
        exclude = ['name_file', ]
        autofill = {
            'AttributeForm_category': ['select', 3, 'CDNX_products_categorys_foreign', 'AttributeForm_family', ],
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['family', 3],
                ['category', 3],
                ['order', 3],
                ['public', 3],
                ['type_price', 3],
                ['price', 3],
                ['type_value', 3],
                ['list_value', 3],
                ['image', 6],
                ['attribute', 6],
            )
        ]
        return g

    def clean(self):
        cleaned_data = super(AttributeForm, self).clean()
        type_value = cleaned_data.get("type_value")
        list_value = cleaned_data.get("list_value")

        if type_value == TYPE_VALUES[2][0] and list_value is None:
            self._errors["type_value"] = ErrorList([_("Debe elegir un lista de valores")])


class FeatureSpecialForm(GenModelForm):
    class Meta:
        model = FeatureSpecial
        exclude = ['name_file', ]
        autofill = {
            'FeatureSpecialForm_category': ['select', 3, 'CDNX_products_categorys_foreign', 'FeatureSpecialForm_family', ],
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['family', 3],
                ['category', 3],
                ['order', 2],
                ['public', 2],
                ['unique', 2],
                ['type_price', 3],
                ['price', 3],
                ['type_value', 3],
                ['list_value', 3],
                ['image', 6],
            )
        ]
        return g

    def clean(self):
        cleaned_data = super(FeatureSpecialForm, self).clean()
        type_value = cleaned_data.get("type_value")
        list_value = cleaned_data.get("list_value")

        if type_value == TYPE_VALUES[2][0] and list_value is None:
            self._errors["type_value"] = ErrorList([_("Debe elegir un lista de valores")])


class FamilyForm(GenModelForm):
    class Meta:
        model = Family
        exclude = ['name_file', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 2],
                ['code', 4],
                ['public', 3],
                ['show_menu', 3],
                ['icon', 6],
                ['image', 6],
            )
        ]
        return g


class CategoryForm(GenModelForm):
    class Meta:
        model = Category
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 2],
                ['code', 2],
                ['family', 4],
                ['public', 1],
                ['show_menu', 1],
                ['show_only_product_stock', 2],
                ['icon', 6],
                ['image', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['order', 2],
                ['code', 4],
                ['family', 4],
                ['public', 1],
                ['show_menu', 1],
                ['show_only_product_stock', 2],
                ['image', 6],
                ['icon', 6],
            )
        ]
        return g


class BrandForm(GenModelForm):
    class Meta:
        model = Brand
        exclude = ['name_file', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 2],
                ['outstanding', 2],
                ['show_menu', 2],
                ['image', 6],
            )
        ]
        return g


class SubcategoryForm(GenModelForm):
    class Meta:
        model = Subcategory
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 2],
                ['code', 3],
                ['category', 3],
                ['public', 1],
                ['show_menu', 1],
                ['show_brand', 1],
                ['outstanding', 1],
                ['icon', 6],
                ['image', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['order', 2],
                ['code', 3],
                ['category', 3],
                ['public', 1],
                ['show_menu', 1],
                ['show_brand', 1],
                ['outstanding', 1],
                ['icon', 6],
                ['image', 6],
            )
        ]
        return g


class SubcategoryOwnForm(GenModelForm):
    class Meta:
        model = Subcategory
        exclude = ['category']

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 3],
                ['code', 3],
                ['public', 2],
                ['show_menu', 2],
                ['outstanding', 2],
                ['icon', 6],
                ['image', 6],
            )
        ]
        return g


class ProductFormCreate(GenModelForm):
    class Meta:
        model = Product
        exclude = []
        autofill = {
            'ProductFormCreate_category': ['select', 3, 'CDNX_products_categorys_foreign', 'ProductFormCreate_family', ],
            'ProductFormCreate_subcategory': ['select', 3, 'CDNX_products_subcategorys_foreign', 'ProductFormCreate_category', ],
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['code', 4],
                ['price_base', 3],
                ['public', 1],
                ['of_sales', 1],
                ['of_purchase', 1],
                ['force_stock', 1],
                ['caducable', 1],
                ['model', 4],
                ['brand', 4],
                ['feature_special', 4],
                ['family', 4],
                ['category', 4],
                ['subcategory', 4],
                ['tax', 4],
                ['url_video', 4],
            ),
            (
                _('Packaging information'), 12,
                ['packing_cost', 4],
                ['weight', 4],
            )
        ]
        return g


class ProductFormCreateCustom(GenModelForm):
    pass_to_final = forms.BooleanField(label=_("Create product final"), required=False, initial=True)
    ean13 = forms.CharField(label=_("EAN-13"), max_length=13, required=False)

    class Meta:
        model = Product
        exclude = []
        autofill = {
            'ProductFormCreateCustom_category': ['select', 3, 'CDNX_products_categorys_foreign', 'ProductFormCreateCustom_family', ],
            'ProductFormCreateCustom_subcategory': ['select', 3, 'CDNX_products_subcategorys_foreign', 'ProductFormCreateCustom_category', ],
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['code', 3],
                ['price_base', 2],
                ['pass_to_final', 2],
                ['public', 1],
                ['of_sales', 1],
                ['of_purchase', 1],
                ['force_stock', 1],
                ['caducable', 1],
                ['model', 4],
                ['brand', 4],
                ['feature_special', 4],
                ['family', 4],
                ['category', 4],
                ['subcategory', 4],
                ['tax', 4],
                ['url_video', 4],
                ['ean13', 4],
            ),
            (
                _('Packaging information'), 12,
                ['packing_cost', 4],
                ['weight', 4],
            )
        ]
        return g


class ProductForm(GenModelForm):
    class Meta:
        model = Product
        exclude = ['related', ]
        autofill = {
            'ProductForm_category': ['select', 3, 'CDNX_products_categorys_foreign', 'ProductForm_family', ],
            'ProductForm_subcategory': ['select', 3, 'CDNX_products_subcategorys_foreign', 'ProductForm_category', ],
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['code', 4],
                ['price_base', 3],
                ['public', 1],
                ['of_sales', 1],
                ['of_purchase', 1],
                ['force_stock', 1],
                ['caducable', 1],
                ['model', 4],
                ['brand', 4],
                ['feature_special', 4],
                ['family', 4],
                ['category', 4],
                ['subcategory', 4],
                ['tax', 4],
                ['url_video', 4],
            ),
            (
                _('Packaging information'), 12,
                ['packing_cost', 4],
                ['weight', 4],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        lang = get_language_database()
        g = [
            (
                _('Details'), 6,
                ['pk', 6],
                ['model', 6],
                ['brand', 6],
                ['family', 6],
                ['category', 6],
                ['subcategory', 6],
                ['public', 6],
                ['code', 6],
                ['price_base', 6],
                ['of_sales', 6],
                ['of_purchase', 6],
                ['force_stock', 6],
                ['tax', 6],
                ['url_video', 6],
                ['feature_special', 6],
                ['packing_cost', 6],
                ['weight', 6],
                ['caducable', 6],
            ),
            (
                _('Information'), 6,
                ["{}__name".format(lang), 6],
                ["{}__slug".format(lang), 6],
                ["{}__public".format(lang), 6],
                ["{}__meta_title".format(lang), 6],
                ["{}__meta_description".format(lang), 6],
            )
        ]
        return g


class ProductRelatedSubForm(GenModelForm):
    new_product = forms.ModelChoiceField(queryset=Product.objects.all(), label=_('Product'), required=True)

    class Meta:
        model = Product
        fields = ['new_product', ]
        """
        autofill = {
            'new_product': ['select', 3, 'limittrials_foreign', '__pk__'],
        }
        """

    # Esto es un intento de que solo muestre las que no tienen riesgo de provocar bucles. Se deja para más adelante.
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        return super(ProductRelatedSubForm, self).__init__(*args, **kwargs)

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['new_product', 12],
            )
        ]
        return g


class ProductRelationSoldForm(GenModelForm):
    class Meta:
        model = ProductRelationSold
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['product', 6],
                ['related', 6],
                ['hits', 6],
            )
        ]
        return g


class ProductImageForm(GenModelForm):
    class Meta:
        model = ProductImage
        exclude = ['product', 'name_file', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 4],
                ['public', 2],
                ['principal', 2],
                ['flagship_product', 2],
                ['outstanding', 2],
                ['image', 12],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['product', 6],
                ['order', 6],
                ['public', 6],
                ['principal', 6],
                ['flagship_product', 4],
                ['outstanding', 4],
                ['image', 6],
                ['name_file', 6],
            )
        ]
        return g


class ProductFinalImageForm(GenModelForm):
    class Meta:
        model = ProductFinalImage
        exclude = ['product_final', 'name_file', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['order', 4],
                ['public', 2],
                ['principal', 2],
                ['flagship_product', 2],
                ['outstanding', 2],
                ['image', 12],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['product_final', 6],
                ['order', 6],
                ['public', 6],
                ['principal', 6],
                ['flagship_product', 4],
                ['outstanding', 4],
                ['image', 6],
                ['name_file', 6],
            )
        ]
        return g


class ProductDocumentForm(GenModelForm):
    class Meta:
        model = ProductDocument
        exclude = ['product', 'name_file', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['doc_path', 9],
                ['public', 3],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['product', 6],
                ['name_file', 6],
                ['public', 6],
                ['doc_path', 6],
            )
        ]
        return g


class ProductFinalFormCreate(GenModelForm):
    related = forms.ModelMultipleChoiceField(
        queryset=ProductFinal.objects.all(),
        label=_('Related products'),
        required=False,
        widget=MultiStaticSelect(
            attrs={'manytomany': True, }
        )
    )

    related_accesory = forms.ModelMultipleChoiceField(
        queryset=ProductFinal.objects.all(),
        label=_('Related accesory'),
        required=False,
        widget=MultiStaticSelect(
            attrs={'manytomany': True, }
        )
    )

    class Meta:
        model = ProductFinal
        exclude = []
        autofill = {
            'ProductFinalFormCreate_product': ['select', 3, 'CDNX_products_products_foreign'],
        }

    def __groups__(self):
        g = [(
            _('Details'), 12,
            ["product", 4],
            ["offer", 2],
            ["outstanding", 2],
            ['most_sold', 2],
            ["sample", 2],
            ["code", 4],
            ["price_base_local", 4],
            ["ean13", 4],
            ["related", 6],
            ["related_accesory", 6],
        ), (
            _('Packaging information'), 12,
            ['packing_cost', 4],
            ['weight', 4],
        )]
        return g


class ProductFinalFormCreateModal(ProductFinalFormCreate):
    class Meta:
        model = ProductFinal
        exclude = ['product', ]
        autofill = {
            'ProductFinalFormCreate_product': ['select', 3, 'CDNX_products_products_foreign'],
        }

    def __groups__(self):
        g = [(
            _('Details'), 12,
            ["offer", 3],
            ["outstanding", 3],
            ['most_sold', 3],
            ["sample", 3],
            ["code", 4],
            ["price_base_local", 4],
            ["ean13", 4],
            ["related", 6],
            ["related_accesory", 6],
        ), (
            _('Packaging information'), 12,
            ['packing_cost', 4],
            ['weight', 4],
        )]
        return g


class ProductFinalForm(GenModelForm):
    class Meta:
        model = ProductFinal
        exclude = ['related', 'related_accesory']
        autofill = {
            'ProductFinalFormCreate_product': ['select', 3, 'CDNX_products_products_foreign'],  # Al usar un multiform, el nombre es distinto.
        }

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ["product", 4],
                ["offer", 2],
                ["outstanding", 2],
                ['most_sold', 2],
                ['sample', 2],
                ["code", 4],
                ["price_base_local", 4],
                ["ean13", 4],
            ), (
                _('Packaging information'), 12,
                ['packing_cost', 4],
                ['weight', 4],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        lang = get_language_database()
        g = [
            (
                _('Details'), 6,
                ['pk', 6],
                ["code", 4],
                ["product", 6],
                ["price_base_local", 4],
                ["offer", 3],
                ["outstanding", 3],
                ["price", 6],
                ["reviews_value", 6],
                ["reviews_count", 6],
                ["ean13", 6],
                ["most_sold", 6],
                ["sample", 6],
                ['packing_cost', 4],
                ['weight', 4],
            ),
            (
                _('Information'), 6,
                ["{}__name".format(lang), 6],
                ["{}__slug".format(lang), 6],
                ["{}__public".format(lang), 6],
                ["{}__meta_title".format(lang), 6],
                ["{}__meta_description".format(lang), 6],
            )
        ]
        return g


class ProductFinalRelatedSubForm(GenModelForm):
    new_product = forms.ModelChoiceField(queryset=ProductFinal.objects.all(), label=_('Product'), required=True,)

    class Meta:
        model = ProductFinal
        fields = ['new_product', ]

    # Esto es un intento de que solo muestre las que no tienen riesgo de provocar bucles. Se deja para más adelante.
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        return super(ProductFinalRelatedSubForm, self).__init__(*args, **kwargs)

    def __groups__(self):
        g = [
            (_('Details'), 12,
                ['new_product', 12],)
        ]
        return g


class ProductFinalAttributeForm(GenModelForm):
    product_pk = forms.CharField(widget=forms.HiddenInput())
    value = forms.CharField(widget=forms.HiddenInput(), required=False)
    value_free = forms.CharField(label=_("Value"), max_length=80, required=False)
    value_bool = forms.BooleanField(label=_("Value"), required=False)
    value_list = forms.CharField(label=_("Value"), required=False, widget=DynamicSelect())

    class Meta:
        model = ProductFinalAttribute
        exclude = ["product", "product_pk", ]
        autofill = {
            'attribute': ['select', 3, 'CDNX_products_attributes_foreign', 'product_pk'],
            'value_list': ['select', 3, 'CDNX_products_OptionValueAttributes_foreign', 'product_pk', 'attribute'],
        }

    def __init__(self, *args, **kwargs):
        product_pk = kwargs.get('product_pk', None)
        value_bool = kwargs.get('value_bool', None)
        value_free = kwargs.get('value_free', None)
        value_list = kwargs.get('value_list', None)
        if product_pk:
            kwargs.pop('product_pk')
        if value_bool:
            kwargs.pop('value_bool')
        if value_free:
            kwargs.pop('value_free')
        if value_list:
            kwargs.pop('value_list')
        r = super(ProductFinalAttributeForm, self).__init__(*args, **kwargs)
        self.initial['product_pk'] = product_pk
        self.initial['value_bool'] = value_bool
        self.initial['value_free'] = value_free
        self.initial['value_list'] = value_list
        return r

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ["attribute", 12],
                ['value_free', 12, None, None, None, None, None, None, ["ng-show=show_optionvalue('{}')".format(TYPE_VALUE_FREE)]],
                ['value_bool', 12, None, None, None, None, None, None, ["ng-show=show_optionvalue('{}')".format(TYPE_VALUE_BOOLEAN)]],
                ['value_list', 12, None, None, None, None, None, None, ["ng-show=show_optionvalue('{}')".format(TYPE_VALUE_LIST)]],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ["attribute", 6],
                ["value", 6],
            )
        ]
        return g


class ProductFeatureForm(GenModelForm):
    product_pk = forms.CharField(widget=forms.HiddenInput())
    value = forms.CharField(widget=forms.HiddenInput(), required=False)
    value_free = forms.CharField(label=_("Value"), max_length=80, required=False)
    value_bool = forms.BooleanField(label=_("Value"), required=False)
    value_list = forms.CharField(label=_("Value"), required=False, widget=DynamicSelect())

    class Meta:
        model = ProductFeature
        exclude = ["product", "product_pk", ]
        autofill = {
            'feature': ['select', 3, 'CDNX_products_features_foreign', 'product_pk'],
            'value_list': ['select', 3, 'CDNX_products_OptionValueFeatures_foreign', 'product_pk', 'feature'],
        }

    def __init__(self, *args, **kwargs):
        product_pk = kwargs.get('product_pk', None)
        value_bool = kwargs.get('value_bool', None)
        value_free = kwargs.get('value_free', None)
        value_list = kwargs.get('value_list', None)
        if product_pk:
            kwargs.pop('product_pk')
        if value_bool:
            kwargs.pop('value_bool')
        if value_free:
            kwargs.pop('value_free')
        if value_list:
            kwargs.pop('value_list')
        r = super(ProductFeatureForm, self).__init__(*args, **kwargs)
        self.initial['product_pk'] = product_pk
        self.initial['value_bool'] = value_bool
        self.initial['value_free'] = value_free
        self.initial['value_list'] = value_list
        return r

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['feature', 12],
                ['value_free', 12, None, None, None, None, None, None, ["ng-show=show_optionvalue('{}')".format(TYPE_VALUE_FREE)]],
                ['value_bool', 12, None, None, None, None, None, None, ["ng-show=show_optionvalue('{}')".format(TYPE_VALUE_BOOLEAN)]],
                ['value_list', 12, None, None, None, None, None, None, ["ng-show=show_optionvalue('{}')".format(TYPE_VALUE_LIST)]],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['product', 6],
                ['feature', 6],
                ['value', 6],
            )
        ]
        return g


class ProductUniqueForm(GenModelForm):
    product_pk = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ProductUnique
        exclude = ['product_final', "product_pk", ]

    def __init__(self, *args, **kwargs):
        product_pk = kwargs.get('product_pk', None)
        if product_pk:
            kwargs.pop('product_pk')
        super(ProductUniqueForm, self).__init__(*args, **kwargs)
        self.initial['product_pk'] = product_pk
        return None

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['value', 6],
                ['stock_original', 6],
                ['box', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['product_final', 6],
                ['product_final__product__feature_special', 6],
                ['value', 6],
                ['stock_original', 6],
                ['stock_real', 6],
                ['stock_locked', 6],
            )
        ]
        return g


class GroupValuesForm(GenModelForm):
    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['name', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['name', 6],
            )
        ]
        return g


class GroupValueFeatureForm(GroupValuesForm):
    class Meta:
        model = GroupValueFeature
        exclude = []


class GroupValueAttributeForm(GroupValuesForm):
    class Meta:
        model = GroupValueAttribute
        exclude = []


class GroupValueFeatureSpecialForm(GroupValuesForm):
    class Meta:
        model = GroupValueFeatureSpecial
        exclude = []


class OptionValuesForm(GenModelForm):
    def __groups__(self):
        g = []
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['group', 6],
            )
        ]
        return g


class OptionValueFeatureForm(OptionValuesForm):
    class Meta:
        model = OptionValueFeature
        exclude = ['group', ]


class OptionValueAttributeForm(OptionValuesForm):
    class Meta:
        model = OptionValueAttribute
        exclude = ['group', ]


class OptionValueFeatureSpecialForm(OptionValuesForm):
    class Meta:
        model = OptionValueFeatureSpecial
        exclude = ['group', ]


class FlagshipProductForm(GenModelForm):
    class Meta:
        model = FlagshipProduct
        exclude = ['name_file', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['product_final', 6],
                ['public', 3],
                ['view_video', 3],
                ['orientazion', 6],
                ['image', 6],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['product_final', 6],
                ['public', 6],
                ['view_video', 6],
                ['orientazion', 6],
                ['image', 6],
                ['name_file', 6],
            )
        ]
        return g

    def clean(self):
        if self.cleaned_data['view_video'] and not self.cleaned_data['product_final'].product.url_video:
            msg = _("The select product haven't video url")
            self._errors["view_video"] = ErrorList([_(msg)])


class ProductFinalOptionForm(GenModelForm):
    products_pack = forms.ModelMultipleChoiceField(
        queryset=ProductFinal.objects.all(),
        label=_('Option products'),
        required=False,
        widget=MultiStaticSelect(
            attrs={'manytomany': True, }
        )
    )

    class Meta:
        model = ProductFinalOption
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['product_final', 6],
                ['order', 3],
                ['active', 3],
                ['products_pack', 12],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (
                _('Details'), 12,
                ['product_final', 6],
                ['products_pack', 6],
                ['active', 6],
                ['order', 6],
            )
        ]
        return g


class ProductFinalOptionFormWithoutProduct(GenModelForm):
    products_pack = forms.ModelMultipleChoiceField(
        queryset=ProductFinal.objects.all(),
        label=_('Option products'),
        required=False,
        widget=MultiStaticSelect(
            attrs={'manytomany': True, }
        )
    )

    class Meta:
        model = ProductFinalOption
        exclude = ['product_final', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['products_pack', 8],
                ['order', 2],
                ['active', 2],
            )
        ]
        return g


# MODELS
query = ""
forms_dyn = []
for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        exec("from codenerix_products.models import {}Text{}\n".format(model, lang_code))

        if model in ['ProductImage', 'ProductFinalImage']:
            label = _('Title and alternative text of the image')
        else:
            label = _('Description')
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,"""
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['description', 12, None, None, None, None, '{label}', ["ng-change=refresh_lang_field('description', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['description', 12, None, None, None, None, '{label}'],
            )]\n"""
        exec(query.format(model=model, lang=lang_code, label=label, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))


# MODELS BRANDS
for info in MODELS_BRANDS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_products.models import {}Text{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,
                """
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['name', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('name', '{model}TextForm', [{languages}])"]],
                ['slug', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('slug', '{model}TextForm', [{languages}])"]],
                ['public', 4],
                ['description_short', 6, None, None, None, None, None, ["ng-blur=refresh_lang_field('description_short', '{model}TextForm', [{languages}])"]],
                ['description_long', 6, None, None, None, None, None, ["ng-blur=refresh_lang_field('description_long', '{model}TextForm', [{languages}])"]],
            ), (_('SEO'),12,
                ['meta_title', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_title', '{model}TextForm', [{languages}])"]],
                ['meta_description', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_description', '{model}TextForm', [{languages}])"]],
                ['meta_keywords', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_keywords', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['name', 4],
                ['slug', 4],
                ['public', 4],
                ['description_short', 6],
                ['description_long', 6],
            ), (_('SEO'),12,
                ['meta_title', 4],
                ['meta_description', 4],
                ['meta_keywords', 4],
            )]\n"""
        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))


# MODELS PRODUCTS
for info in MODELS_PRODUCTS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_products.models import {}Text{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,
                """
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['name', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('name', '{model}TextForm', [{languages}])"]],
                ['slug', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('slug', '{model}TextForm', [{languages}])"]],
                ['public', 4],
                ['description_short', 6, None, None, None, None, None, ["ng-blur=refresh_lang_field('description_short', '{model}TextForm', [{languages}])"]],
                ['description_long', 6, None, None, None, None, None, ["ng-blur=refresh_lang_field('description_long', '{model}TextForm', [{languages}])"]],
            ), (_('SEO'),12,
                ['meta_title', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_title', '{model}TextForm', [{languages}])"]],
                ['meta_description', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_description', '{model}TextForm', [{languages}])"]],
                ['meta_keywords', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_keywords', '{model}TextForm', [{languages}])"]],
                ['tags', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('tags', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['name', 4],
                ['slug', 4],
                ['public', 4],
                ['description_short', 6],
                ['description_long', 6],
            ), (_('SEO'),12,
                ['meta_title', 4],
                ['meta_description', 4],
                ['meta_keywords', 4],
                ['tags', 4],
            )]\n"""
        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))


# MODELS PRODUCTS
for info in MODELS_PRODUCTS_FINAL:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_products.models import {}Text{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,
                """
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['name', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('name', '{model}TextForm', [{languages}])"]],
                ['slug', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('slug', '{model}TextForm', [{languages}])"]],
                ['public', 4],
                ['description_short', 6, None, None, None, None, None, ["ng-blur=refresh_lang_field('description_short', '{model}TextForm', [{languages}])"]],
                ['description_long', 6, None, None, None, None, None, ["ng-blur=refresh_lang_field('description_long', '{model}TextForm', [{languages}])"]],
                ['description_sample', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('description_sample', '{model}TextForm', [{languages}])"]],
            ), (_('SEO'),12,
                ['meta_title', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_title', '{model}TextForm', [{languages}])"]],
                ['meta_description', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_description', '{model}TextForm', [{languages}])"]],
                ['meta_keywords', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_keywords', '{model}TextForm', [{languages}])"]],
                ['tags', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_keywords', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['name', 4],
                ['slug', 4],
                ['public', 4],
                ['description_short', 6],
                ['description_long', 6],
                ['description_sample', 12],
            ), (_('SEO'),12,
                ['meta_title', 4],
                ['meta_description', 4],
                ['meta_keywords', 4],
                ['tags', 4],
            )]\n"""
        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))


# MODELS SLIDERS
query = ""
forms_dyn = []
for info in MODELS_SLIDERS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_products.models import {}Text{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,"""
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['title', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('title', '{model}TextForm', [{languages}])"]],
                ['description', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('description', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['title', 12],
                ['description', 12],
            )]\n"""
        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))

# MODELS SLUG
query = ""
forms_dyn = []
for info in MODELS_SLUG:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from codenerix_products.models import {}Text{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}Text{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,"""
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['name', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('name', '{model}TextForm', [{languages}])"]],
                ['slug', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('slug', '{model}TextForm', [{languages}])"]],
                ['description', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('description', '{model}TextForm', [{languages}])"]],
            ), (_('SEO'),12,
                ['meta_title', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_title', '{model}TextForm', [{languages}])"]],
                ['meta_description', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_description', '{model}TextForm', [{languages}])"]],
                ['meta_keywords', 4, None, None, None, None, None, ["ng-blur=refresh_lang_field('meta_keywords', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['name', 12],
                ['slug', 12],
                ['description', 12],
            ), (_('SEO'),12,
                ['meta_title', 4],
                ['meta_description', 4],
                ['meta_keywords', 4],
            )]\n"""

        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))
