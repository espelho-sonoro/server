(function(){
  angular.module('EspelhosSonoros')
    .config(function($routeProvider) {
      $routeProvider
        .when('/video', {
          templateUrl: '/templates/video.html',
          controller: 'PlayerController',
          controllerAs: 'player'
        })
        .when('/', {
          templateUrl: '/templates/video.html',
          controller: 'PlayerController',
          controllerAs: 'player'
        });
    });
})();
