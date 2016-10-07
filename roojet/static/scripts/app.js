'use strict';

/**
 * @ngdoc overview
 * @name ROO
 * @description
 * # ROO
 *
 * Main module of the application.
 */
var app = angular.module('ROO', [
  'ngResource',
  'chart.js'
]);

app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.config(function($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.withCredentials = true;
});
