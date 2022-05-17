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

import copy

from operator import or_
from collections import Iterable
from functools import reduce
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction, IntegrityError
from django.db.models import F, Q
from django.utils import timezone
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from codenerix.fields import ImageAngularField
from codenerix.helpers import nameunify, qobject_builder_string_search
from codenerix.lib.helpers import upload_path
from codenerix.models import CodenerixModel
from codenerix.fields import WysiwygAngularField
from codenerix_extensions.helpers import get_language_database
from codenerix_extensions.files.models import GenImageFile, GenDocumentFile, GenImageFileNull
from codenerix_storages.models import StorageBox

from codenerix_products.exceptions import ProductUniqueAlreadyExists, ProductUniqueQuantityExceeded, ProductUniqueNotProductFinal, ProductFinalAttributeOnlyOne


CURRENCY_MAX_DIGITS = getattr(settings, 'CDNX_INVOICING_CURRENCY_MAX_DIGITS', 10)
CURRENCY_DECIMAL_PLACES = getattr(settings, 'CDNX_INVOICING_CURRENCY_DECIMAL_PLACES', 2)

PRODUCT_UNIQUE_VALUE_LENGTH = 80

TYPE_PRICE_PERCENTAGE = 'P'
TYPE_PRICE_INCREASE = 'I'
TYPE_PRICE_FINAL = 'F'

TYPE_PRICES = (
    (TYPE_PRICE_PERCENTAGE, _('Porcentaje sobre el precio del producto')),
    (TYPE_PRICE_INCREASE, _('Incremento sobre el precio del producto')),
    (TYPE_PRICE_FINAL, _('Precio final')),
)

TYPE_VALUE_LIST = 'O'
TYPE_VALUE_BOOLEAN = 'B'
TYPE_VALUE_FREE = 'F'
TYPE_VALUES = (
    (TYPE_VALUE_FREE, _('Sin validacion')),
    (TYPE_VALUE_BOOLEAN, _('Boolean')),
    (TYPE_VALUE_LIST, _('Lista de opciones')),
)

TYPE_ORIENTAZION = (
    ('R', _('Right')),
    ('L', _('Left')),
)


# Model Mixins

class CustomQueryMixin(object):

    @classmethod
    def query_or(cls, query, *values_list, **annotations):
        pop_annotations = False
        if 'pop_annotations' in annotations:
            pop_annotations = annotations['pop_annotations']
            annotations.pop('pop_annotations')

        annotated_keys = annotations.values()
        annotations = {key: F(value) for key, value in annotations.items()}

        if isinstance(query, Iterable):
            query = reduce(or_, query)

        result = cls.objects.filter(query).values(*values_list).annotate(**annotations)

        if pop_annotations:
            for querydict in result:
                for value in annotated_keys:
                    querydict.pop(value)

        return result


# tipos de impuestos aplicables a los productos
class TypeTax(CodenerixModel):
    tax = models.FloatField(_("Tax (%)"), validators=[MinValueValidator(0), MaxValueValidator(100)], blank=False, null=False)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
    default = models.BooleanField(_("Default"), blank=False, default=False)
    recargo_equivalencia = models.FloatField(_("Recargo de equivalencia (%)"), validators=[MinValueValidator(0), MaxValueValidator(100)], blank=False, null=False)

    def __unicode__(self):
        return u"{}".format(smart_str(self.name))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('tax', _("Tax (%)")))
        fields.append(('recargo_equivalencia', _("Recargo de equivalencia (%)")))
        fields.append(('default', _('Default')))
        return fields

    def lock_delete(self):
        if self.products.exists():
            return _("Cannot delete type tax model, relationship between type tax model and products")
        else:
            return super(TypeTax, self).lock_delete()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.default:
                TypeTax.objects.exclude(pk=self.pk).update(default=False)
            else:
                if not TypeTax.objects.exclude(pk=self.pk).filter(default=True).exists():
                    self.default = True

        if self.pk:
            obj = TypeTax.objects.get(pk=self.pk)
            if obj.tax != self.tax:
                result = super(TypeTax, self).save(*args, **kwargs)
                for product in self.products.all():
                    for pf in product.products_final.all():
                        pf.recalculate()
            else:
                result = super(TypeTax, self).save(*args, **kwargs)
        else:
            result = super(TypeTax, self).save(*args, **kwargs)
        return result


# atributos
class GenAttr(CodenerixModel, GenImageFileNull):  # META: Abstract class
    """
    type_value:
        * libre (no hay validación extra)
        * Boolean (no/si)
        * lista de opciones (select)
    type_price:
        * porcentaje sobre el precio del producto
        * incremento sobre el precio del producto
        * precio final
    """
    class Meta(CodenerixModel.Meta):
        abstract = True

    type_value = models.CharField(_("Type value"), max_length=2, choices=TYPE_VALUES, blank=False, null=False, default=TYPE_VALUE_FREE)
    price = models.FloatField(_("Price"), blank=False, null=False, default=0)
    type_price = models.CharField(_("Type price"), max_length=2, choices=TYPE_PRICES, blank=False, null=False, default=TYPE_PRICE_PERCENTAGE)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)

    def __fields__(self, info):
        fields = []
        fields.append(('family', _('Family')))
        fields.append(('category', _('Category')))
        fields.append(('get_type_value_display', _('Type Value')))
        fields.append(('public', _('Public')))
        fields.append(('order', _('Order')))

        lang = settings.LANGUAGES_DATABASES[0].lower()
        fields.append(('{}__description'.format(lang), 'Description', 100))
        return fields

    def __unicode__(self):
        return u"{}".format(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).description)

    def __str__(self):
        return self.__unicode__()


# description del texto en diferentes idiomas
class GenText(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    description = models.CharField(_("Description"), max_length=250, blank=False, null=False)

    def __fields__(self, info):
        fields = []
        fields.append(('description', _('Description'), 100))
        return fields

    def __unicode__(self):
        return u"{}".format(self.description)

    def __str__(self):
        return self.__unicode__()


# texto de posicionamiento
class GenSEOText(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True, null=True)
    meta_description = models.CharField(_("Meta Description"), max_length=70, blank=True, null=True)
    meta_keywords = models.CharField(_("Meta Keywords"), max_length=160, blank=True, null=True)


# description del texto en diferentes idiomas
class GenTextSlug(GenSEOText):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    slug = models.CharField(_("Slug"), max_length=250, blank=False, null=False, unique=True)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    description = WysiwygAngularField(_("Description"), blank=False, null=False)

    def __fields__(self, info):
        fields = []
        fields.append(('name', _('Name'), 100))
        fields.append(('description', _('Description'), 100))
        return fields

    def __unicode__(self):
        return u"{}".format(self.name)

    def __str__(self):
        return self.__unicode__()

    def save(self, *args, **kwards):
        self.slug = nameunify(self.slug, True)
        return super(GenTextSlug, self).save(*args, **kwards)


class GenTextTitle(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    title = models.CharField(_("Text alternavive image"), max_length=250, blank=False, null=False)
    description = WysiwygAngularField(_("Description"), blank=True, null=True)


# texto de los product y brands
class GenProductBrandText(GenSEOText):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    description_short = WysiwygAngularField(_("Description short"), blank=True, null=True)
    description_long = WysiwygAngularField(_("Description long"), blank=True, null=True)
    # url amigable
    slug = models.CharField(_("Slug"), max_length=250, blank=False, null=False, unique=True)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)

    def __str__(self):
        return u"{}".format(smart_str(self.description_short))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('meta_title', _("Tittle")))
        fields.append(('meta_description', _("Meta Description")))
        fields.append(('description_short', _("Description short")))
        fields.append(('description_long', _("Description long")))
        fields.append(('slug', _("Slug")))
        return fields

    def save(self, *args, **kwards):
        self.slug = nameunify(self.slug, True)
        return super(GenProductBrandText, self).save(*args, **kwards)


