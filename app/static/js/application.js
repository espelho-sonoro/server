$(function() {
  var videoOpts = {
    src: 'http://360.littlstar.com/production/a0a5746e-87ac-4f20-9724-ecba40429e54/mobile.mp4',
    preload: true,
    autoplay: true,
    loop: true,
    muted: true,
    resizable: true,
    crossorigin: true,
  };

  var frame = new Axis(document.querySelector('#video'), videoOpts);
  frame.render();
  frame.controls.mouse.disable();
  frame.controls.keyboard.disable();

  frame.once('ready', function() {
    $('#side-pane').height($('#video-pane').height());
  });

  var videoSocket = io('/video');

  var setFramePosition = function(x, y) {
    videoSocket.emit('position', {x:x, y:y});
  };

  var rotateFrame = function(x, y) {
    videoSocket.emit('rotate', {x:x, y:y});
  };

  videoSocket.on('position', function(data) {
    frame.orientation.x = data.x;
    frame.orientation.y = data.y;
  });

  $('#downButton').bind('click', function() {
    rotateFrame(-0.2, 0);
  });

  $('#upButton').bind('click', function() {
    rotateFrame(0.2, 0);
  });

  $('#leftButton').bind('click', function() {
    rotateFrame(0, 0.2);
  });

  $('#rightButton').bind('click', function() {
    rotateFrame(0, -0.2);
  });

  $('#centerButton').bind('click', function() {
    setFramePosition(0, Math.PI/2);
  });

  $('#playButton').bind('click', function() {
    frame.play();
  });

  $('#pauseButton').bind('click', function() {
    frame.pause();
  });
});
