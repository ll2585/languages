var hanjaApp = angular.module('hanjaApp', ['ngRoute']).config(function ($routeProvider) {
  $routeProvider
    .when('/', {
        templateUrl : 'static/hanja/summary.html',
        controller : 'MainCtrl'
  }).when('/articles', {
        templateUrl : 'static/hanja/article_main.html',
        controller : 'ArticleCtrl'
  });
});
hanjaApp.controller('MainCtrl', ['$scope', '$http', function($scope, $http){
    $scope.message = "HI!";
    $scope.hanjas = [];
    $scope.cur_page = '';


    $scope.load_hanja = function(level){
        var httpRequest = $http({
            method: 'GET',
            url: 'api/v1.0/korean/hanja/list/' + level
        }).success(function(data, status) {
            $scope.cur_page = level;
            $scope.hanjas = data['result'];
        });
    };
}]);


hanjaApp.controller('ArticleCtrl', ['$scope', '$http', function($scope, $http){
    $scope.message = "HI!";
    $scope.cur_page = '';
    $scope.hanja_levels = ['8',
  '7',
  '6-1',
  '6-2',
  '5-1',
  '5-2',
  '4-1',
  '4-2',
  '3-1',
  '3-2',
  '2-2',
  '2-1',
  '1'
];
    $scope.load_articles = function(){
        var httpRequest = $http({
            method: 'GET',
            url: '/api/v1.0/korean/hanja/article/all/'
        }).success(function(data, status) {
            console.log(data);
            $scope.articles = data;
        });
    };
}]);
