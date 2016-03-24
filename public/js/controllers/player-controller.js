(function() {
  angular.module('EspelhosSonoros').controller('PlayerController', [
    'MovementService',
    function(MovementService) {
      var controller = this;
      var el = document.querySelector('#video');

      var videoOpts = {
        src: 'http://360.littlstar.com/production/a0a5746e-87ac-4f20-9724-ecba40429e54/mobile.mp4',
        preload: true,
        autoplay: true,
        loop: true,
        muted: true,
        resizable: true,
        crossorigin: true,
      };

      this.frame = new Axis(el, videoOpts);
      this.frame.render();
      this.frame.controls.mouse.disable();
      this.frame.controls.keyboard.disable();

      this.updatePositionFromService = function() {
        MovementService.currentPosition(function(position) {
          controller.frame.orientation.x = position.x;
          controller.frame.orientation.y = position.y;
        });
      };

      this.frame.on('ready', function() {
        controller.poolPosition();
      });

      this.rotateDown = function() {
        MovementService.rotate(-0.2, 0);
      };

      this.rotateUp = function() {
        MovementService.rotate(0.2, 0);
      };

      this.rotateLeft = function() {
        MovementService.rotate(0, 0.2);
      };

      this.rotateRight = function() {
        MovementService.rotate(0, -0.2);
      };

      this.center = function() {
        MovementService.forcePosition(0, Math.PI/2);
      };

      this.play = function() {
        this.frame.play();
      };

      this.pause = function() {
        this.frame.pause();
      };

      this.poolPosition = function() {
        setInterval(function() {
          controller.updatePositionFromService();
          controller.poolPosition();
        }, 500);
      };
    }
  ]);
})();
