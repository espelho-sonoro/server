(function() {
  angular.module('EspelhosSonoros').controller('VideoController', function() {

    var controller = this;
    var el = document.querySelector('#video');

    var videoOpts = {
      src: 'http://360.littlstar.com/production/a0a5746e-87ac-4f20-9724-ecba40429e54/mobile.mp4',
      preload: true,
      autoplay: true,
      loop: true,
      resizable: true,
      crossorigin: true,
    };

    this.frame = new Axis(el, videoOpts);
    this.frame.render();

    this.frame.once('ready', function() {
      controller.frame.focus();
    });

    this.rotateDown = function() {
      this.frame.rotate('x', {'value': -0.2});
    };

    this.rotateUp = function() {
      this.frame.rotate('x', {'value': 0.2});
    };

    this.rotateLeft = function() {
      this.frame.rotate('y', {'value': 0.2});
    };

    this.rotateRight = function() {
      this.frame.rotate('y', {'value': -0.2});
    };

    this.center = function() {
      this.frame.orientation.x = 0;
      this.frame.orientation.y = Math.PI/2;
      this.frame.orientation.update();
    };

    this.play = function() {
      this.frame.play();
    };

    this.pause = function() {
      this.frame.pause();
    };

  });
})();
