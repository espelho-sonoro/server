(function(){
  angular.module('EspelhosSonoros')
    .config(function($routeProvider) {
      $routeProvider
        .when('/video', {
          templateUrl: '/templates/video.html',
          controller: 'VideoController',
          controllerAs: 'video'
        })
        .when('/', {
          templateUrl: '/templates/video.html',
          controller: 'VideoController',
          controllerAs: 'video'
        });
    });
})();
