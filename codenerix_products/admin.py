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

from django.contrib import admin
from django.conf import settings

from .models import Feature, Attribute, FeatureSpecial, Family, Category, Subcategory, Product, ProductRelationSold, ProductImage, ProductDocument, ProductFinal, ProductFeature, ProductUnique, Brand
from .models import GroupValueFeature, GroupValueAttribute, GroupValueFeatureSpecial
from .models import OptionValueFeature, OptionValueAttribute, OptionValueFeatureSpecial
from .models import MODELS, MODELS_PRODUCTS, MODELS_SLUG, MODELS_SLIDERS

admin.site.register(Feature)
admin.site.register(Attribute)
admin.site.register(FeatureSpecial)
admin.site.register(Family)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(ProductRelationSold)
admin.site.register(ProductImage)
admin.site.register(ProductDocument)
admin.site.register(ProductFinal)
admin.site.register(ProductFeature)
admin.site.register(ProductUnique)
admin.site.register(Brand)
admin.site.register(GroupValueFeature)
admin.site.register(GroupValueAttribute)
admin.site.register(GroupValueFeatureSpecial)
admin.site.register(OptionValueFeature)
admin.site.register(OptionValueAttribute)
admin.site.register(OptionValueFeatureSpecial)


for info in MODELS + MODELS_PRODUCTS + MODELS_SLIDERS + MODELS_SLUG:
    model = info[1]
    for lang in settings.LANGUAGES:
        lang_code = lang[0]
        query = "from .models import {}Text{}\n".format(model, lang_code.upper())
        query += "admin.site.register({}Text{})\n".format(model, lang_code.upper())
        exec(query)
