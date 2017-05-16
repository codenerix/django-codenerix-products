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

from django.conf.urls import url
from .views import FeatureList, AttributeList, FeatureSpecialList, FamilyList, CategoryList, SubcategoryList, ProductList, ProductRelationSoldList, ProductImageList, ProductDocumentList, ProductFinalList, ProductFeatureList, ProductUniqueList, \
    FeatureCreate, AttributeCreate, FeatureSpecialCreate, FamilyCreate, CategoryCreate, SubcategoryCreate, ProductCreate, ProductRelationSoldCreate, ProductFinalCreate, \
    FeatureCreateModal, AttributeCreateModal, FeatureSpecialCreateModal, FamilyCreateModal, CategoryCreateModal, SubcategoryCreateModal, SubcategoryCreateModalAll, ProductCreateModal, ProductRelationSoldCreateModal, ProductImageCreateModal, ProductDocumentCreateModal, ProductFinalCreateModal, ProductFeatureCreateModal, ProductUniqueCreateModal, \
    FeatureUpdate, AttributeUpdate, FeatureSpecialUpdate, FamilyUpdate, CategoryUpdate, SubcategoryUpdate, ProductUpdate, ProductRelationSoldUpdate, ProductImageUpdate, ProductDocumentUpdate, ProductFinalUpdate, ProductFeatureUpdate, ProductUniqueUpdate, \
    FeatureUpdateModal, AttributeUpdateModal, FeatureSpecialUpdateModal, FamilyUpdateModal, CategoryUpdateModal, SubcategoryUpdateModal, ProductUpdateModal, ProductRelationSoldUpdateModal, ProductImageUpdateModal, ProductDocumentUpdateModal, ProductFinalUpdateModal, ProductFeatureUpdateModal, ProductUniqueUpdateModal, \
    FeatureDelete, AttributeDelete, FeatureSpecialDelete, FamilyDelete, CategoryDelete, SubcategoryDelete, ProductDelete, ProductRelationSoldDelete, ProductImageDelete, ProductDocumentDelete, ProductFinalDelete, ProductFeatureDelete, ProductUniqueDelete, \
    ProductDetails, ProductFeatureSubList, ProductFeatureDetailsModal, \
    ProductDocumentSubList, ProductDocumentDetailsModal, \
    ProductFinalDetails, CategoryDetails, \
    ProductFinalImageList, ProductFinalImageCreate, ProductFinalImageCreateModal, ProductFinalImageUpdate, ProductFinalImageUpdateModal, ProductFinalImageDelete, ProductFinalImageSubList, ProductFinalImageDetails, ProductFinalImageDetailsModal, \
    ProductFinalAttributeList, ProductFinalAttributeSubList, ProductFinalAttributeCreateModal, ProductFinalAttributeDetailsModal, ProductFinalAttributeUpdateModal, ProductFinalAttributeDelete, \
    ProductImageSubList, ProductImageDetailsModal, \
    ProductUniqueSubList, ProductUniqueDetailsModal, \
    CategoryForeign, SubcategoryForeign, FeatureForeign, \
    ProductFinalRelatedSubList, ProductFinalRelatedSubUpdateModal, ProductFinalRelatedSubDelete, \
    ProductFinalAccesorySubList, ProductFinalAccesorySubUpdateModal, ProductFinalAccesorySubDelete, \
    ProductForeign, \
    AttributeForeign, FeatureSpecialForeign, \
    TypeTaxList, TypeTaxCreate, TypeTaxCreateModal, TypeTaxUpdate, TypeTaxUpdateModal, TypeTaxDelete, \
    SubcategorySubList, SubcategoryDetailModal, \
    TypeRecargoEquivalenciaList, TypeRecargoEquivalenciaCreate, TypeRecargoEquivalenciaCreateModal, TypeRecargoEquivalenciaUpdate, TypeRecargoEquivalenciaUpdateModal, TypeRecargoEquivalenciaDelete, \
    ProductFinalForeignSales, ProductFinalForeignPurchases,  \
    BrandList, BrandCreate, BrandCreateModal, BrandUpdate, BrandUpdateModal, BrandDelete, \
    FlagshipProductList, FlagshipProductCreate, FlagshipProductCreateModal, FlagshipProductUpdate, FlagshipProductUpdateModal, FlagshipProductDelete, \
    CategorySubListPro, CategoryDetailModalPro, CategoryUpdateModalPro, \
    ListProducts, TypeTaxDetails, \
    ProductFinalSubList, ProductFinalDetailsModal, \
    GroupValueFeatureList, GroupValueFeatureCreate, GroupValueFeatureCreateModal, GroupValueFeatureDetails, GroupValueFeatureUpdate, GroupValueFeatureUpdateModal, GroupValueFeatureDelete, \
    GroupValueAttributeList, GroupValueAttributeCreate, GroupValueAttributeCreateModal, GroupValueAttributeDetails, GroupValueAttributeUpdate, GroupValueAttributeUpdateModal, GroupValueAttributeDelete, \
    GroupValueFeatureSpecialList, GroupValueFeatureSpecialCreate, GroupValueFeatureSpecialCreateModal, GroupValueFeatureSpecialDetails, GroupValueFeatureSpecialUpdate, GroupValueFeatureSpecialUpdateModal, GroupValueFeatureSpecialDelete, \
    OptionValueFeatureList, OptionValueFeatureUpdate, OptionValueFeatureUpdateModal, OptionValueFeatureDelete, OptionValueFeatureSubList, OptionValueFeatureSubListModal, OptionValueFeatureCreateModal, OptionValueFeatureDetailsModal, OptionValueFeatureForeign, \
    OptionValueAttributeList, OptionValueAttributeUpdate, OptionValueAttributeUpdateModal, OptionValueAttributeDelete, OptionValueAttributeSubList, OptionValueAttributeSubListModal, OptionValueAttributeCreateModal, OptionValueAttributeDetailsModal, OptionValueAttributeForeign, \
    OptionValueFeatureSpecialList, OptionValueFeatureSpecialUpdate, OptionValueFeatureSpecialUpdateModal, OptionValueFeatureSpecialDelete, OptionValueFeatureSpecialSubList, OptionValueFeatureSpecialSubListModal, OptionValueFeatureSpecialCreateModal, OptionValueFeatureSpecialDetailsModal, OptionValueFeatureSpecialForeign


