(function() {
  angular.module('EspelhosSonoros').service('MovementService', [
    '$http',
    function($http) {
      var service = this;

      this.rotate = function(x, y) {
        $http.post('/api/video/position', {x:x, y:y});
      };

      this.forcePosition = function(x, y) {
        $http.put('/api/video/position', {x:x, y:y});
      };

      this.currentPosition = function(cb) {
        $http.get('/api/video/position')
          .success(cb);
      };
    }
  ]);
})();
