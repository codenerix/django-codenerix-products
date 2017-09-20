/*
 *
 * django-codenerix-products
 *
 * Copyright 2017 Centrologic Computational Logistic Center S.L.
 *
 * Project URL : http://www.codenerix.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';

// Angular codenerix Controllers
angular.module('codenerixPRODUCTSControllers', [])

.controller('CDNXPRODUCTSFormProductFeatureCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        $scope.options = [];

        $scope.show_optionvalue = function(type_value){
            var result = false;
            if ($scope.valuegetforeingkey['feature'] != undefined){
                angular.forEach($scope.valuegetforeingkey['feature'].rows, function(value, key){

                    if (value.id == $scope[$scope.form_name].feature.$viewValue && value.type == type_value){
                        result = true;
                    }
                });
            }
            return result;
        }
    }
])
.controller('CDNXPRODUCTSFormProductAttributeCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        $scope.options = [];

        $scope.show_optionvalue = function(type_value){
            var result = false;
            if ($scope.valuegetforeingkey['attribute'] != undefined){
                angular.forEach($scope.valuegetforeingkey['attribute'].rows, function(value, key){

                    if (value.id == $scope[$scope.form_name].attribute.$viewValue && value.type == type_value){
                        result = true;
                    }
                });
            }
            return result;
        }
    }
])
.controller('CDNXPRODUCTSFormProductAddProductFinalCtrl', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register) {
        console.log("a");
        
        $scope.addnewandproductfinal = function () {
            console.log("b");
            var listid = 0;
            if ($scope.data.meta.linkadd) {
                $state.go('formcustom'+listid);
            }
        };
    }
])
.controller('FormAddCtrlProductCustom', ['$scope', '$rootScope', '$timeout', '$http', '$window', '$uibModal', '$state', '$stateParams', '$templateCache', 'Register','hotkeys',
    function ($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, hotkeys) {
        if (ws_entry_point==undefined) { ws_entry_point=""; }
        $scope.options = [];
        multiadd($scope, $rootScope, $timeout, $http, $window, $uibModal, $state, $stateParams, $templateCache, Register, 0, "/"+ws_entry_point+"/custom", hotkeys);
    }
])
;