urlpatterns = [
    url(r'^typetaxs$', TypeTaxList.as_view(), name='CDNX_products_typetaxs_list'),
    url(r'^typetaxs/add$', TypeTaxCreate.as_view(), name='CDNX_products_typetaxs_add'),
    url(r'^typetaxs/addmodal$', TypeTaxCreateModal.as_view(), name='CDNX_products_typetaxs_addmodal'),
    url(r'^typetaxs/(?P<pk>\w+)$', TypeTaxDetails.as_view(), name='CDNX_products_categorys_details'),
    url(r'^typetaxs/(?P<pk>\w+)/edit$', TypeTaxUpdate.as_view(), name='CDNX_products_typetaxs_edit'),
    url(r'^typetaxs/(?P<pk>\w+)/editmodal$', TypeTaxUpdateModal.as_view(), name='CDNX_products_typetaxs_editmodal'),
    url(r'^typetaxs/(?P<pk>\w+)/delete$', TypeTaxDelete.as_view(), name='CDNX_products_typetaxs_delete'),

    url(r'^typerecargoequivalencias$', TypeRecargoEquivalenciaList.as_view(), name='CDNX_products_typerecargoequivalencias_list'),
    url(r'^typerecargoequivalencias/add$', TypeRecargoEquivalenciaCreate.as_view(), name='CDNX_products_typerecargoequivalencias_add'),
    url(r'^typerecargoequivalencias/addmodal$', TypeRecargoEquivalenciaCreateModal.as_view(), name='CDNX_products_typerecargoequivalencias_addmodal'),
    url(r'^typerecargoequivalencias/(?P<pk>\w+)/edit$', TypeRecargoEquivalenciaUpdate.as_view(), name='CDNX_products_typerecargoequivalencias_edit'),
    url(r'^typerecargoequivalencias/(?P<pk>\w+)/editmodal$', TypeRecargoEquivalenciaUpdateModal.as_view(), name='CDNX_products_typerecargoequivalencias_editmodal'),
    url(r'^typerecargoequivalencias/(?P<pk>\w+)/delete$', TypeRecargoEquivalenciaDelete.as_view(), name='CDNX_products_typerecargoequivalencias_delete'),

    url(r'^features$', FeatureList.as_view(), name='CDNX_products_features_list'),
    url(r'^features/add$', FeatureCreate.as_view(), name='CDNX_products_features_add'),
    url(r'^features/addmodal$', FeatureCreateModal.as_view(), name='CDNX_products_features_addmodal'),
    url(r'^features/(?P<pk>\w+)/edit$', FeatureUpdate.as_view(), name='CDNX_products_features_edit'),
    url(r'^features/(?P<pk>\w+)/editmodal$', FeatureUpdateModal.as_view(), name='CDNX_products_features_editmodal'),
    url(r'^features/(?P<pk>\w+)/delete$', FeatureDelete.as_view(), name='CDNX_products_features_delete'),
    url(r'^features/foreign/(?P<search>[\w\W]+|\*)$', FeatureForeign.as_view(), name='CDNX_products_features_foreign'),

    url(r'^attributes$', AttributeList.as_view(), name='CDNX_products_attributes_list'),
    url(r'^attributes/add$', AttributeCreate.as_view(), name='CDNX_products_attributes_add'),
    url(r'^attributes/addmodal$', AttributeCreateModal.as_view(), name='CDNX_products_attributes_addmodal'),
    url(r'^attributes/(?P<pk>\w+)/edit$', AttributeUpdate.as_view(), name='CDNX_products_attributes_edit'),
    url(r'^attributes/(?P<pk>\w+)/editmodal$', AttributeUpdateModal.as_view(), name='CDNX_products_attributes_editmodal'),
    url(r'^attributes/(?P<pk>\w+)/delete$', AttributeDelete.as_view(), name='CDNX_products_attributes_delete'),
    url(r'^attributes/foreign/(?P<search>[\w\W]+|\*)$', AttributeForeign.as_view(), name='CDNX_products_attributes_foreign'),

    url(r'^featurespecials$', FeatureSpecialList.as_view(), name='CDNX_products_featurespecials_list'),
    url(r'^featurespecials/add$', FeatureSpecialCreate.as_view(), name='CDNX_products_featurespecials_add'),
    url(r'^featurespecials/addmodal$', FeatureSpecialCreateModal.as_view(), name='CDNX_products_featurespecials_addmodal'),
    url(r'^featurespecials/(?P<pk>\w+)/edit$', FeatureSpecialUpdate.as_view(), name='CDNX_products_featurespecials_edit'),
    url(r'^featurespecials/(?P<pk>\w+)/editmodal$', FeatureSpecialUpdateModal.as_view(), name='CDNX_products_featurespecials_editmodal'),
    url(r'^featurespecials/(?P<pk>\w+)/delete$', FeatureSpecialDelete.as_view(), name='CDNX_products_featurespecials_delete'),
    url(r'^featurespecials/foreign/(?P<search>[\w\W]+|\*)$', FeatureSpecialForeign.as_view(), name='CDNX_products_featurespecials_foreign'),

    url(r'^familys$', FamilyList.as_view(), name='CDNX_products_familys_list'),
    url(r'^familys/add$', FamilyCreate.as_view(), name='CDNX_products_familys_add'),
    url(r'^familys/addmodal$', FamilyCreateModal.as_view(), name='CDNX_products_familys_addmodal'),
    url(r'^familys/(?P<pk>\w+)/edit$', FamilyUpdate.as_view(), name='CDNX_products_familys_edit'),
    url(r'^familys/(?P<pk>\w+)/editmodal$', FamilyUpdateModal.as_view(), name='CDNX_products_familys_editmodal'),
    url(r'^familys/(?P<pk>\w+)/delete$', FamilyDelete.as_view(), name='CDNX_products_familys_delete'),

    url(r'^brands$', BrandList.as_view(), name='CDNX_products_brand_list'),
    url(r'^brands/add$', BrandCreate.as_view(), name='CDNX_products_brand_add'),
    url(r'^brands/addmodal$', BrandCreateModal.as_view(), name='CDNX_products_brand_addmodal'),
    url(r'^brands/(?P<pk>\w+)/edit$', BrandUpdate.as_view(), name='CDNX_products_brand_edit'),
    url(r'^brands/(?P<pk>\w+)/editmodal$', BrandUpdateModal.as_view(), name='CDNX_products_brand_editmodal'),
    url(r'^brands/(?P<pk>\w+)/delete$', BrandDelete.as_view(), name='CDNX_products_brand_delete'),

    url(r'^categorys$', CategoryList.as_view(), name='CDNX_products_categorys_list'),
    url(r'^categorys/add$', CategoryCreate.as_view(), name='CDNX_products_categorys_add'),
    url(r'^categorys/addmodal$', CategoryCreateModal.as_view(), name='CDNX_products_categorys_addmodal'),
    url(r'^categorys/(?P<pk>\w+)$', CategoryDetails.as_view(), name='CDNX_products_categorys_details'),
    url(r'^categorys/(?P<pk>\w+)/edit$', CategoryUpdate.as_view(), name='CDNX_products_categorys_edit'),
    url(r'^categorys/(?P<pk>\w+)/editmodal$', CategoryUpdateModal.as_view(), name='CDNX_products_categorys_editmodal'),
    url(r'^categorys/(?P<pk>\w+)/delete$', CategoryDelete.as_view(), name='CDNX_products_categorys_delete'),
    url(r'^categorys/foreign/(?P<search>[\w\W]+|\*)$', CategoryForeign.as_view(), name='CDNX_products_categorys_foreign'),

    url(r'^categorys/(?P<pk>\w+)/sublistpro$', CategorySubListPro.as_view(), name='CDNX_products_categoryrelateds_sublist'),
    url(r'^categorys/(?P<cpk>\w+)/sublistpro/(?P<pk>\w+)$', CategoryDetailModalPro.as_view(), name='CDNX_products_category_sublist_details'),
    url(r'^categorys/(?P<cpk>\w+)/sublistpro/(?P<pk>\w+)/edit$', CategoryUpdateModalPro.as_view(), name='CDNX_products_category_sublist_edit'),
    url(r'^categorys/(?P<cpk>\w+)/sublistpro/(?P<pk>\w+)/editmodal$', CategoryUpdateModalPro.as_view(), name='CDNX_products_category_sublist_editmodal'),
    url(r'^categorys/(?P<cpk>\w+)/sublistpro/(?P<pk>\w+)/delete$', CategoryDelete.as_view(), name='CDNX_products_category_sublist_delete'),

    url(r'^subcategorys$', SubcategoryList.as_view(), name='CDNX_products_subcategorys_list'),
    url(r'^subcategorys/add$', SubcategoryCreate.as_view(), name='CDNX_products_subcategorys_add'),
    url(r'^subcategorys/addmodal$', SubcategoryCreateModalAll.as_view(), name='CDNX_products_subcategorys_addmodal'),
    url(r'^subcategorys/(?P<pk>\w+)/edit$', SubcategoryUpdate.as_view(), name='CDNX_products_subcategorys_edit'),
    url(r'^subcategorys/(?P<pk>\w+)/editmodal$', SubcategoryUpdateModal.as_view(), name='CDNX_products_subcategorys_editmodal'),
    url(r'^subcategorys/(?P<pk>\w+)/delete$', SubcategoryDelete.as_view(), name='CDNX_products_subcategorys_delete'),
    url(r'^subcategorys/foreign/(?P<search>[\w\W]+|\*)$', SubcategoryForeign.as_view(), name='CDNX_products_subcategorys_foreign'),

    url(r'^subcategorys/(?P<pk>\w+)/sublist$', SubcategorySubList.as_view(), name='CDNX_products_subcategory_sublist'),
    url(r'^subcategorys/(?P<cpk>\w+)/sublist/add$', SubcategoryCreateModal.as_view(), name='CDNX_products_subcategory_sublist_add'),
    url(r'^subcategorys/(?P<cpk>\w+)/sublist/addmodal$', SubcategoryCreateModal.as_view(), name='CDNX_products_subcategory_sublist_addmodal'),
    url(r'^subcategorys/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', SubcategoryDetailModal.as_view(), name='CDNX_products_subcategory_sublist_details'),
    url(r'^subcategorys/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', SubcategoryUpdateModal.as_view(), name='CDNX_products_subcategory_sublist_edit'),
    url(r'^subcategorys/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', SubcategoryUpdateModal.as_view(), name='CDNX_products_subcategory_sublist_editmodal'),
    url(r'^subcategorys/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', SubcategoryDelete.as_view(), name='CDNX_products_subcategory_sublist_delete'),

    url(r'^products$', ProductList.as_view(), name='CDNX_products_products_list'),
    url(r'^products/add$', ProductCreate.as_view(), name='CDNX_products_products_add'),
    url(r'^products/addmodal$', ProductCreateModal.as_view(), name='CDNX_products_products_addmodal'),
    url(r'^products/(?P<pk>\w+)$', ProductDetails.as_view(), name='CDNX_products_products_details'),
    url(r'^products/(?P<pk>\w+)/edit$', ProductUpdate.as_view(), name='CDNX_products_products_edit'),
    url(r'^products/(?P<pk>\w+)/editmodal$', ProductUpdateModal.as_view(), name='CDNX_products_products_editmodal'),
    url(r'^products/(?P<pk>\w+)/delete$', ProductDelete.as_view(), name='CDNX_products_products_delete'),
    url(r'^products/foreign/(?P<search>[\w\W]+|\*)$', ProductForeign.as_view(), name='CDNX_products_products_foreign'),

    url(r'^productrelationsolds$', ProductRelationSoldList.as_view(), name='CDNX_products_productrelationsolds_list'),
    url(r'^productrelationsolds/add$', ProductRelationSoldCreate.as_view(), name='CDNX_products_productrelationsolds_add'),
    url(r'^productrelationsolds/addmodal$', ProductRelationSoldCreateModal.as_view(), name='CDNX_products_productrelationsolds_addmodal'),
    url(r'^productrelationsolds/(?P<pk>\w+)/edit$', ProductRelationSoldUpdate.as_view(), name='CDNX_products_productrelationsolds_edit'),
    url(r'^productrelationsolds/(?P<pk>\w+)/editmodal$', ProductRelationSoldUpdateModal.as_view(), name='CDNX_products_productrelationsolds_editmodal'),
    url(r'^productrelationsolds/(?P<pk>\w+)/delete$', ProductRelationSoldDelete.as_view(), name='CDNX_products_productrelationsolds_delete'),

    url(r'^productimages$', ProductImageList.as_view(), name='CDNX_products_productimages_list'),
    url(r'^productimages/(?P<pk>\w+)/edit$', ProductImageUpdate.as_view(), name='CDNX_products_productimages_edit'),
    url(r'^productimages/(?P<pk>\w+)/editmodal$', ProductImageUpdateModal.as_view(), name='CDNX_products_productimages_editmodal'),
    url(r'^productimages/(?P<pk>\w+)/delete$', ProductImageDelete.as_view(), name='CDNX_products_productimages_delete'),
    url(r'^productimages/(?P<pk>\w+)/sublist$', ProductImageSubList.as_view(), name='CDNX_products_productimages_sublist'),
    url(r'^productimages/(?P<cpk>\w+)/sublist/add$', ProductImageCreateModal.as_view(), name='CDNX_products_productimages_sublist_add'),
    url(r'^productimages/(?P<cpk>\w+)/sublist/addmodal$', ProductImageCreateModal.as_view(), name='CDNX_products_productimages_sublist_addmodal'),
    url(r'^productimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductImageDetailsModal.as_view(), name='CDNX_products_productimages_sublist_details'),
    url(r'^productimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductImageUpdateModal.as_view(), name='CDNX_products_productimages_sublist_edit'),
    url(r'^productimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ProductImageUpdateModal.as_view(), name='CDNX_products_productimages_sublist_editmodal'),
    url(r'^productimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductImageDelete.as_view(), name='CDNX_products_productimages_sublist_delete'),

    url(r'^productdocuments$', ProductDocumentList.as_view(), name='CDNX_products_productdocuments_list'),
    url(r'^productdocuments/(?P<pk>\w+)/edit$', ProductDocumentUpdate.as_view(), name='CDNX_products_productdocuments_edit'),
    url(r'^productdocuments/(?P<pk>\w+)/editmodal$', ProductDocumentUpdateModal.as_view(), name='CDNX_products_productdocuments_editmodal'),
    url(r'^productdocuments/(?P<pk>\w+)/delete$', ProductDocumentDelete.as_view(), name='CDNX_products_productdocuments_delete'),
    url(r'^productdocuments/(?P<pk>\w+)/sublist$', ProductDocumentSubList.as_view(), name='CDNX_products_productdocuments_sublist'),
    url(r'^productdocuments/(?P<cpk>\w+)/sublist/add$', ProductDocumentCreateModal.as_view(), name='CDNX_products_productdocuments_sublist_add'),
    url(r'^productdocuments/(?P<cpk>\w+)/sublist/addmodal$', ProductDocumentCreateModal.as_view(), name='CDNX_products_productdocuments_sublist_addmodal'),
    url(r'^productdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductDocumentDetailsModal.as_view(), name='CDNX_products_productdocuments_sublist_details'),
    url(r'^productdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductDocumentUpdateModal.as_view(), name='CDNX_products_productdocuments_sublist_edit'),
    url(r'^productdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ProductDocumentUpdateModal.as_view(), name='CDNX_products_productdocuments_sublist_editmodal'),
    url(r'^productdocuments/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductDocumentDelete.as_view(), name='CDNX_products_productdocuments_sublist_delete'),

    url(r'^productfinals$', ProductFinalList.as_view(), name='CDNX_products_productfinals_list'),
    url(r'^productfinals/add$', ProductFinalCreate.as_view(), name='CDNX_products_productfinals_add'),
    url(r'^productfinals/addmodal$', ProductFinalCreateModal.as_view(), name='CDNX_products_productfinals_addmodal'),
    url(r'^productfinals/(?P<pk>\w+)$', ProductFinalDetails.as_view(), name='CDNX_products_productfinals_details'),
    url(r'^productfinals/(?P<pk>\w+)/edit$', ProductFinalUpdate.as_view(), name='CDNX_products_productfinals_edit'),
    url(r'^productfinals/(?P<pk>\w+)/editmodal$', ProductFinalUpdateModal.as_view(), name='CDNX_products_productfinals_editmodal'),
    url(r'^productfinals/(?P<pk>\w+)/delete$', ProductFinalDelete.as_view(), name='CDNX_products_productfinals_delete'),

    url(r'^productfinals/foreignsales/(?P<search>[\w\W]+|\*)$', ProductFinalForeignSales.as_view(), name='CDNX_products_productfinals_foreign_sales'),
    url(r'^productfinals/foreignpurchases/(?P<search>[\w\W]+|\*)$', ProductFinalForeignPurchases.as_view(), name='CDNX_products_productfinals_foreign_purchases'),

    url(r'^productfinals/(?P<pk>\w+)/related$', ProductFinalRelatedSubList.as_view(), name='CDNX_products_productfinalrelateds_sublist'),
    url(r'^productfinals/(?P<pk>\w+)/related/add$', ProductFinalRelatedSubUpdateModal.as_view(), name='CDNX_products_productfinalrelateds_sublist_add'),
    url(r'^productfinals/(?P<pk>\w+)/related/addmodal$', ProductFinalRelatedSubUpdateModal.as_view(), name='CDNX_products_productfinalrelateds_sublist_addmodal'),
    url(r'^productfinals/(?P<tpk>\w+)/related/(?P<pk>\w+)/delete$', ProductFinalRelatedSubDelete.as_view(), name='CDNX_products_productfinalrelateds_sublist_delete'),

    url(r'^productfinals/(?P<pk>\w+)/accesory$', ProductFinalAccesorySubList.as_view(), name='CDNX_products_productfinalaccesory_sublist'),
    url(r'^productfinals/(?P<pk>\w+)/accesory/add$', ProductFinalAccesorySubUpdateModal.as_view(), name='CDNX_products_productfinalaccesory_sublist_add'),
    url(r'^productfinals/(?P<pk>\w+)/accesory/addmodal$', ProductFinalAccesorySubUpdateModal.as_view(), name='CDNX_products_productfinalaccesory_sublist_addmodal'),
    url(r'^productfinals/(?P<tpk>\w+)/accesory/(?P<pk>\w+)/delete$', ProductFinalAccesorySubDelete.as_view(), name='CDNX_products_productfinalaccesory_sublist_delete'),

    url(r'^productfinals/(?P<pk>\w+)/sublist$', ProductFinalSubList.as_view(), name='CDNX_products_productfinals_sublist'),
    url(r'^productfinals/(?P<cpk>\w+)/sublist/add$', ProductFinalCreateModal.as_view(), name='CDNX_products_productfinals_sublist_add'),
    url(r'^productfinals/(?P<cpk>\w+)/sublist/addmodal$', ProductFinalCreateModal.as_view(), name='CDNX_products_productfinals_sublist_addmodal'),
    url(r'^productfinals/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductFinalDetailsModal.as_view(), name='CDNX_products_productfinals_sublist_details'),
    url(r'^productfinals/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductFinalUpdateModal.as_view(), name='CDNX_products_productfinals_sublist_edit'),
    url(r'^productfinals/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ProductFinalUpdateModal.as_view(), name='CDNX_products_productfinals_sublist_editmodal'),
    url(r'^productfinals/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductFinalDelete.as_view(), name='CDNX_products_productfinals_sublist_delete'),


    url(r'^productfinalimages$', ProductFinalImageList.as_view(), name='CDNX_products_productfinalimages_list'),
    url(r'^productfinalimages/(?P<pk>\w+)/edit$', ProductFinalImageUpdate.as_view(), name='CDNX_products_productfinalimages_edit'),
    url(r'^productfinalimages/(?P<pk>\w+)/editmodal$', ProductFinalImageUpdateModal.as_view(), name='CDNX_products_productfinalimages_editmodal'),
    url(r'^productfinalimages/(?P<pk>\w+)/delete$', ProductFinalImageDelete.as_view(), name='CDNX_products_productfinalimages_delete'),
    url(r'^productfinalimages/(?P<pk>\w+)/sublist$', ProductFinalImageSubList.as_view(), name='CDNX_products_productfinalimages_sublist'),
    url(r'^productfinalimages/(?P<cpk>\w+)/sublist/add$', ProductFinalImageCreateModal.as_view(), name='CDNX_products_productfinalimages_sublist_add'),
    url(r'^productfinalimages/(?P<cpk>\w+)/sublist/addmodal$', ProductFinalImageCreateModal.as_view(), name='CDNX_products_productfinalimages_sublist_addmodal'),
    url(r'^productfinalimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductFinalImageDetailsModal.as_view(), name='CDNX_products_productfinalimages_sublist_details'),
    url(r'^productfinalimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductFinalImageUpdateModal.as_view(), name='CDNX_products_productfinalimages_sublist_edit'),
    url(r'^productfinalimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ProductFinalImageUpdateModal.as_view(), name='CDNX_products_productfinalimages_sublist_editmodal'),
    url(r'^productfinalimages/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductFinalImageDelete.as_view(), name='CDNX_products_productfinalimages_sublist_delete'),

    url(r'^productfinalattributes$', ProductFinalAttributeList.as_view(), name='CDNX_products_productfinalattributes_list'),
    url(r'^productfinalattributes/(?P<pk>\w+)/editmodal$', ProductFinalAttributeUpdateModal.as_view(), name='CDNX_products_productfinalattributes_editmodal'),
    url(r'^productfinalattributes/(?P<pk>\w+)/delete$', ProductFinalAttributeDelete.as_view(), name='CDNX_products_productfinalattributes_delete'),
    url(r'^productfinalattributes/(?P<pk>\w+)/sublist$', ProductFinalAttributeSubList.as_view(), name='CDNX_products_productfinalattributes_sublist'),
    url(r'^productfinalattributes/(?P<pk>\w+)/sublist/add$', ProductFinalAttributeCreateModal.as_view(), name='CDNX_products_productfinalattributes_sublist_add'),
    url(r'^productfinalattributes/(?P<pk>\w+)/sublist/addmodal$', ProductFinalAttributeCreateModal.as_view(), name='CDNX_products_productfinalattributes_sublist_addmodal'),

    url(r'^productfinalattributes/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductFinalAttributeDetailsModal.as_view(), name='CDNX_products_productfinalattributes_sublist_details'),
    url(r'^productfinalattributes/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductFinalAttributeUpdateModal.as_view(), name='CDNX_products_productfinalattributes_sublist_edit'),
    url(r'^productfinalattributes/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ProductFinalAttributeUpdateModal.as_view(), name='CDNX_products_productfinalattributes_sublist_editmodal'),
    url(r'^productfinalattributes/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductFinalAttributeDelete.as_view(), name='CDNX_products_productfinalattributes_sublist_delete'),

    url(r'^productfeatures$', ProductFeatureList.as_view(), name='CDNX_products_productfeatures_list'),
    url(r'^productfeatures/(?P<pk>\w+)/edit$', ProductFeatureUpdate.as_view(), name='CDNX_products_productfeatures_edit'),
    url(r'^productfeatures/(?P<pk>\w+)/editmodal$', ProductFeatureUpdateModal.as_view(), name='CDNX_products_productfeatures_editmodal'),
    url(r'^productfeatures/(?P<pk>\w+)/delete$', ProductFeatureDelete.as_view(), name='CDNX_products_productfeatures_delete'),
    url(r'^productfeatures/(?P<pk>\w+)/sublist$', ProductFeatureSubList.as_view(), name='CDNX_products_productfeatures_sublist'),
    url(r'^productfeatures/(?P<pk>\w+)/sublist/add$', ProductFeatureCreateModal.as_view(), name='CDNX_products_productfeatures_sublist_add'),
    url(r'^productfeatures/(?P<pk>\w+)/sublist/addmodal$', ProductFeatureCreateModal.as_view(), name='CDNX_products_productfeatures_sublist_addmodal'),
    url(r'^productfeatures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductFeatureDetailsModal.as_view(), name='CDNX_products_productfeatures_sublist_details'),
    url(r'^productfeatures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductFeatureUpdateModal.as_view(), name='CDNX_products_productfeatures_sublist_edit'),
    url(r'^productfeatures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ProductFeatureUpdateModal.as_view(), name='CDNX_products_productfeatures_sublist_editmodal'),
    url(r'^productfeatures/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductFeatureDelete.as_view(), name='CDNX_products_productfeatures_sublist_delete'),

    url(r'^productuniques$', ProductUniqueList.as_view(), name='CDNX_products_productuniques_list'),
    url(r'^productuniques/(?P<pk>\w+)/edit$', ProductUniqueUpdate.as_view(), name='CDNX_products_productuniques_edit'),
    url(r'^productuniques/(?P<pk>\w+)/editmodal$', ProductUniqueUpdateModal.as_view(), name='CDNX_products_productuniques_editmodal'),
    url(r'^productuniques/(?P<pk>\w+)/delete$', ProductUniqueDelete.as_view(), name='CDNX_products_productuniques_delete'),
    url(r'^productuniques/(?P<pk>\w+)/sublist$', ProductUniqueSubList.as_view(), name='CDNX_products_productuniques_sublist'),
    url(r'^productuniques/(?P<cpk>\w+)/sublist/add$', ProductUniqueCreateModal.as_view(), name='CDNX_products_productuniques_sublist_add'),
    url(r'^productuniques/(?P<cpk>\w+)/sublist/addmodal$', ProductUniqueCreateModal.as_view(), name='CDNX_products_productuniques_sublist_addmodal'),
    url(r'^productuniques/(?P<cpk>\w+)/sublist/(?P<pk>\w+)$', ProductUniqueDetailsModal.as_view(), name='CDNX_products_productuniques_sublist_details'),
    url(r'^productuniques/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/edit$', ProductUniqueUpdateModal.as_view(), name='CDNX_products_productuniques_sublist_edit'),
    url(r'^productuniques/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/editmodal$', ProductUniqueUpdateModal.as_view(), name='CDNX_products_productuniques_sublist_editmodal'),
    url(r'^productuniques/(?P<cpk>\w+)/sublist/(?P<pk>\w+)/delete$', ProductUniqueDelete.as_view(), name='CDNX_products_productuniques_sublist_delete'),


    url(r'^flagshipproducts$', FlagshipProductList.as_view(), name='CDNX_products_flagshipproducts_list'),
    url(r'^flagshipproducts/add$', FlagshipProductCreate.as_view(), name='CDNX_products_flagshipproducts_add'),
    url(r'^flagshipproducts/addmodal$', FlagshipProductCreateModal.as_view(), name='CDNX_products_flagshipproducts_addmodal'),
    url(r'^flagshipproducts/(?P<pk>\w+)/edit$', FlagshipProductUpdate.as_view(), name='CDNX_products_flagshipproducts_edit'),
    url(r'^flagshipproducts/(?P<pk>\w+)/editmodal$', FlagshipProductUpdateModal.as_view(), name='CDNX_products_flagshipproducts_editmodal'),
    url(r'^flagshipproducts/(?P<pk>\w+)/delete$', FlagshipProductDelete.as_view(), name='CDNX_products_flagshipproducts_delete'),

    url(r'^listproducts/(?P<type>\w+)/(?P<pk>[0-9]+)$', ListProducts.as_view(), name='CDNX_products_list_products'),

    url(r'^groupvaluefeatures$', GroupValueFeatureList.as_view(), name='CDNX_products_GroupValueFeatures_list'),
    url(r'^groupvaluefeatures/add$', GroupValueFeatureCreate.as_view(), name='CDNX_products_GroupValueFeatures_add'),
    url(r'^groupvaluefeatures/addmodal$', GroupValueFeatureCreateModal.as_view(), name='CDNX_products_GroupValueFeatures_addmodal'),
    url(r'^groupvaluefeatures/(?P<pk>\w+)$', GroupValueFeatureDetails.as_view(), name='CDNX_products_GroupValueFeatures_details'),
    url(r'^groupvaluefeatures/(?P<pk>[0-9]+)/edit$', GroupValueFeatureUpdate.as_view(), name='CDNX_products_GroupValueFeatures_edit'),
    url(r'^groupvaluefeatures/(?P<pk>\w+)/editmodal$', GroupValueFeatureUpdateModal.as_view(), name='CDNX_products_GroupValueFeatures_editmodal'),
    url(r'^groupvaluefeatures/(?P<pk>\w+)/delete$', GroupValueFeatureDelete.as_view(), name='CDNX_products_GroupValueFeatures_delete'),

    url(r'^groupvalueattributes$', GroupValueAttributeList.as_view(), name='CDNX_products_GroupValueAttributes_list'),
    url(r'^groupvalueattributes/add$', GroupValueAttributeCreate.as_view(), name='CDNX_products_GroupValueAttributes_add'),
    url(r'^groupvalueattributes/addmodal$', GroupValueAttributeCreateModal.as_view(), name='CDNX_products_GroupValueAttributes_addmodal'),
    url(r'^groupvalueattributes/(?P<pk>\w+)$', GroupValueAttributeDetails.as_view(), name='CDNX_products_GroupValueAttributes_details'),
    url(r'^groupvalueattributes/(?P<pk>[0-9]+)/edit$', GroupValueAttributeUpdate.as_view(), name='CDNX_products_GroupValueAttributes_edit'),
    url(r'^groupvalueattributes/(?P<pk>\w+)/editmodal$', GroupValueAttributeUpdateModal.as_view(), name='CDNX_products_GroupValueAttributes_editmodal'),
    url(r'^groupvalueattributes/(?P<pk>\w+)/delete$', GroupValueAttributeDelete.as_view(), name='CDNX_products_GroupValueAttributes_delete'),

    url(r'^groupvaluefeaturespecials$', GroupValueFeatureSpecialList.as_view(), name='CDNX_products_GroupValueFeatureSpecials_list'),
    url(r'^groupvaluefeaturespecials/add$', GroupValueFeatureSpecialCreate.as_view(), name='CDNX_products_GroupValueFeatureSpecials_add'),
    url(r'^groupvaluefeaturespecials/addmodal$', GroupValueFeatureSpecialCreateModal.as_view(), name='CDNX_products_GroupValueFeatureSpecials_addmodal'),
    url(r'^groupvaluefeaturespecials/(?P<pk>\w+)$', GroupValueFeatureSpecialDetails.as_view(), name='CDNX_products_GroupValueFeatureSpecials_details'),
    url(r'^groupvaluefeaturespecials/(?P<pk>[0-9]+)/edit$', GroupValueFeatureSpecialUpdate.as_view(), name='CDNX_products_GroupValueFeatureSpecials_edit'),
    url(r'^groupvaluefeaturespecials/(?P<pk>\w+)/editmodal$', GroupValueFeatureSpecialUpdateModal.as_view(), name='CDNX_products_GroupValueFeatureSpecials_editmodal'),
    url(r'^groupvaluefeaturespecials/(?P<pk>\w+)/delete$', GroupValueFeatureSpecialDelete.as_view(), name='CDNX_products_GroupValueFeatureSpecials_delete'),


    url(r'^optionvaluefeatures$', OptionValueFeatureList.as_view(), name='CDNX_products_OptionValueFeatures_list'),
    url(r'^optionvaluefeatures/(?P<gpk>\w+)/edit$', OptionValueFeatureUpdate.as_view(), name='CDNX_products_OptionValueFeatures_edit'),
    url(r'^optionvaluefeatures/(?P<gpk>\w+)/editmodal$', OptionValueFeatureUpdateModal.as_view(), name='CDNX_products_OptionValueFeatures_editmodal'),
    url(r'^optionvaluefeatures/(?P<gpk>\w+)/delete$', OptionValueFeatureDelete.as_view(), name='CDNX_products_OptionValueFeatures_delete'),
    url(r'^optionvaluefeatures/(?P<pk>\w+)/sublist$', OptionValueFeatureSubList.as_view(), name='CDNX_products_OptionValueFeatures_sublist'),
    url(r'^optionvaluefeatures/(?P<pk>\w+)/sublistm$', OptionValueFeatureSubListModal.as_view(), name='CDNX_products_OptionValueFeatures_sublist_modal'),
    url(r'^optionvaluefeatures/(?P<gpk>[0-9]+)/sublist/add$', OptionValueFeatureCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add'),
    url(r'^optionvaluefeatures/(?P<gpk>[0-9]+)/sublistm/add$', OptionValueFeatureCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add2'),
    url(r'^optionvaluefeatures/(?P<gpk>[0-9]+)/sublist/addmodal$', OptionValueFeatureCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_addmodal'),
    url(r'^optionvaluefeatures/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)$', OptionValueFeatureDetailsModal.as_view(), name='CDNX_products_OptionValueFeatures_sublist_details'),
    url(r'^optionvaluefeatures/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)$', OptionValueFeatureDetailsModal.as_view(), name='CDNX_products_OptionValueFeatures_sublist_details'),
    url(r'^optionvaluefeatures/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)/edit$', OptionValueFeatureUpdateModal.as_view(), name='CDNX_products_OptionValueFeatures_sublist_editmodal'),
    url(r'^optionvaluefeatures/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/editmodal$', OptionValueFeatureUpdateModal.as_view(), name='CDNX_products_OptionValueFeatures_sublist_editmodal'),
    url(r'^optionvaluefeatures/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/delete$', OptionValueFeatureDelete.as_view(), name='CDNX_products_OptionValueFeatures_sublist_delete'),
    url(r'^optionvaluefeatures/foreign/(?P<search>[\w\W]+|\*)$', OptionValueFeatureForeign.as_view(), name='CDNX_products_OptionValueFeatures_foreign'),

    url(r'^optionvalueattributes$', OptionValueAttributeList.as_view(), name='CDNX_products_OptionValueAttributes_list'),
    url(r'^optionvalueattributes/(?P<gpk>\w+)/edit$', OptionValueAttributeUpdate.as_view(), name='CDNX_products_OptionValueAttributes_edit'),
    url(r'^optionvalueattributes/(?P<gpk>\w+)/editmodal$', OptionValueAttributeUpdateModal.as_view(), name='CDNX_products_OptionValueAttributes_editmodal'),
    url(r'^optionvalueattributes/(?P<gpk>\w+)/delete$', OptionValueAttributeDelete.as_view(), name='CDNX_products_OptionValueAttributes_delete'),
    url(r'^optionvalueattributes/(?P<pk>\w+)/sublist$', OptionValueAttributeSubList.as_view(), name='CDNX_products_OptionValueAttributes_sublist'),
    url(r'^optionvalueattributes/(?P<pk>\w+)/sublistm$', OptionValueAttributeSubListModal.as_view(), name='CDNX_products_OptionValueAttributes_sublist_modal'),
    url(r'^optionvalueattributes/(?P<gpk>[0-9]+)/sublist/add$', OptionValueAttributeCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add'),
    url(r'^optionvalueattributes/(?P<gpk>[0-9]+)/sublistm/add$', OptionValueAttributeCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add2'),
    url(r'^optionvalueattributes/(?P<gpk>[0-9]+)/sublist/addmodal$', OptionValueAttributeCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_addmodal'),
    url(r'^optionvalueattributes/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)$', OptionValueAttributeDetailsModal.as_view(), name='CDNX_products_OptionValueAttributes_sublist_details'),
    url(r'^optionvalueattributes/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)$', OptionValueAttributeDetailsModal.as_view(), name='CDNX_products_OptionValueAttributes_sublist_details'),
    url(r'^optionvalueattributes/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)/edit$', OptionValueAttributeUpdateModal.as_view(), name='CDNX_products_OptionValueAttributes_sublist_editmodal'),
    url(r'^optionvalueattributes/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/editmodal$', OptionValueAttributeUpdateModal.as_view(), name='CDNX_products_OptionValueAttributes_sublist_editmodal'),
    url(r'^optionvalueattributes/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/delete$', OptionValueAttributeDelete.as_view(), name='CDNX_products_OptionValueAttributes_sublist_delete'),
    url(r'^optionvalueattributes/foreign/(?P<search>[\w\W]+|\*)$', OptionValueAttributeForeign.as_view(), name='CDNX_products_OptionValueAttributes_foreign'),

    url(r'^optionvaluefeaturespecials$', OptionValueFeatureSpecialList.as_view(), name='CDNX_products_OptionValueFeatureSpecials_list'),
    url(r'^optionvaluefeaturespecials/(?P<gpk>\w+)/edit$', OptionValueFeatureSpecialUpdate.as_view(), name='CDNX_products_OptionValueFeatureSpecials_edit'),
    url(r'^optionvaluefeaturespecials/(?P<gpk>\w+)/editmodal$', OptionValueFeatureSpecialUpdateModal.as_view(), name='CDNX_products_OptionValueFeatureSpecials_editmodal'),
    url(r'^optionvaluefeaturespecials/(?P<gpk>\w+)/delete$', OptionValueFeatureSpecialDelete.as_view(), name='CDNX_products_OptionValueFeatureSpecials_delete'),
    url(r'^optionvaluefeaturespecials/(?P<pk>\w+)/sublist$', OptionValueFeatureSpecialSubList.as_view(), name='CDNX_products_OptionValueFeatureSpecials_sublist'),
    url(r'^optionvaluefeaturespecials/(?P<pk>\w+)/sublistm$', OptionValueFeatureSpecialSubListModal.as_view(), name='CDNX_products_OptionValueFeatureSpecials_sublist_modal'),
    url(r'^optionvaluefeaturespecials/(?P<gpk>[0-9]+)/sublist/add$', OptionValueFeatureSpecialCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add'),
    url(r'^optionvaluefeaturespecials/(?P<gpk>[0-9]+)/sublistm/add$', OptionValueFeatureSpecialCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add2'),
    url(r'^optionvaluefeaturespecials/(?P<gpk>[0-9]+)/sublist/addmodal$', OptionValueFeatureSpecialCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_addmodal'),
    url(r'^optionvaluefeaturespecials/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)$', OptionValueFeatureSpecialDetailsModal.as_view(), name='CDNX_products_OptionValueFeatureSpecials_sublist_details'),
    url(r'^optionvaluefeaturespecials/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)$', OptionValueFeatureSpecialDetailsModal.as_view(), name='CDNX_products_OptionValueFeatureSpecials_sublist_details'),
    url(r'^optionvaluefeaturespecials/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)/edit$', OptionValueFeatureSpecialUpdateModal.as_view(), name='CDNX_products_OptionValueFeatureSpecials_sublist_editmodal'),
    url(r'^optionvaluefeaturespecials/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/editmodal$', OptionValueFeatureSpecialUpdateModal.as_view(), name='CDNX_products_OptionValueFeatureSpecials_sublist_editmodal'),
    url(r'^optionvaluefeaturespecials/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/delete$', OptionValueFeatureSpecialDelete.as_view(), name='CDNX_products_OptionValueFeatureSpecials_sublist_delete'),
    url(r'^optionvaluefeaturespecials/foreign/(?P<search>[\w\W]+|\*)$', OptionValueFeatureSpecialForeign.as_view(), name='CDNX_products_OptionValueFeatureSpecials_foreign'),
]
