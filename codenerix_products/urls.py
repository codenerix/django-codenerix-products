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
    GroupValueList, GroupValueCreate, GroupValueCreateModal, GroupValueUpdate, GroupValueUpdateModal, GroupValueDelete, \
    OptionValueList, OptionValueCreateModal, OptionValueUpdate, OptionValueUpdateModal, OptionValueDelete, OptionValueForeign, \
    GroupValueDetails, OptionValueSubList, OptionValueDetailsModal, \
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
    ListProducts, OptionValueSubListModal, TypeTaxDetails, \
    ProductFinalSubList, ProductFinalDetailsModal

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

    url(r'^groupvalues$', GroupValueList.as_view(), name='CDNX_products_groupvalues_list'),
    url(r'^groupvalues/add$', GroupValueCreate.as_view(), name='CDNX_products_groupvalues_add'),
    url(r'^groupvalues/addmodal$', GroupValueCreateModal.as_view(), name='CDNX_products_groupvalues_addmodal'),
    url(r'^groupvalues/(?P<pk>\w+)$', GroupValueDetails.as_view(), name='CDNX_products_groupvalues_details'),
    url(r'^groupvalues/(?P<pk>[0-9]+)/edit$', GroupValueUpdate.as_view(), name='CDNX_products_groupvalues_edit'),
    url(r'^groupvalues/(?P<pk>\w+)/editmodal$', GroupValueUpdateModal.as_view(), name='CDNX_products_groupvalues_editmodal'),
    url(r'^groupvalues/(?P<pk>\w+)/delete$', GroupValueDelete.as_view(), name='CDNX_products_groupvalues_delete'),

    url(r'^optionvalues$', OptionValueList.as_view(), name='CDNX_products_optionvalues_list'),
    url(r'^optionvalues/(?P<gpk>\w+)/edit$', OptionValueUpdate.as_view(), name='CDNX_products_optionvalues_edit'),
    url(r'^optionvalues/(?P<gpk>\w+)/editmodal$', OptionValueUpdateModal.as_view(), name='CDNX_products_optionvalues_editmodal'),
    url(r'^optionvalues/(?P<gpk>\w+)/delete$', OptionValueDelete.as_view(), name='CDNX_products_optionvalues_delete'),
    url(r'^optionvalues/(?P<pk>\w+)/sublist$', OptionValueSubList.as_view(), name='CDNX_products_optionvalues_sublist'),
    url(r'^optionvalues/(?P<pk>\w+)/sublistm$', OptionValueSubListModal.as_view(), name='CDNX_products_optionvalues_sublist_modal'),
    url(r'^optionvalues/(?P<gpk>[0-9]+)/sublist/add$', OptionValueCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add'),
    url(r'^optionvalues/(?P<gpk>[0-9]+)/sublistm/add$', OptionValueCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_add2'),
    url(r'^optionvalues/(?P<gpk>[0-9]+)/sublist/addmodal$', OptionValueCreateModal.as_view(), name='CDNX_products_optionv2alues_sublist_addmodal'),
    url(r'^optionvalues/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)$', OptionValueDetailsModal.as_view(), name='CDNX_products_optionvalues_sublist_details'),
    url(r'^optionvalues/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)$', OptionValueDetailsModal.as_view(), name='CDNX_products_optionvalues_sublist_details'),
    url(r'^optionvalues/(?P<cpk>[0-9]+)/sublistm/(?P<pk>[0-9]+)/edit$', OptionValueUpdateModal.as_view(), name='CDNX_products_optionvalues_sublist_editmodal'),
    url(r'^optionvalues/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/editmodal$', OptionValueUpdateModal.as_view(), name='CDNX_products_optionvalues_sublist_editmodal'),
    url(r'^optionvalues/(?P<cpk>[0-9]+)/sublist/(?P<pk>[0-9]+)/delete$', OptionValueDelete.as_view(), name='CDNX_products_optionvalues_sublist_delete'),
    url(r'^optionvalues/foreign/(?P<search>[\w\W]+|\*)$', OptionValueForeign.as_view(), name='CDNX_products_features_values_foreign'),

    url(r'^flagshipproducts$', FlagshipProductList.as_view(), name='CDNX_products_flagshipproducts_list'),
    url(r'^flagshipproducts/add$', FlagshipProductCreate.as_view(), name='CDNX_products_flagshipproducts_add'),
    url(r'^flagshipproducts/addmodal$', FlagshipProductCreateModal.as_view(), name='CDNX_products_flagshipproducts_addmodal'),
    url(r'^flagshipproducts/(?P<pk>\w+)/edit$', FlagshipProductUpdate.as_view(), name='CDNX_products_flagshipproducts_edit'),
    url(r'^flagshipproducts/(?P<pk>\w+)/editmodal$', FlagshipProductUpdateModal.as_view(), name='CDNX_products_flagshipproducts_editmodal'),
    url(r'^flagshipproducts/(?P<pk>\w+)/delete$', FlagshipProductDelete.as_view(), name='CDNX_products_flagshipproducts_delete'),

    url(r'^listproducts/(?P<type>\w+)/(?P<pk>[0-9]+)$', ListProducts.as_view(), name='CDNX_products_list_products'),
]
