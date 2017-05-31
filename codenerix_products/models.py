# -*- coding: utf-8 -*-
#
# django-codenerix-products
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
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

from operator import or_
from collections import Iterable
from functools import reduce

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Sum, F, Q
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from codenerix.fields import ImageAngularField
from codenerix.helpers import nameunify
from codenerix.lib.helpers import upload_path
from codenerix.models import CodenerixModel
from codenerix.fields import WysiwygAngularField
from codenerix_extensions.helpers import get_language_database
from codenerix_extensions.files.models import GenImageFile, GenDocumentFile, GenImageFileNull


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

    def __unicode__(self):
        return u"{}".format(smart_text(self.name))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('tax', _("Tax (%)")))
        return fields

    def lock_delete(self):
        if self.type_recargo_equivalencia.exists():
            return _("Cannot delete type tax model, relationship between type tax model and recargo equivalencia")
        elif self.products.exists():
            return _("Cannot delete type tax model, relationship between type tax model and products")
        else:
            return super(TypeTax, self).lock_delete()

    def save(self, *args, **kwargs):
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


class TypeRecargoEquivalencia(CodenerixModel):
    type_tax = models.ForeignKey(TypeTax, related_name='type_recargo_equivalencia', verbose_name=_("Tax"))
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False)
    recargo_equivalencia = models.FloatField(_("Recargo de equivalencia (%)"), validators=[MinValueValidator(0), MaxValueValidator(100)], blank=False, null=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.name))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        fields.append(('type_tax__name', _("Type Tax")))
        fields.append(('type_tax__tax', _("Value (%)")))
        fields.append(('recargo_equivalencia', _("Recargo de equivalencia (%)")))
        return fields

    def lock_delete(self):
        if self.products.exists():
            return _("Cannot delete recargo equivalencia model, relationship between recargo equivalencia model and products")
        else:
            return super(TypeRecargoEquivalencia, self).lock_delete()

    def save(self, *args, **kwargs):
        if self.pk:
            obj = TypeRecargoEquivalencia.objects.get(pk=self.pk)
            if obj.recargo_equivalencia != self.recargo_equivalencia:
                result = super(TypeRecargoEquivalencia, self).save(*args, **kwargs)
                for product in self.products.all():
                    for pf in product.products_final.all():
                        pf.recalculate()
            else:
                result = super(TypeRecargoEquivalencia, self).save(*args, **kwargs)
        else:
            result = super(TypeRecargoEquivalencia, self).save(*args, **kwargs)
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
    class Meta:
        abstract = True

    type_value = models.CharField(_("Type value"), max_length=2, choices=TYPE_VALUES, blank=False, null=False, default='F')
    price = models.FloatField(_("Price"), blank=False, null=False, default=0)
    type_price = models.CharField(_("Type price"), max_length=2, choices=TYPE_PRICES, blank=False, null=False, default=TYPE_PRICE_PERCENTAGE)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)

    def __fields__(self, info):
        fields = []
        fields.append(('family', _('Family')))
        fields.append(('category', _('Category')))
        fields.append(('type_value', _('Type Value')))
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
    class Meta:
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


# description del texto en diferentes idiomas
class GenTextSlug(CodenerixModel):  # META: Abstract class
    class Meta:
        abstract = True

    slug = models.CharField(_("Slug"), max_length=250, blank=False, null=False, unique=True)
    name = models.CharField(_("Name"), max_length=250, blank=False, null=False, unique=True)
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
    class Meta:
        abstract = True

    title = models.CharField(_("Text alternavive image"), max_length=250, blank=False, null=False)
    description = WysiwygAngularField(_("Description"), blank=True, null=True)


# texto de los product y productfinal
class GenProductText(CodenerixModel):  # META: Abstract class
    class Meta:
        abstract = True

    meta_title = models.CharField(_("Meta Title"), max_length=70, blank=True, null=True)
    meta_description = models.CharField(_("Meta Description"), max_length=70, blank=True, null=True)
    description_short = WysiwygAngularField(_("Description short"), blank=True, null=True)
    description_long = WysiwygAngularField(_("Description long"), blank=True, null=True)
    # url amigable
    slug = models.CharField(_("Slug"), max_length=250, blank=False, null=False, unique=True)
    name = models.CharField(_("Name"), max_length=250, blank=True, null=True)
    # faltan los campos para posicionamiento
    public = models.BooleanField(_("Public"), blank=True, null=False, default=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.description_short))

    def __str__(self):
        return self.__unicode__()

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
        return super(GenProductText, self).save(*args, **kwards)


