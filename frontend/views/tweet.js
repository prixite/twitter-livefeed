'use strict';

angular.module('myApp.tweet', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/tweet', {
    templateUrl: 'views/tweet.html',
    controller: 'TweetCtrl'
  });
}])

.controller('TweetCtrl', ["$scope", function($scope) {
    $scope.tweets = [];

    var ws = new WebSocket("ws://localhost:8888/websocket");
    ws.onmessage = function(event) {
        var data = JSON.parse(event.data);
        $scope.tweets.push(data);
        $scope.$apply();
    };

}]);