class GenProductText(GenProductBrandText):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    tags = models.TextField(_("TAGs"), blank=True, null=True)


class GenBrandText(GenProductBrandText):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True


# texto de productfinal
class GenProductFinalText(GenProductText):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    description_sample = WysiwygAngularField(_("Sample description"), blank=True, null=True)

# #####################################


# familias
class Family(CodenerixModel, GenImageFileNull):
    code = models.CharField(_("Code"), max_length=250, blank=True, null=True, unique=True)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    show_menu = models.BooleanField(_("Show menu"), blank=True, null=False, default=True)
    icon = ImageAngularField(_("Icon"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja que sea una imagen superior a 200px transparente y en formato png o svg'))

    def __fields__(self, info):
        fields = []
        fields.append(('order', _("Order")))
        fields.append(('{}__name'.format(settings.LANGUAGES_DATABASES[0].lower()), _("Name")))
        fields.append(('code', _("Code")))
        fields.append(('public', _("Public")))
        fields.append(('show_menu', _("Show Menu")))
        return fields

    def __str__(self):
        if self.code:
            return u"{} ({})".format(smart_str(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name), smart_str(self.code))
        else:
            return u"{}".format(smart_str(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name))

    def __unicode__(self):
        return self.__str__()

    def lock_delete(self):
        if self.products.exists():
            return _("Cannot delete family model, relationship between family model and products")
        elif self.features.exists():
            return _("Cannot delete family model, relationship between family model and features")
        elif self.attributes.exists():
            return _("Cannot delete family model, relationship between family model and attributes")
        elif self.feature_specials.exists():
            return _("Cannot delete family model, relationship between family model and feature special")
        elif self.categories.exists():
            return _("Cannot delete family model, relationship between family model and categories")
        else:
            return super(Family, self).lock_delete()


# categorias
class Category(CodenerixModel):
    code = models.CharField(_("Code"), max_length=250, blank=True, null=True, unique=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='categories', verbose_name=_("Family"))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    show_menu = models.BooleanField(_("Show menu"), blank=True, null=False, default=True)
    show_only_product_stock = models.BooleanField(_("Show only products in stock"), blank=True, null=False, default=True)
    image = ImageAngularField(_("Image"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja un tamaño comprendido entre 1200px y 2000px'))
    icon = ImageAngularField(_("Icon"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja que sea una imagen superior a 200px transparente y en formato png o svg'))
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)

    def __str__(self):
        if self.code:
            return u"{} ({})".format(smart_str(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name), smart_str(self.code))
        else:
            return u"{}".format(smart_str(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('order', _("Order")))
        fields.append(('{}__name'.format(settings.LANGUAGES_DATABASES[0].lower()), _("Name")))
        fields.append(('code', _("Code")))
        fields.append(('family__{}__name'.format(settings.LANGUAGES_DATABASES[0].lower()), _("Family name")))
        fields.append(('family__code', _("Family code")))
        fields.append(('public', _("Public")))
        fields.append(('show_menu', _("Show Menu")))
        fields.append(('show_only_product_stock', _("Show Only Products with Stock")))
        return fields

    def lock_delete(self):
        if self.products.exists():
            return _("Cannot delete category model, relationship between category model and products")
        elif self.features.exists():
            return _("Cannot delete category model, relationship between category model and features")
        elif self.attributes.exists():
            return _("Cannot delete category model, relationship between category model and attributes")
        elif self.feature_specials.exists():
            return _("Cannot delete category model, relationship between category model and feature special")
        elif self.subcategory.exists():
            return _("Cannot delete category model, relationship between category model and subcategories")
        else:
            return super(Category, self).lock_delete()


# subcategorias
class Subcategory(CodenerixModel):
    code = models.CharField(_("Code"), max_length=250, blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory', verbose_name=_("Category"))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    show_menu = models.BooleanField(_("Show menu"), blank=True, null=False, default=True)
    show_brand = models.BooleanField(_("Show brand (for menu)"), blank=True, null=False, default=True)
    outstanding = models.BooleanField(_("Outstanding"), blank=True, null=False, default=False)
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    image = ImageAngularField(_("Image"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja un tamaño comprendido entre 1200px y 2000px'))
    icon = ImageAngularField(_("Icon"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja que sea una imagen superior a 200px transparente y en formato png o svg'))

    def __str__(self):
        if self.code:
            return u"{} ({})".format(smart_str(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name), smart_str(self.code))
        else:
            return u"{}".format(smart_str(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name))

    def __unicode__(self):
        return self.__str__()

    def __fields__(self, info):
        fields = []
        fields.append(('{}__name'.format(settings.LANGUAGES_DATABASES[0].lower()), _("Name")))
        fields.append(('code', _("Code")))
        fields.append(('category__{}__name'.format(settings.LANGUAGES_DATABASES[0].lower()), _("Category name")))
        fields.append(('category__code', _("Category code")))
        fields.append(('category__family__{}__name'.format(settings.LANGUAGES_DATABASES[0].lower()), _("Family name")))
        fields.append(('category__family__code', _("Family code")))
        fields.append(('public', _("Public")))
        fields.append(('show_menu', _("Show Menu")))
        fields.append(('show_brand', _("Show brand (for menu)")))
        fields.append(('outstanding', _("Outstanding")))
        fields.append(('order', _("Order")))
        return fields

    def lock_delete(self):
        if self.products.exists():
            return _("Cannot delete subcategory model, relationship between subcategory model and products")
        else:
            return super(Subcategory, self).lock_delete()


# grupo de valores
class GroupValues(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    name = models.CharField(_("Name"), max_length=250, blank=True, null=True, unique=True)

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        return fields

    def __unicode__(self):
        return u"{}".format(smart_str(self.name))

    def __str__(self):
        return self.__unicode__()


# grupo de valores para features
class GroupValueFeature(GroupValues):
    def __fields__(self, info):
        fields = super(GroupValueFeature, self).__fields__(info)
        fields.append(('options_value_feature', _('Option value')))
        return fields

    def lock_delete(self):
        if self.options_value_feature.exists():
            return _("Cannot delete group value model, relationship between group value model and options")
        elif self.features.exists():
            return _("Cannot delete group value model, relationship between group value model and features")
        else:
            return super(GroupValueFeature, self).lock_delete()


# grupo de valores para attributes
class GroupValueAttribute(GroupValues):
    def __fields__(self, info):
        fields = super(GroupValueAttribute, self).__fields__(info)
        fields.append(('options_value_attribute', _('Option value')))
        return fields

    def lock_delete(self):
        if self.options_value_attribute.exists():
            return _("Cannot delete group value model, relationship between group value model and options")

        elif self.attributes.exists():
            return _("Cannot delete group value model, relationship between group value model and attributes")
        else:
            return super(GroupValueAttribute, self).lock_delete()


# grupo de valores para features special
class GroupValueFeatureSpecial(GroupValues):
    def __fields__(self, info):
        fields = super(GroupValueFeatureSpecial, self).__fields__(info)
        fields.append(('options_value_feature_special', _('Option value')))
        return fields

    def lock_delete(self):
        if self.options_value_feature_special.exists():
            return _("Cannot delete group value model, relationship between group value model and options")
        elif self.feature_specials.exists():
            return _("Cannot delete group value model, relationship between group value model and feature special")
        else:
            return super(GroupValueFeatureSpecial, self).lock_delete()


# opciones de los grupos de valores
class OptionValues(CodenerixModel):  # META: Abstract class
    class Meta(CodenerixModel.Meta):
        abstract = True

    def __fields__(self, info):
        fields = []
        for lang_code in settings.LANGUAGES_DATABASES:
            fields.append(('{}__description'.format(lang_code.lower()), _(lang_code.upper())))
        return fields

    def __unicode__(self):
        string = []
        for lang_code in settings.LANGUAGES_DATABASES:
            string.append(u"{}: {}".format(lang_code, getattr(self, lang_code.lower())))

        return u"{}".format(" | ".join(string))

    def __str__(self):
        return self.__unicode__()


# opciones de los grupos de valores para features
class OptionValueFeature(OptionValues):
    group = models.ForeignKey(GroupValueFeature, on_delete=models.CASCADE, related_name='options_value_feature', verbose_name=_("Options value"))


# opciones de los grupos de valores para attributes
class OptionValueAttribute(OptionValues):
    group = models.ForeignKey(GroupValueAttribute, on_delete=models.CASCADE, related_name='options_value_attribute', verbose_name=_("Options value"))


# opciones de los grupos de valores features special
class OptionValueFeatureSpecial(OptionValues):
    group = models.ForeignKey(GroupValueFeatureSpecial, on_delete=models.CASCADE, related_name='options_value_feature_special', verbose_name=_("Options value"))


# caracteristicas (comunes a todos los productos (resolución, RAM))
class Feature(GenAttr):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='features', verbose_name=_("Family"), blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='features', verbose_name=_("Category"), blank=True, null=True)
    list_value = models.ForeignKey(GroupValueFeature, on_delete=models.CASCADE, related_name='features', verbose_name=_("List value"), blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            obj = Feature.objects.get(pk=self.pk)
            if obj.price != self.price:
                result = super(Feature, self).save(*args, **kwargs)
                for pf in ProductFinal.objects.filter(product__product_features__feature=self):
                    pf.recalculate()
            else:
                result = super(Feature, self).save(*args, **kwargs)
        else:
            result = super(Feature, self).save(*args, **kwargs)
        return result

    def lock_delete(self):
        if self.product_features.exists():
            return _("Cannot delete feature model, relationship between feature model and products")
        else:
            return super(Feature, self).lock_delete()


# atributos (subconjunto de productos (color, talla))
class Attribute(GenAttr):
    """
    los atributos están relacionados entre ellos
    el order indica el orden en el que aparcerán
    """
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='attributes', verbose_name=_("Family"), blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes', verbose_name=_("Category"), blank=True, null=True)
    attribute = models.ForeignKey("self", on_delete=models.CASCADE, related_name='attributes', verbose_name=_("Attribute"), blank=True, null=True)
    list_value = models.ForeignKey(GroupValueAttribute, on_delete=models.CASCADE, related_name='attributes', verbose_name=_("List value"), blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            obj = Attribute.objects.get(pk=self.pk)
            if obj.price != self.price:
                result = super(Attribute, self).save(*args, **kwargs)
                for pf in ProductFinal.objects.filter(products_final_attr__attribute=self):
                    pf.recalculate()
            else:
                result = super(Attribute, self).save(*args, **kwargs)
        else:
            result = super(Attribute, self).save(*args, **kwargs)
        return result

    def lock_delete(self):
        if self.products_final_attr.exists():
            return _("Cannot delete attribute model, relationship between attribute model and products final")
        else:
            return super(Attribute, self).lock_delete()


# caracteristicas especiales (unico por producto (imei, fecha caducidad))
class FeatureSpecial(GenAttr):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='feature_specials', verbose_name=_("Family"), blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='feature_specials', verbose_name=_("Category"), blank=True, null=True)
    list_value = models.ForeignKey(GroupValueFeatureSpecial, on_delete=models.CASCADE, related_name='feature_specials', verbose_name=_("List value"), blank=True, null=True)
    unique = models.BooleanField(_("The value must unique"), blank=True, null=False, default=True)

    def __fields__(self, info):
        fields = super(FeatureSpecial, self).__fields__(info)
        fields.append(('unique', _("The value must unique")))
        return fields

    def save(self, *args, **kwargs):
        if self.pk:
            obj = FeatureSpecial.objects.get(pk=self.pk)
            if obj.price != self.price:
                result = super(FeatureSpecial, self).save(*args, **kwargs)
                for pf in ProductFinal.objects.filter(product__feature_special=self):
                    pf.recalculate()
            else:
                result = super(FeatureSpecial, self).save(*args, **kwargs)
        else:
            result = super(FeatureSpecial, self).save(*args, **kwargs)
        return result

    def lock_delete(self):
        if self.products.exists():
            return _("Cannot delete feature special model, relationship between feature special model and products")
        else:
            return super(FeatureSpecial, self).lock_delete()


# Marcas
class Brand(CodenerixModel, GenImageFileNull):
    outstanding = models.BooleanField(_("Outstanding"), blank=True, null=False, default=True)
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    show_menu = models.BooleanField(_("Show menu"), blank=True, null=False, default=True)

    def __unicode__(self):
        name_res = _("Missing brand name")
        for lang_code, lang_name in settings.LANGUAGES:
            translation = getattr(self, lang_code.lower(), None)
            if translation is not None:
                if translation.name and len(translation.name) > 0:
                    name_res = u"{}".format(smart_str(translation.name))
                else:
                    name_res = u"{}".format(smart_str(translation.slug))
        return name_res

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('outstanding', _("Outstanding")))
        fields.append(('order', _("Order")))
        fields.append(('show_menu', _("Show menu")))
        return fields

    def lock_delete(self):
        if self.products.exists():
            return _("Cannot delete brand model, relationship between brand model and products")
        else:
            return super(Brand, self).lock_delete()


# definición de productos
class GenProduct(CodenerixModel):  # META: Abstract class
    """
    @warning: brand no debe permitir nulo. Recordar para la limpieza de la bbdd.
    """
    # se hace abstracta para que hereden product y productfinal
    class Meta(CodenerixModel.Meta):
        abstract = True

    model = models.CharField(_("Model"), max_length=250, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name=_("Brand"), blank=True, null=True)
    tax = models.ForeignKey(TypeTax, on_delete=models.CASCADE, related_name='products', verbose_name=_("Tax (%)"), null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='products', verbose_name=_("Family"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_("Category"))
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products', verbose_name=_("Subcategory"))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    code = models.CharField(_("Code"), max_length=250, blank=False, null=False, unique=True)
    price_base = models.DecimalField(_("Price base"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0)
    # producto para la venta
    of_sales = models.BooleanField(_("Sales"), blank=True, null=False, default=True)
    # producto para la compra
    of_purchase = models.BooleanField(_("Purchase"), blank=True, null=False, default=True)
    # es necesario que el producto tenga stock para su venta
    force_stock = models.BooleanField(_("Force stock"), blank=True, null=False, default=True)
    url_video = models.CharField(_("Url Video"), max_length=250, blank=True, null=True)
    # indica si es necesario tener una caracteristica especial obligatoriamente
    feature_special = models.ForeignKey(FeatureSpecial, on_delete=models.CASCADE, related_name='products', verbose_name=_("Feature special"), blank=True, null=True)
    packing_cost = models.DecimalField(_("Packing cost"), blank=False, null=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0)
    weight = models.FloatField(_("Weight"), blank=False, null=False, default=0)
    caducable = models.BooleanField(_("Caducable"), blank=True, null=False, default=False)

    def __unicode__(self):
        return u"{}".format(smart_str(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        lang = get_language_database()

        fields = []
        fields.append(('family__{}__name'.format(lang), _("Family")))
        fields.append(('category__{}__name'.format(lang), _("Category")))
        fields.append(('subcategory__{}__name'.format(lang), _("Subcategory")))
        fields.append(('public', _("Public")))
        fields.append(('tax', _("Tax")))
        fields.append(('code', _("Code")))
        fields.append(('price_base', _("Price base")))
        fields.append(('of_sales', _("Sales")))
        fields.append(('of_purchase', _("Purchase")))
        fields.append(('force_stock', _("Force stock")))
        fields.append(('url_video', _("Url Video")))
        fields.append(('feature_special', _("Feature special")))
        fields.append(('packing_cost', _("Packing cost")))
        fields.append(('weight', _("Weight")))
        fields.append(('caducable', _("Caducable")))

        return fields

    def __searchQ__(self, info, text):
        lang = get_language_database()

        text_filters = {}
        text_filters['product_slug'] = Q(**{"{}__slug__icontains".format(lang): text})
        text_filters['product_name'] = Q(**{"{}__name__icontains".format(lang): text})
        try:
            text_filters['identifier'] = Q(pk=int(text))
        except ValueError:
            pass
        return text_filters


# productos
class Product(CustomQueryMixin, GenProduct):

    def lock_delete(self):
        if self.products_final.exists():
            return _("Cannot delete product model, relationship between product model and products final")
        elif self.products_image.exists():
            return _("Cannot delete product model, relationship between product model and products image")
        elif self.products_document.exists():
            return _("Cannot delete product model, relationship between product model and products document")
        elif self.product_features.exists():
            return _("Cannot delete product model, relationship between product model and products feature")
        elif self.products_related.exists():
            return _("Cannot delete product model, relationship between product model and products related")
        elif self.products_related_sold.exists():
            return _("Cannot delete product model, relationship between product model and products related sold")
        else:
            return super(Product, self).lock_delete()

    def save(self, *args, **kwargs):
        if self.pk:
            obj = Product.objects.get(pk=self.pk)
            if obj.price_base != self.price_base or obj.tax != self.tax:
                result = super(Product, self).save(*args, **kwargs)
                for pf in self.products_final.all():
                    pf.recalculate()
            else:
                result = super(Product, self).save(*args, **kwargs)
        else:
            result = super(Product, self).save(*args, **kwargs)
        return result

    def pass_to_productfinal(self, ean13=None):
        get_class = lambda x: globals()[x]

        try:
            with transaction.atomic():
                pf = ProductFinal()
                pf.product = self
                pf.code = self.code
                pf.price_base_local = self.price_base
                if ean13:
                    pf.ean13 = ean13
                pf.save()

                for lang_code in settings.LANGUAGES_DATABASES:
                    lang = getattr(self, lang_code.lower(), None)
                    if lang:
                        model_name = "{}Text{}".format('ProductFinal', lang_code)
                        model = get_class(model_name)
                        pft = model()
                        pft.product = pf
                        pft.meta_title = getattr(lang, 'meta_title', None)
                        pft.meta_description = getattr(lang, 'meta_description', None)
                        pft.description_short = getattr(lang, 'description_short', None)
                        pft.description_long = getattr(lang, 'description_long', None)
                        pft.slug = getattr(lang, 'slug', None)
                        pft.name = getattr(lang, 'name', None)
                        pft.public = getattr(lang, 'public', None)
                        pft.meta_title = getattr(lang, 'meta_title', None)
                        pft.meta_description = getattr(lang, 'meta_description', None)
                        pft.meta_keywords = getattr(lang, 'meta_keywords', None)
                        pft.tags = getattr(lang, 'tags', None)
                        pft.save()
        except IntegrityError as e:
            raise IntegrityError(e)

    @classmethod
    def find_product(cls, query, lang, onlypublic=False):
        product = cls.query_or(
            query,
            "pk",
            "price_base",
            # "product__pk",
            "model",
            "code",
            "url_video",
            # "product__brand__{}__name".format(lang),
            # "product__brand__{}__slug".format(lang),
            # "product__brand__image",
            # "product__brand__outstanding",
            # "product__family",
            # "product__family__code",
            "family__pk".format(lang),
            "family__{}__slug".format(lang),
            # "product__family__image",
            "family__{}__name".format(lang),
            "family__{}__description".format(lang),
            "category__pk",
            # "product__category",
            # "product__category__code".format(lang),
            # "product__category__image".format(lang),
            "category__{}__slug".format(lang),
            "category__{}__name".format(lang),
            "category__{}__description".format(lang),
            # "product__subcategory",
            # "product__subcategory__code",
            # "product__subcategory__image",
            "subcategory__pk",
            "subcategory__{}__slug".format(lang),
            "subcategory__{}__name".format(lang),
            "subcategory__{}__description".format(lang),
            "family__image",
            "family__icon",
            "category__image",
            "subcategory__image",
            "tax__tax",
            "{}__meta_title".format(lang),
            "{}__meta_description".format(lang),
            "{}__meta_keywords".format(lang),
            "{}__description_short".format(lang),
            "{}__description_long".format(lang),
            "{}__slug".format(lang),
            "{}__name".format(lang),
            "weight",
            family_image="family__image".format(lang),
            family_name="family__{}__name".format(lang),
            family_slug="family__{}__slug".format(lang),
            family_description="family__{}__description".format(lang),
            category_image="category__image".format(lang),
            category_slug="category__{}__slug".format(lang),
            category_name="category__{}__name".format(lang),
            category_description="category__{}__description".format(lang),
            subcategory_image="subcategory__image".format(lang),
            subcategory_slug="subcategory__{}__slug".format(lang),
            subcategory_name="subcategory__{}__name".format(lang),
            subcategory_description="subcategory__{}__description".format(lang),
            tax="tax__tax",
            meta_title="{}__meta_title".format(lang),
            meta_description="{}__meta_description".format(lang),
            meta_keywords="{}__meta_keywords".format(lang),
            description_short="{}__description_short".format(lang),
            description_long="{}__description_long".format(lang),
            name="{}__name".format(lang),
            slug="{}__slug".format(lang),
            pop_annotations=True
        )
        if onlypublic:
            product = product.exclude(public=False)
        product = product.first()

        # if product:
        #     product_final = cls.objects.get(pk=product['pk'])
        #     prices = product_final.calculate_price()
        #     product['price'] = prices['price_total']

        return product


# productos relacionados mas vendidos
class ProductRelationSold(CodenerixModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False, related_name='products_related', verbose_name=_("Product"))
    related = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False, related_name='products_related_sold', verbose_name=_("Products related"))
    hits = models.SmallIntegerField(_("Hits"), blank=True, null=True)

    class Meta(CodenerixModel.Meta):
        unique_together = (('product', 'related'), )

    def __unicode__(self):
        return u"{} ({})".format(smart_str(self.product), smart_str(self.hits))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('product', _("Product")))
        fields.append(('related', _("Products related")))
        fields.append(('hits', _("Hits")))
        return fields


# imagenes de productos
class ProductImage(CodenerixModel, GenImageFile):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_image', verbose_name=_("Product"))
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    principal = models.BooleanField(_("Principal"), blank=False, null=False, default=False)
    flagship_product = models.BooleanField(_("Flagship product"), default=False)
    outstanding = models.BooleanField(_("Outstanding"), default=False)

    def __unicode__(self):
        return u"{} ({})".format(smart_str(self.product), smart_str(self.order))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('product', _("Product")))
        fields.append(('order', _("Order")))
        fields.append(('public', _("Public")))
        fields.append(('principal', _("Principal")))
        return fields

    # Save necesita un check que indique si debe comprobar o no los productos destacados y productos estrella.
    @transaction.atomic
    def save(self, *args, **kwards):
        if self.principal:
            ProductImage.objects.filter(product=self.product).exclude(pk=self.pk).update(principal=False)
        elif not ProductImage.objects.exclude(pk=self.pk).filter(principal=True).exists():
            self.principal = True

        # Si no hay ninguna imagen con el check de producto estrella, marco esta.
        if self.flagship_product:
            ProductImage.objects.filter(product=self.product, flagship_product=True).exclude(pk=self.pk).update(flagship_product=False)
        elif not ProductImage.objects.filter(product=self.product, flagship_product=True).exclude(pk=self.pk).exists():
            self.flagship_product = True

        # Producto destacado
        if self.outstanding:
            ProductImage.objects.filter(product=self.product, outstanding=True).exclude(pk=self.pk).update(outstanding=False)
        elif not ProductImage.objects.filter(product=self.product, outstanding=True).exclude(pk=self.pk).exists():
            self.outstanding = True

        return super(ProductImage, self).save(*args, **kwards)


# documentos de productos
class ProductDocument(CodenerixModel, GenDocumentFile):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_document', verbose_name=_("Product"))
    public = models.BooleanField(_("Public"), blank=False, null=False, default=False)

    def __unicode__(self):
        return u"{}".format(smart_str(self.product))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('product', _("Product")))
        fields.append(('public', _("Public")))
        return fields


# producto final (1 producto muchos atributos) (pulgadas, RAM)
class ProductFinal(CustomQueryMixin, CodenerixModel):
    """
    el stock se relaciona con esta clase
    definición de productos individuales
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False, related_name='products_final', verbose_name=_('Product'))
    # productos relacionados
    related = models.ManyToManyField("ProductFinal", blank=True, related_name='productsrelated', symmetrical=False)
    related_accesory = models.ManyToManyField("ProductFinal", blank=True, related_name='productsrelatedaccesory', symmetrical=False)
    offer = models.BooleanField(_("Offer"), blank=True, null=False, default=False)
    outstanding = models.BooleanField(_("Outstanding"), blank=True, null=False, default=False)
    most_sold = models.BooleanField(_("Most sold"), blank=True, null=False, default=False)
    # price without tax
    price_base = models.DecimalField(_("Price base"), null=False, blank=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)
    # price with tax
    price = models.DecimalField(_("Price"), null=False, blank=False, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, default=0, editable=False)
    ean13 = models.CharField(_("EAN-13"), null=True, blank=True, max_length=13)

    reviews_value = models.FloatField(_("Reviews"), null=False, blank=False, default=0, editable=False)
    reviews_count = models.IntegerField(_("Reviews count"), null=False, blank=False, default=0, editable=False)
    sample = models.BooleanField(_("Sample"), blank=True, null=False, default=False, help_text=_('If this option is checked the product can not be sold'))

    code = models.CharField(_("Code"), max_length=250, blank=True, null=True, unique=True, help_text=_('If it is empty, code is equal to code product'))
    price_base_local = models.DecimalField(_("Price base"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, help_text=_('If it is empty, price base is equal to price base of product'))

    packing_cost = models.DecimalField(_("Packing cost"), blank=True, null=True, max_digits=CURRENCY_MAX_DIGITS, decimal_places=CURRENCY_DECIMAL_PLACES, help_text=_('If it is empty, packing cost is equal to packing cost of product'))
    weight = models.FloatField(_("Weight"), blank=True, null=True, help_text=_('If it is empty, weight is equal to weight of product'))

    def __str__(self):
        lang = get_language_database()
        lang_model = getattr(self, '{}'.format(lang), None)
        if lang_model:
            name = lang_model.name
        else:
            name = self.product

        if self.ean13:
            name = u"{} ({})".format(smart_str(name), self.ean13)
        else:
            name = u"{}".format(name)
        return name

    def __unicode__(self):
        return self.__str__()

    def get_name(self):
        lang = get_language_database()
        lang_model = getattr(self, '{}'.format(lang), None)
        if lang_model:
            name = lang_model.name
        else:
            name = self.product
        return name

    def __fields__(self, info):
        lang = get_language_database()
        fields = []
        fields.append(('code', _("Code")))
        fields.append(('product__code', _("Product Code")))
        fields.append(('{}__name'.format(lang), _("Product")))
        fields.append(('product__family__{}__name'.format(lang), _("Family")))
        fields.append(('product__category__{}__name'.format(lang), _("Category")))
        fields.append(('product__subcategory__{}__name'.format(lang), _("Subcategory")))
        fields.append(('{}__public'.format(lang), _("Public")))
        fields.append(('price', _("Price")))
        fields.append(('is_pack', _("Is pack")))
        fields.append(('sample', _("Sample")))
        return fields

    def __searchF__(self, info):
        lang = get_language_database()

        fields = {}
        fields['product__family__{}__name'.format(lang)] = (_('Family'), lambda x, lang=lang: Q(**{'product__family__{}__name__icontains'.format(lang): x}), 'input')
        fields['product__category__{}__name'.format(lang)] = (_('Category'), lambda x, lang=lang: Q(**{'product__category__{}__name__icontains'.format(lang): x}), 'input')
        fields['product__subcategory__{}__name'.format(lang)] = (_('Subcategory'), lambda x, lang=lang: Q(**{'product__subcategory__{}__name__icontains'.format(lang): x}), 'input')
        fields['{}__name'.format(lang)] = (_('Product'), lambda x, lang=lang: Q(**{'{}__name__icontains'.format(lang): x}), 'input')
        fields['product__code'] = (_('Product Code'), lambda x, lang=lang: Q(**{'product__code__icontains': x}), 'input')
        return fields

    def __searchQ__(self, info, text):
        lang = get_language_database()

        qobject = qobject_builder_string_search(
            [
                "{}__name".format(lang),
                "{}__slug".format(lang),
            ],
            text
        )

        text_filters = {}
        text_filters['product_name'] = qobject

        return text_filters

    def save(self, *args, **kwards):
        self.recalculate(commit=False)
        return super(ProductFinal, self).save(*args, **kwards)

    def recalculate(self, commit=True):
        prices = self.calculate_price()
        if self.price != prices['price_total'] or self.price_base != prices['price_base']:
            self.price = prices['price_total']
            self.price_base = prices['price_base']
            if commit:
                self.save()

    def lock_delete(self):
        if self.products_final_attr.exists():
            return _("Cannot delete product final model, relationship between product final model and products final attributes")
        elif self.productfinals_image.exists():
            return _("Cannot delete product final model, relationship between product final model and products final image")
        elif self.products_unique.exists():
            return _("Cannot delete product final model, relationship between product final model and products unique")
        elif self.flagship_products.exists():
            return _("Cannot delete product final model, relationship between product final model and products flaship")
        else:
            return super(ProductFinal, self).lock_delete()

    def calculate_price(self):
        if self.price_base_local is None:
            price = self.product.price_base
        else:
            price = self.price_base_local
        tax = self.product.tax.tax
        price_base = price

        # atributos
        update = True
        for attr in self.products_final_attr.all().order_by('-updated'):
            if update:
                if attr.attribute.type_price == TYPE_PRICE_FINAL:
                    price = Decimal(attr.attribute.price)
                    update = False
                elif attr.attribute.type_price == TYPE_PRICE_INCREASE:
                    price += Decimal(attr.attribute.price)
                elif attr.attribute.type_price == TYPE_PRICE_PERCENTAGE:
                    price += price_base * Decimal(attr.attribute.price / 100.0)

        # caracteristicas
        if update:
            for feature in self.product.product_features.all().order_by('-updated'):
                if update:
                    if feature.feature.type_price == TYPE_PRICE_FINAL:
                        price = Decimal(feature.feature.price)
                        update = False
                    elif feature.feature.type_price == TYPE_PRICE_INCREASE:
                        price += Decimal(feature.feature.price)
                    elif feature.feature.type_price == TYPE_PRICE_PERCENTAGE:
                        price += price_base * Decimal(feature.feature.price / 100.0)

        # caracteristicas especiales
        if update and self.product.feature_special:
            if self.product.feature_special.type_price == TYPE_PRICE_FINAL:
                price = Decimal(self.product.feature_special.price)
            elif self.product.feature_special.type_price == TYPE_PRICE_INCREASE:
                price += Decimal(self.product.feature_special.price)
            elif self.product.feature_special.type_price == TYPE_PRICE_PERCENTAGE:
                price += price_base * Decimal(self.product.feature_special.price / 100.0)

        result = {}
        result['price_base'] = price
        result['tax'] = price * Decimal(tax) / 100
        result['price_total'] = price + result['tax']
        return result

    def is_pack(self):
        return self.productfinals_option.exists()

    @property
    def ispack(self):
        return self.is_pack()

    @classmethod
    def get_recommended_products(cls, lang, family=None, category=None, subcategory=None):
        products = []
        query = Q(most_sold=True) | Q(product__products_image__principal=True)
        if family is not None:
            query &= Q(product__family=category)
        if category is not None:
            query &= Q(product__category=category)
        if subcategory is not None:
            query &= Q(product__subcategory=subcategory)
        for product in cls.query_or(
            query,
            "{}__slug".format(lang),
            "offer",
            "created",
            "offer",
            "pk",
            "product__{}__name".format(lang),
            "product__model",
            "product__brand__{}__name".format(lang),
            "product__products_image__image",
            "{}__meta_title".format(lang),
            slug="{}__slug".format(lang),
            meta_title="{}__meta_title".format(lang),
            image="product__products_image__image",
            name="product__{}__name".format(lang),
            pop_annotations=True
        ):
            product['new'] = 1 if (timezone.now() - product['created']).days <= settings.CDNX_PRODUCTS_NOVELTY_DAYS else 0
            products.append(product)

        return products

    @classmethod
    def get_outstanding_products(cls, lang, family=None, category=None, subcategory=None, limit=16):
        products = []
        query = Q(outstanding=True) & (Q(product__products_image__principal=True) | Q(productfinals_image__principal=True))
        if family is not None:
            query &= Q(product__family=family)
        if category is not None:
            query &= Q(product__category=category)
        if subcategory is not None:
            query &= Q(product__subcategory=subcategory)

        qset = cls.objects.filter(
            query
        ).values(
            "{}__slug".format(lang),
            "offer",
            "created",
            "offer",
            "pk",
            "sample",
            "code",
            "product__tax__tax",
            "product__{}__name".format(lang),
            "product__model",
            "product__category__{}__name".format(lang),
            "product__brand__{}__name".format(lang),
            "product__products_image__image",
            "{}__meta_title".format(lang)
        ).annotate(
            slug=F("{}__slug".format(lang)),
            meta_title=F("{}__meta_title".format(lang)),
            image_product=F("product__products_image__image"),
            image_productfinal=F("productfinals_image__image"),
            name=F("product__{}__name".format(lang)),
            category_name=F("product__category__{}__name".format(lang))
        )[:limit]

        for product in qset:
            prices = cls.objects.get(pk=product['pk']).calculate_price()
            product['pop_annotations'] = True
            product['price'] = prices['price_total']
            product['new'] = 1 if (timezone.now() - product['created']).days <= settings.CDNX_PRODUCTS_NOVELTY_DAYS else 0
            if product['image_productfinal']:
                product['image'] = product['image_productfinal']
            else:
                product['image'] = product['image_product']
            products.append(product)

        return products

    @classmethod
    def get_products(cls, lang, family=None, category=None, subcategory=None, brand=None):
        products = []
        query = Q(product__products_image__principal=True)

        if family is not None:
            query &= Q(product__family=family)
        if category is not None:
            query &= Q(product__category=category)
        if subcategory is not None:
            query &= Q(product__subcategory=subcategory)
        if brand is not None:
            query &= Q(product__brand=brand)
        for product in cls.query_or(
            query,
            "{}__slug".format(lang),
            "offer",
            "created",
            "offer",
            "pk",
            "product__tax__tax",
            "product__{}__name".format(lang),
            "product__model",
            "product__brand__{}__name".format(lang),
            "product__products_image__image",
            "{}__meta_title".format(lang),
            slug="{}__slug".format(lang),
            meta_title="{}__meta_title".format(lang),
            image="product__products_image__image",
            name="product__{}__name".format(lang),
            pop_annotations=True
        ):
            prices = cls.objects.get(pk=product['pk']).calculate_price()
            product['price'] = prices['price_total']
            product['new'] = 1 if (timezone.now() - product['created']).days <= settings.CDNX_PRODUCTS_NOVELTY_DAYS else 0
            products.append(product)

        return products

    @classmethod
    def find_product(cls, query, lang, onlypublic=False):
        product = cls.query_or(
            query,
            "pk",
            "offer",
            "outstanding",
            "price",
            "sample",
            "reviews_value",
            "reviews_count",
            "product__pk",
            "product__model",
            "product__code",
            "product__url_video",
            "product__brand__{}__name".format(lang),
            "product__brand__{}__slug".format(lang),
            "product__brand__image",
            "product__brand__outstanding",
            "product__family",
            "product__family__code",
            "product__family__{}__slug".format(lang),
            "product__family__image",
            "product__family__{}__name".format(lang),
            "product__family__{}__description".format(lang),
            "product__category",
            "product__category__code".format(lang),
            "product__category__image".format(lang),
            "product__category__{}__slug".format(lang),
            "product__category__{}__name".format(lang),
            "product__category__{}__description".format(lang),
            "product__subcategory",
            "product__subcategory__code",
            "product__subcategory__image",
            "product__subcategory__{}__slug".format(lang),
            "product__subcategory__{}__name".format(lang),
            "product__subcategory__{}__description".format(lang),
            "product__tax__tax",
            "product__family__image",
            "product__family__icon",
            "product__category__image",
            "product__subcategory__image",
            "{}__meta_title".format(lang),
            "{}__meta_description".format(lang),
            "{}__meta_keywords".format(lang),
            "{}__description_short".format(lang),
            "{}__description_long".format(lang),
            "{}__description_sample".format(lang),
            "{}__slug".format(lang),
            "{}__name".format(lang),
            "product__{}__meta_title".format(lang),
            "product__{}__meta_description".format(lang),
            "product__{}__description_short".format(lang),
            "product__{}__description_long".format(lang),
            "weight",
            "product__weight",
            "code",
            family_name="product__family__{}__name".format(lang),
            family_slug="product__family__{}__slug".format(lang),
            family_description="product__family__{}__description".format(lang),
            category_slug="product__category__{}__slug".format(lang),
            category_name="product__category__{}__name".format(lang),
            category_description="product__category__{}__description".format(lang),
            subcategory_slug="product__subcategory__{}__slug".format(lang),
            subcategory_name="product__subcategory__{}__name".format(lang),
            subcategory_description="product__subcategory__{}__description".format(lang),
            family_image="product__family__image",
            family_icon="product__family__icon",
            category_image="product__category__image",
            subcategory_image="product__subcategory__image",
            tax="product__tax__tax",
            meta_title="{}__meta_title".format(lang),
            meta_description="{}__meta_description".format(lang),
            meta_keywords="{}__meta_keywords".format(lang),
            description_short="{}__description_short".format(lang),
            description_long="{}__description_long".format(lang),
            description_sample="{}__description_sample".format(lang),
            name="{}__name".format(lang),
            slug="{}__slug".format(lang),
            product_meta_title="product__{}__meta_title".format(lang),
            product_meta_description="product__{}__meta_description".format(lang),
            product_description_short="product__{}__description_short".format(lang),
            product_description_long="product__{}__description_long".format(lang),
            stars="reviews_value",
            pop_annotations=True
        )
        if onlypublic:
            product = product.exclude(product__model=False)
        product = product.first()

        if product:
            product_final = cls.objects.get(pk=product['pk'])
            prices = product_final.calculate_price()
            product['price'] = prices['price_total']

        return product

    def get_value_product_unique(self, pos):
        """
        Return all products unique relationship with POS's Storage (only salable zones)
        """
        qs = ProductUnique.objects.filter(
            box__box_structure__zone__storage__in=pos.storage_stock.filter(storage_zones__salable=True),
            product_final=self
        )
        return qs


# imagenes de productos
class ProductFinalImage(CodenerixModel, GenImageFile):
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='productfinals_image', verbose_name=_("Product Final"))
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    principal = models.BooleanField(_("Principal"), blank=False, null=False, default=False)
    flagship_product = models.BooleanField(_("Flagship product"), default=False)
    outstanding = models.BooleanField(_("Outstanding"), default=False)

    def __unicode__(self):
        return u"{} ({})".format(smart_str(self.product_final), smart_str(self.order))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _("Product")))
        fields.append(('order', _("Order")))
        fields.append(('public', _("Public")))
        fields.append(('principal', _("Principal")))
        return fields

    # Save necesita un check que indique si debe comprobar o no los productos destacados y productos estrella.
    @transaction.atomic
    def save(self, *args, **kwards):
        if self.principal:
            ProductFinalImage.objects.filter(product_final=self.product_final).exclude(pk=self.pk).update(principal=False)
        elif not ProductFinalImage.objects.exclude(pk=self.pk).filter(principal=True).exists():
            self.principal = True

        # Si no hay ninguna imagen con el check de producto estrella, marco esta.
        if self.flagship_product:
            ProductFinalImage.objects.filter(product_final=self.product_final, flagship_product=True).exclude(pk=self.pk).update(flagship_product=False)
        elif not ProductFinalImage.objects.filter(product_final=self.product_final, flagship_product=True).exclude(pk=self.pk).exists():
            self.flagship_product = True

        # Producto destacado
        if self.outstanding:
            ProductFinalImage.objects.filter(product_final=self.product_final, outstanding=True).exclude(pk=self.pk).update(outstanding=False)
        elif not ProductFinalImage.objects.filter(product_final=self.product_final, outstanding=True).exclude(pk=self.pk).exists():
            self.outstanding = True

        return super(ProductFinalImage, self).save(*args, **kwards)


# producto final (1 producto muchos atributos) (pulgadas, RAM)
class ProductFinalAttribute(CodenerixModel):
    """
    el stock se relaciona con esta clase
    definición de productos individuales
    """
    product = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, blank=False, null=False, related_name='products_final_attr', verbose_name=_('Product'))
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, blank=False, null=True, related_name='products_final_attr', verbose_name=_('Attributes'))

    value = models.CharField(_("Value"), max_length=80)

    def __unicode__(self, show_attribute=True):
        value = ''
        if self.attribute.type_value == TYPE_VALUE_BOOLEAN:
            value = bool(self.value) and _('True') or _('False')
        elif self.attribute.type_value == TYPE_VALUE_FREE:
            value = self.value
        elif self.attribute.type_value == TYPE_VALUE_LIST:
            lang = get_language_database()
            field = '{}__description'.format(lang)
            ov = OptionValueAttribute.objects.filter(
                group=self.attribute.list_value,
                pk=int(self.value)
            ).values(
                field
            ).first()
            if ov:
                value = ov[field]
        if show_attribute:
            return u"{}: {}".format(smart_str(self.attribute), smart_str(value))
        else:
            return u"{}".format(smart_str(value))

    def __str__(self):
        return self.__unicode__()

    def get_value_attribute(self):
        return self.__unicode__(show_attribute=False)

    def __fields__(self, info):
        fields = []
        fields.append(('product', _("Product")))
        fields.append(('attribute', _("Attribute")))
        fields.append(('get_value_attribute', _("Value")))
        return fields

    @staticmethod
    def validate(pk, product, attribute):
        if pk is None and ProductFinalAttribute.objects.filter(product__pk=product, attribute__pk=attribute).exists():
            msg = _('A product final can not have the same attribute')
        elif ProductFinalAttribute.objects.filter(product__pk=product, attribute__pk=attribute).exclude(pk=pk).exists():
            msg = _('A product final can not have the same attribute')
        else:
            msg = None

        return msg

    def save(self, *args, **kwargs):
        msg = ProductFinalAttribute.validate(self.pk, self.product.pk, self.attribute.pk)
        if msg:
            raise ProductFinalAttributeOnlyOne(msg)
        return super(ProductFinalAttribute, self).save(*args, **kwargs)


# valor de las caracteristicas del producto (talla, color)
class ProductFeature(CodenerixModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('Product'), related_name='product_features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, blank=False, null=False, verbose_name=_('Feature'), related_name='product_features')
    value = models.CharField(_("Value"), max_length=80)

    def __unicode__(self):
        return u"{}".format(smart_str(self.product))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('product', _("Product")))
        fields.append(('feature', _("Feature")))
        fields.append(('value', _("Value")))
        return fields


# valor de las caracteristicas especiales del producto final (imei, fecha caducidad)
class ProductUnique(CodenerixModel):
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, blank=False, null=False, related_name='products_unique', verbose_name=_('Product final'))
    box = models.ForeignKey(StorageBox, on_delete=models.CASCADE, blank=False, null=False, related_name='products_unique', verbose_name=_('Box'))
    value = models.CharField(_("Value"), max_length=80, null=True, blank=True)
    caducity = models.DateField(_("Caducity"), blank=True, null=True, default=None)
    stock_original = models.FloatField(_("Stock original"), null=False, blank=False, default=0)
    stock_real = models.FloatField(_("Stock real"), null=False, blank=False, default=0, editable=False)
    stock_locked = models.FloatField(_("Stock locked"), null=False, blank=False, default=0, editable=False)

    def __str__(self):
        if self.value:
            result = self.value
        else:
            result = self.product_final
        return u"{} ({})".format(smart_str(result), self.box)

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _("Product")))
        fields.append(('product_final__product__feature_special', _("Feature special")))
        fields.append(('value', _("Value")))
        fields.append(('box', _("Box")))
        fields.append(('stock_original', _("Stock original")))
        fields.append(('stock_real', _("Stock real")))
        fields.append(('stock_locked', _("Stock locked")))
        return fields

    def locked_stock(self, quantity):
        self.stock_locked += quantity
        self.save()

    @transaction.atomic
    def duplicate(self, quantity, locked=False):
        # Do we have enought stock?
        if self.stock_real > quantity:
            if locked:
                # Do we have enought locked stock?
                if self.stock_lock>=quantity:
                    newlock = quantity
                else:
                    raise IOError("Not enought locked products to split")
            else:
                # Find available stock here
                available = self.stock_real-self.stock_lock
                # Do you have enought free stock?
                if available>=quantity:
                    newlock = 0
                else:
                    raise IOError("Not enought free products to split")

            # Make a copy from the actual ProductUnique
            new_line = copy.copy(self)
            new_line.pk = None
            # Complete stocks as calculated
            new_line.stock_original = quantity
            new_line.stock_real = quantity
            new_line.stock_lock = newlock
            new_line.save()
            self.stock_original -= quantity
            self.stock_real -= quantity
            self.stock_lock -= newlock
            self.save()

            # Check PurchaseAlbaran and link them to the new product
            for pal in self.line_albaran_purchases.all():
                pal.product_unique.add(new_line)
                pal.save()

            # Return new ProductUnique
            return new_line
        elif self.stock_real == quantity:
            raise IOError("No need to split, you are taking all units from here")
        else:
            raise IOError("Not enought products to split")

    def save(self, *args, **kwargs):
        product_final = ProductFinal.objects.filter(pk=self.product_final_id).first()
        # se comprueba que no se repite el valor de las caracteristicas especiales de los productos finales cuando sean unicas
        if product_final:
            if product_final.product.feature_special and product_final.product.feature_special.unique:
                if ProductUnique.objects.filter(
                    value=self.value,
                    product_final__product=product_final.product
                ).exclude(
                    pk=self.pk
                ).exists():
                    raise ProductUniqueAlreadyExists(_('Ya existe un producto unico con el valor de la caracteristicas especial'))
                elif self.stock_original > 1:
                    raise ProductUniqueQuantityExceeded(_('Este producto unico solo se puede cargar en cantidades de uno, porque la caracteristica especian indica que debe el valor no se puede repetir'))

        else:
            raise ProductUniqueNotProductFinal(_("Product final not seleted"))

        if self.pk is None:
            self.stock_real = self.stock_original
            self.stock_locked = 0

        return super(ProductUnique, self).save(*args, **kwargs)


# producto estrella (solo un registro publico)
class FlagshipProduct(CustomQueryMixin, CodenerixModel, GenImageFile):
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, blank=False, null=False, related_name='flagship_products', verbose_name=_('Flagship product'))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    view_video = models.BooleanField(_("View video"), blank=True, null=False, default=False)
    orientazion = models.CharField(_("Orientazion"), max_length=2, choices=TYPE_ORIENTAZION, blank=False, null=False, default='R')

    def __unicode__(self):
        return u"{}".format(smart_str(self.product_final))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _("Product")))
        fields.append(('public', _("Public")))
        fields.append(('view_video', _("View Video")))
        fields.append(('orientazion', _("Orientazion")))
        return fields

    def save(self, *args, **kwards):
        if self.public:
            if self.pk:
                FlagshipProduct.objects.exclude(pk=self.pk).update(public=False)
            else:
                FlagshipProduct.objects.all().update(public=False)
        return super(FlagshipProduct, self).save(*args, **kwards)

    @classmethod
    def get_flagship(cls, lang, apply_surcharge=False):
        flagship = cls.query_or(
            Q(public=True),
            "image",
            "view_video",
            "product_final__pk",
            "product_final__price",
            "product_final__product__tax__tax",
            "product_final__product__url_video",
            "product_final__{}__slug".format(lang),
            "orientazion",
            "{}__title".format(lang),
            "{}__description".format(lang),
            pk="product_final__pk",
            price="product_final__price",
            tax="product_final__product__tax__tax",
            slug="product_final__{}__slug".format(lang),
            title="{}__title".format(lang),
            description="{}__description".format(lang),
            pop_annotations=True
        ).first()

        if flagship:
            product_final = ProductFinal.objects.get(pk=flagship['pk'])
            prices = product_final.calculate_price(apply_surcharge)
            flagship['price'] = prices['price_total']

        return flagship


class ProductFinalOption(CodenerixModel):
    product_final = models.ForeignKey(ProductFinal, on_delete=models.CASCADE, related_name='productfinals_option', verbose_name=_("Product Final"))
    products_pack = models.ManyToManyField(ProductFinal, related_name='productfinals_optionpack', symmetrical=False, blank=False)
    active = models.BooleanField(_("Active"), blank=False, null=False, default=True)
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)

    def __unicode__(self):
        lang = get_language_database()
        return u"{}".format(smart_str(getattr(self, lang).name))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        lang = get_language_database()
        fields = []
        fields.append(('product_final', _("Product final")))
        fields.append(('{}__name'.format(lang), _("Option")))
        fields.append(('order', _("Order")))
        fields.append(('products_pack', _("Products options")))
        fields.append(('active', _("Active")))
        return fields


MODELS_SLUG = [
    ("family", "Family"),
    ("category", "Category"),
    ("subcategory", "Subcategory"),
    ("product_final_option", "ProductFinalOption"),
]

for info in MODELS_SLUG:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenTextSlug):\n".format(model, lang_code)
        query += "  {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)

MODELS = [
    ("feature", "Feature"),
    ("attribute", "Attribute"),
    ("feature_special", "FeatureSpecial"),
    ("product_image", "ProductImage"),        # para los alt y los titles de las imagenes
    ("product_final_image", "ProductFinalImage"),
    ("product_document", "ProductDocument"),  # para los titles de los enlaces
    ("option_value", "OptionValueFeature"),
    ("option_value", "OptionValueAttribute"),
    ("option_value", "OptionValueFeatureSpecial"),
]

for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenText):\n".format(model, lang_code)
        query += "  {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)


MODELS_PRODUCTS = [
    ('product', 'ProductText', 'Product'),
]

for info in MODELS_PRODUCTS:
    field = info[0]
    model_source = info[1]
    model_relate = info[2]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenProductText):\n".format(model_source, lang_code)
        query += "  {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model_relate, lang_code.lower())
        exec(query)

MODELS_BRANDS = [
    ('brand', 'Brand', 'Brand'),
]

for info in MODELS_BRANDS:
    field = info[0]
    model_source = info[1]
    model_relate = info[2]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenBrandText):\n".format(model_source, lang_code)
        query += "  {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model_relate, lang_code.lower())
        exec(query)

MODELS_PRODUCTS_FINAL = [
    ('product', 'ProductFinal', 'ProductFinal'),
]

for info in MODELS_PRODUCTS_FINAL:
    field = info[0]
    model_source = info[1]
    model_relate = info[2]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenProductFinalText):\n".format(model_source, lang_code)
        query += "  {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model_relate, lang_code.lower())
        exec(query)

MODELS_SLIDERS = [
    ('product', 'FlagshipProduct'),
]

for info in MODELS_SLIDERS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenTextTitle):\n".format(model, lang_code)
        query += "  {} = models.OneToOneField({}, on_delete=models.CASCADE, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)