# #####################################


# familias
class Family(CodenerixModel, GenImageFileNull):
    code = models.CharField(_("Code"), max_length=250, blank=True, null=True, unique=True)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    show_menu = models.BooleanField(_("Show menu"), blank=True, null=False, default=True)

    def __fields__(self, info):
        fields = []
        fields.append(('{}__name'.format(settings.LANGUAGES_DATABASES[0].lower()), _("Name")))
        fields.append(('code', _("Code")))
        fields.append(('public', _("Public")))
        fields.append(('show_menu', _("Show Menu")))
        return fields

    def __unicode__(self):
        return u"{} ({})".format(smart_text(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name), smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

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
    family = models.ForeignKey(Family, related_name='categories', verbose_name=_("Family"))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    show_menu = models.BooleanField(_("Show menu"), blank=True, null=False, default=True)
    show_only_product_stock = models.BooleanField(_("Show only products in stock"), blank=True, null=False, default=True)
    image = ImageAngularField(_("Image"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja un tamaño comprendido entre 1200px y 2000px'))
    icon = ImageAngularField(_("Icon"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja que sea una imagen superior a 200px transparente y en formato png o svg'))
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    
    def __unicode__(self):
        return u"{} ({})".format(smart_text(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name), smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

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
    category = models.ForeignKey(Category, related_name='subcategory', verbose_name=_("Category"))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    show_menu = models.BooleanField(_("Show menu"), blank=True, null=False, default=True)
    show_brand = models.BooleanField(_("Show brand (for menu)"), blank=True, null=False, default=True)
    outstanding = models.BooleanField(_("Outstanding"), blank=True, null=False, default=False)
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    image = ImageAngularField(_("Image"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja un tamaño comprendido entre 1200px y 2000px'))
    icon = ImageAngularField(_("Icon"), upload_to=upload_path, max_length=200, blank=True, null=True, help_text=_(u'Se aconseja que sea una imagen superior a 200px transparente y en formato png o svg'))

    def __unicode__(self):
        return u"{} ({})".format(smart_text(getattr(self, settings.LANGUAGES_DATABASES[0].lower()).name), smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

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
    class Meta:
        abstract = True

    name = models.CharField(_("Name"), max_length=250, blank=True, null=True, unique=True)

    def __fields__(self, info):
        fields = []
        fields.append(('name', _("Name")))
        return fields

    def __unicode__(self):
        return u"{}".format(smart_text(self.name))

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
    class Meta:
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
    group = models.ForeignKey(GroupValueFeature, related_name='options_value_feature', verbose_name=_("Options value"))


# opciones de los grupos de valores para attributes
class OptionValueAttribute(OptionValues):
    group = models.ForeignKey(GroupValueAttribute, related_name='options_value_attribute', verbose_name=_("Options value"))


# opciones de los grupos de valores features special
class OptionValueFeatureSpecial(OptionValues):
    group = models.ForeignKey(GroupValueFeatureSpecial, related_name='options_value_feature_special', verbose_name=_("Options value"))


# caracteristicas (comunes a todos los productos (resolución, RAM))
class Feature(GenAttr):
    family = models.ForeignKey(Family, related_name='features', verbose_name=_("Family"), blank=True, null=True)
    category = models.ForeignKey(Category, related_name='features', verbose_name=_("Category"), blank=True, null=True)
    list_value = models.ForeignKey(GroupValueFeature, related_name='features', verbose_name=_("List value"), blank=True, null=True)

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
    family = models.ForeignKey(Family, related_name='attributes', verbose_name=_("Family"), blank=True, null=True)
    category = models.ForeignKey(Category, related_name='attributes', verbose_name=_("Category"), blank=True, null=True)
    attribute = models.ForeignKey("self", related_name='attributes', verbose_name=_("Attribute"), blank=True, null=True)
    list_value = models.ForeignKey(GroupValueAttribute, related_name='attributes', verbose_name=_("List value"), blank=True, null=True)

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
    family = models.ForeignKey(Family, related_name='feature_specials', verbose_name=_("Family"), blank=True, null=True)
    category = models.ForeignKey(Category, related_name='feature_specials', verbose_name=_("Category"), blank=True, null=True)
    list_value = models.ForeignKey(GroupValueFeatureSpecial, related_name='feature_specials', verbose_name=_("List value"), blank=True, null=True)
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
                    name_res = u"{}".format(smart_text(translation.name))
                else:
                    name_res = u"{}".format(smart_text(translation.slug))
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
    class Meta:
        abstract = True

    model = models.CharField(_("Model"), max_length=250, blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='products', verbose_name=_("Brand"), blank=True, null=True)
    tax = models.ForeignKey(TypeTax, related_name='products', verbose_name=_("Tax (%)"), null=True)
    recargo_equivalencia = models.ForeignKey(TypeRecargoEquivalencia, related_name='products', verbose_name=_("Recargo Equivalencia (%)"), null=True, blank=True)
    family = models.ForeignKey(Family, related_name='products', verbose_name=_("Family"))
    category = models.ForeignKey(Category, related_name='products', verbose_name=_("Category"))
    subcategory = models.ForeignKey(Subcategory, related_name='products', verbose_name=_("Subcategory"))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    code = models.CharField(_("Code"), max_length=250, blank=False, null=False, unique=True)
    price_base = models.FloatField(_("Price base"), blank=False, null=False, default=0)
    # producto para la venta
    of_sales = models.BooleanField(_("Sales"), blank=True, null=False, default=True)
    # producto para la compra
    of_purchase = models.BooleanField(_("Purchase"), blank=True, null=False, default=True)
    # es necesario que el producto tenga stock para su venta
    force_stock = models.BooleanField(_("Force stock"), blank=True, null=False, default=True)
    url_video = models.CharField(_("Url Video"), max_length=250, blank=True, null=True)
    # indica si es necesario tener una caracteristica especial obligatoriamente
    feature_special = models.ForeignKey(FeatureSpecial, related_name='products', verbose_name=_("Feature special"), blank=True, null=True)
    packing_cost = models.FloatField(_("Packing cost"), blank=False, null=False, default=0)
    weight = models.FloatField(_("Weight"), blank=False, null=False, default=0)

    def __unicode__(self):
        return u"{}".format(smart_text(self.code))

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
        fields.append(('recargo_equivalencia', _("Recargo Equivalencia")))
        fields.append(('code', _("Code")))
        fields.append(('price_base', _("Price base")))
        fields.append(('of_sales', _("Sales")))
        fields.append(('of_purchase', _("Pruchase")))
        fields.append(('force_stock', _("Force stock")))
        fields.append(('url_video', _("Url Video")))
        fields.append(('feature_special', _("Feature special")))
        fields.append(('packing_cost', _("Packing cost")))
        fields.append(('weight', _("Weight")))

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
class Product(GenProduct):

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
            if obj.price_base != self.price_base or obj.tax != self.tax or obj.recargo_equivalencia != self.recargo_equivalencia:
                result = super(Product, self).save(*args, **kwargs)
                for pf in self.products_final.all():
                    pf.recalculate()
            else:
                result = super(Product, self).save(*args, **kwargs)
        else:
            result = super(Product, self).save(*args, **kwargs)
        return result


# productos relacionados mas vendidos
class ProductRelationSold(CodenerixModel):
    product = models.ForeignKey(Product, blank=False, null=False, related_name='products_related', verbose_name=_("Product"))
    related = models.ForeignKey(Product, blank=False, null=False, related_name='products_related_sold', verbose_name=_("Products related"))
    hits = models.SmallIntegerField(_("Hits"), blank=True, null=True)

    class Meta:
        unique_together = (('product', 'related'), )

    def __unicode__(self):
        return u"{} ({})".format(smart_text(self.product), smart_text(self.hits))

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
    product = models.ForeignKey(Product, related_name='products_image', verbose_name=_("Product"))
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    principal = models.BooleanField(_("Principal"), blank=False, null=False, default=False)
    flagship_product = models.BooleanField(_("Flagship product"), default=False)
    outstanding = models.BooleanField(_("Outstanding"), default=False)

    def __unicode__(self):
        return u"{} ({})".format(smart_text(self.product), smart_text(self.order))

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
    product = models.ForeignKey(Product, related_name='products_document', verbose_name=_("Product"))
    public = models.BooleanField(_("Public"), blank=False, null=False, default=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.product))

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
    product = models.ForeignKey(Product, blank=False, null=False, related_name='products_final', verbose_name=_('Product'))
    # productos relacionados
    related = models.ManyToManyField("ProductFinal", blank=True, related_name='productsrelated', symmetrical=False)
    related_accesory = models.ManyToManyField("ProductFinal", blank=True, related_name='productsrelatedaccesory', symmetrical=False)
    offer = models.BooleanField(_("Offer"), blank=True, null=False, default=False)
    outstanding = models.BooleanField(_("Outstanding"), blank=True, null=False, default=False)
    most_sold = models.BooleanField(_("Most sold"), blank=True, null=False, default=False)
    stock_real = models.FloatField(_("Stock real"), null=False, blank=False, default=0, editable=False)
    stock_lock = models.FloatField(_("Stock lock"), null=False, blank=False, default=0, editable=False)
    price = models.FloatField(_("Price"), null=False, blank=False, default=0, editable=False)
    ean13 = models.CharField(_("EAN-13"), null=True, blank=True, max_length=13)

    reviews_value = models.FloatField(_("Reviews"), null=False, blank=False, default=0, editable=False)
    reviews_count = models.IntegerField(_("Reviews count"), null=False, blank=False, default=0, editable=False)

    def __unicode__(self):
        name = u"{} - {} ({})".format(self.pk, smart_text(self.product), self.ean13)
        return name

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        lang = get_language_database()
        fields = []
        fields.append(('pk', _("Identifier")))
        fields.append(('{}__name'.format(lang), _("Product")))
        fields.append(('product__family__{}__name'.format(lang), _("Family")))
        fields.append(('product__category__{}__name'.format(lang), _("Category")))
        fields.append(('product__subcategory__{}__name'.format(lang), _("Subcategory")))
        fields.append(('{}__public'.format(lang), _("Public")))
        fields.append(('stock_real', _("Stock real")))
        fields.append(('stock_lock', _("Stock lock")))
        fields.append(('price', _("Price")))
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

    def save(self, *args, **kwards):
        self.recalculate(commit=False)
        return super(ProductFinal, self).save(*args, **kwards)

    def recalculate(self, commit=True):
        newprice = self.calculate_price()['price_total']
        if self.price != newprice:
            self.price = newprice
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

    def calculate_price(self, apply_overcharge=False):
        price = float(self.product.price_base)
        tax = float(self.product.tax.tax)
        if self.product.recargo_equivalencia:
            overcharge = float(self.product.recargo_equivalencia.recargo_equivalencia)
        else:
            overcharge = 0

        # atributos
        update = True
        for attr in self.products_final_attr.all().order_by('-updated'):
            if update:
                if attr.attribute.type_price == TYPE_PRICE_FINAL:
                    price = float(attr.attribute.price)
                    update = False
                elif attr.attribute.type_price == TYPE_PRICE_INCREASE:
                    price += float(attr.attribute.price)
                elif attr.attribute.type_price == TYPE_PRICE_PERCENTAGE:
                    price += (float(self.product.price_base) * float(attr.attribute.price) / 100)

        # caracteristicas
        if update:
            for feature in self.product.product_features.all().order_by('-updated'):
                if update:
                    if feature.feature.type_price == TYPE_PRICE_FINAL:
                        price = float(feature.feature.price)
                        update = False
                    elif feature.feature.type_price == TYPE_PRICE_INCREASE:
                        price += float(feature.feature.price)
                    elif feature.feature.type_price == TYPE_PRICE_PERCENTAGE:
                        price += (float(self.product.price_base) * float(feature.feature.price) / 100)

        # caracteristicas especiales
        if update and self.product.feature_special:
            if self.product.feature_special.type_price == TYPE_PRICE_FINAL:
                price = float(self.product.feature_special.price)
            elif self.product.feature_special.type_price == TYPE_PRICE_INCREASE:
                price += float(self.product.feature_special.price)
            elif self.product.feature_special.type_price == TYPE_PRICE_PERCENTAGE:
                price += float(self.product.price_base) * float(self.product.feature_special.price) / 100

        result = {'overcharge': 0}
        result['price_base'] = float(price)
        result['tax'] = (float(price) * float(tax)) / 100.0
        if apply_overcharge:
            result['overcharge'] = (float(price) * float(overcharge)) / 100.0
        result['price_total'] = float(price) + float(result['tax']) + float(result['overcharge'])
        return result

    @classmethod
    def get_recommended_products(cls, lang, apply_overcharge=False, category=None, subcategory=None):
        products = []
        query = Q(most_sold=True) | Q(product__products_image__principal=True)
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
    def get_outstanding_products(cls, lang, apply_overcharge=False, category=None, subcategory=None):
        products = []
        query = Q(outstanding=True) | Q(product__products_image__principal=True)
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
        )[:16]:
            prices = cls.objects.get(pk=product['pk']).calculate_price(apply_overcharge)
            product['price'] = prices['price_total']
            product['new'] = 1 if (timezone.now() - product['created']).days <= settings.CDNX_PRODUCTS_NOVELTY_DAYS else 0
            products.append(product)

        return products

    @classmethod
    def get_products(cls, lang, apply_overcharge=False, family=None, category=None, subcategory=None, brand=None):
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
            "product__model",
            "product__brand__{}__name".format(lang),
            "product__products_image__image",
            "{}__meta_title".format(lang),
            slug="{}__slug".format(lang),
            meta_title="{}__meta_title".format(lang),
            image="product__products_image__image",
            pop_annotations=True
        ):
            prices = cls.objects.get(pk=product['pk']).calculate_price(apply_overcharge)
            product['price'] = prices['price_total']
            product['new'] = 1 if (timezone.now() - product['created']).days <= settings.CDNX_PRODUCTS_NOVELTY_DAYS else 0
            products.append(product)

        return products

    @classmethod
    def find_product(cls, query, lang, apply_overcharge=False):
        product = cls.query_or(
            query,
            "pk",
            "offer",
            "outstanding",
            "price",
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
            "{}__meta_title".format(lang),
            "{}__meta_description".format(lang),
            "{}__description_short".format(lang),
            "{}__description_long".format(lang),
            "{}__slug".format(lang),
            "{}__name".format(lang),
            "product__{}__meta_title".format(lang),
            "product__{}__meta_description".format(lang),
            "product__{}__description_short".format(lang),
            "product__{}__description_long".format(lang),
            family_name="product__family__{}__name".format(lang),
            family_slug="product__family__{}__slug".format(lang),
            family_description="product__family__{}__description".format(lang),
            category_slug="product__category__{}__slug".format(lang),
            category_name="product__category__{}__name".format(lang),
            category_description="product__category__{}__description".format(lang),
            subcategory_slug="product__subcategory__{}__slug".format(lang),
            subcategory_name="product__subcategory__{}__name".format(lang),
            subcategory_description="product__subcategory__{}__description".format(lang),
            tax="product__tax__tax",
            meta_title="{}__meta_title".format(lang),
            meta_description="{}__meta_description".format(lang),
            description_short="{}__description_short".format(lang),
            description_long="{}__description_long".format(lang),
            name="{}__name".format(lang),
            slug="{}__slug".format(lang),
            product_meta_title="product__{}__meta_title".format(lang),
            product_meta_description="product__{}__meta_description".format(lang),
            product_description_short="product__{}__description_short".format(lang),
            product_description_long="product__{}__description_long".format(lang),
            stars="reviews_value",
            pop_annotations=True
        ).first()

        if product:
            product_final = cls.objects.get(pk=product['pk'])
            prices = product_final.calculate_price(apply_overcharge)
            product['price'] = prices['price_total']

        return product


# imagenes de productos
class ProductFinalImage(CodenerixModel, GenImageFile):
    product_final = models.ForeignKey(ProductFinal, related_name='productfinals_image', verbose_name=_("Product Final"))
    order = models.SmallIntegerField(_("Order"), blank=True, null=True)
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    principal = models.BooleanField(_("Principal"), blank=False, null=False, default=False)
    flagship_product = models.BooleanField(_("Flagship product"), default=False)
    outstanding = models.BooleanField(_("Outstanding"), default=False)

    def __unicode__(self):
        return u"{} ({})".format(smart_text(self.product_final), smart_text(self.order))

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
    product = models.ForeignKey(ProductFinal, blank=False, null=False, related_name='products_final_attr', verbose_name=_('Product'))
    attribute = models.ForeignKey(Attribute, blank=False, null=True, related_name='products_final_attr', verbose_name=_('Attributes'))

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
            return u"{}: {}".format(smart_text(self.attribute), smart_text(value))
        else:
            return u"{}".format(smart_text(value))

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


# valor de las caracteristicas del producto (talla, color)
class ProductFeature(CodenerixModel):
    product = models.ForeignKey(Product, blank=False, null=False, verbose_name=_('Product'), related_name='product_features')
    feature = models.ForeignKey(Feature, blank=False, null=False, verbose_name=_('Feature'), related_name='product_features')
    value = models.CharField(_("Value"), max_length=80)

    def __unicode__(self):
        return u"{}".format(smart_text(self.product))

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
    product_final = models.ForeignKey(ProductFinal, blank=False, null=False, related_name='products_unique', verbose_name=_('Product final'))
    value = models.CharField(_("Value"), max_length=80, null=True, blank=True)
    stock_real = models.FloatField(_("Stock real"), null=False, blank=False, default=0)

    class Meta:
        unique_together = ('product_final', 'value')

    def __unicode__(self):
        return u"{}".format(smart_text(self.product_final))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        fields = []
        fields.append(('product_final', _("Product")))
        fields.append(('product_final__product__feature_special', _("Feature special")))
        fields.append(('value', _("Value")))
        fields.append(('stock_real', _("Stock real")))
        return fields

    def save(self, *args, **kwargs):
        product_final = ProductFinal.objects.filter(pk=self.product_final_id).first()
        # se comprueba que no se repite el valor de las caracteristicas especiales de los productos finales cuando sean unicas
        if product_final:
            if product_final.product.feature_special and product_final.product.feature_special.unique:
                if ProductUnique.objects.filter(
                    value=self.value,
                    product_final__product=product_final.product
                ).exists():
                    raise ValidationError(_('Ya existe un producto final con el valor de la caracteristicas especial'))
        else:
            raise ValidationError(_("Product don't seleted"))

        # save and update stock of product final
        with transaction.atomic():
            r = super(ProductUnique, self).save(*args, **kwargs)
            product_final.stock_real = ProductUnique.objects.filter(product_final=product_final).aggregate(stock=Sum('stock_real'))['stock']
            product_final.save()
            return r


# producto estrella (solo un registro publico)
class FlagshipProduct(CustomQueryMixin, CodenerixModel, GenImageFile):
    product_final = models.ForeignKey(ProductFinal, blank=False, null=False, related_name='flagship_products', verbose_name=_('Flagship product'))
    public = models.BooleanField(_("Public"), blank=True, null=False, default=True)
    view_video = models.BooleanField(_("View video"), blank=True, null=False, default=False)
    orientazion = models.CharField(_("Orientazion"), max_length=2, choices=TYPE_ORIENTAZION, blank=False, null=False, default='R')

    def __unicode__(self):
        return u"{}".format(smart_text(self.product_final))

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


MODELS_SLUG = [
    ("family", "Family"),
    ("category", "Category"),
    ("subcategory", "Subcategory"),
]

for info in MODELS_SLUG:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenTextSlug):\n".format(model, lang_code)
        query += "  {} = models.OneToOneField({}, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
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
        query += "  {} = models.OneToOneField({}, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)


MODELS_PRODUCTS = [
    ('product', 'ProductText', 'Product'),
    ('product', 'ProductFinal', 'ProductFinal'),
    ('brand', 'Brand', 'Brand'),
]

for info in MODELS_PRODUCTS:
    field = info[0]
    model_source = info[1]
    model_relate = info[2]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenProductText):\n".format(model_source, lang_code)
        query += "  {} = models.OneToOneField({}, blank=False, null=False, related_name='{}')\n".format(field, model_relate, lang_code.lower())
        exec(query)

MODELS_SLIDERS = [
    ('product', 'FlagshipProduct'),
]

for info in MODELS_SLIDERS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}Text{}(GenTextTitle):\n".format(model, lang_code)
        query += "  {} = models.OneToOneField({}, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)
