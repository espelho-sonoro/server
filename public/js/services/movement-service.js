(function() {
  angular.module('EspelhosSonoros').service('MovementService', [
    '$http',
    function($http) {
      var service = this;
      var position = {
        x: 0,
        y: Math.PI/2
      }

      this.rotate = function(x, y) {
        position.x += x;
        position.y += y;
        //$http.post('/api/video/position/rotate', {x:x, y:y});
      };

      this.forcePosition = function(x, y) {
        //$http.post('/api/video/position', {x:x, y:y});
        position.x = x;
        position.y = y;
      };

      this.currentPosition = function(cb) {
        cb(position);
        //$http.get('/api/video/position')
          //.success(success);
      };
    }
  ]);
})();
