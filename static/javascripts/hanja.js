var hanjaApp = angular.module('hanjaApp', ['ngRoute']).config(function ($routeProvider) {
  $routeProvider
    .when('/', {
        templateUrl : 'static/hanja/summary.html',
        controller : 'MainCtrl'
  });
});
hanjaApp.controller('MainCtrl', ['$scope', '$http', function($scope, $http){
    $scope.message = "HI!";
    $scope.hanjas = [];


    $scope.load_hanja = function(){
        var httpRequest = $http({
            method: 'GET',
            url: '/static/json/hanja.json'
        }).success(function(data, status) {
            $scope.hanjas = data;
        });
    };
}]);


hanjaApp.directive('hanjas', function() {
     return {
        restrict: 'E',
        replace: true,
        template: '<table cellspacing="0" cellpadding="0">'
        + '<colgroup span="7"></colgroup>'
        + '<tbody>'
        + '<tr class="days">'
        + '</tr>'
        + '<tr ng-repeat="week in hanja_row">'
        + '<td ng-repeat="day in week">{{day}}</td>'
        + '</tr></tbody></table>',
        link: function(scope) {
            scope.hanja_row = [];
            for (var i = 0; i < scope.load_hanja.length; i++) {
                if (i % 4 == 0) {
                    scope.hanja_row.push([]);
                }
                scope.hanja_row[scope.hanja_row.length-1].push(scope.load_hanja[i]);
            }
        }
    }
});