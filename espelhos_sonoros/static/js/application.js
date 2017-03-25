$(function() {
  var ESPELHOS = ESPELHOS || {};

  var setupQueue = function() {
    var queueSocket = io('/queue');

    var buildQueueEntry = function(index, name) {
      var badge = $('<span>').addClass('badge').text(index);
      var userEntry = $('<p>').append(badge).append(name);
      return $('<div>').addClass('item').append(userEntry);
    };

    var updateQueueDiv = function (queue) {
      var newQueue = queue.map(function(element, index) {
        return buildQueueEntry(index, element.name);
      });
      $('#queue-list').empty().append(newQueue);
    };

    var openControlls = function() {
      $('.controller-container-commands').removeClass('hidden');
      $('.controller-container-join-queue').addClass('hidden');
    };

    var closeControlls = function() {
      $('.controller-container-commands').addClass('hidden');
      $('.controller-container-join-queue').removeClass('hidden');
    }

    var isController = function() {
      queueSocket.emit('isController');
    };

    var updateQueue = function() {
      queueSocket.emit('getQueue');
    }

    $('#join-queue-button').bind('click', function() {
      queueSocket.emit('enterQueue');
    });

    queueSocket.on('updateQueue', function(queue) {
      updateQueueDiv(queue);
    });

    queueSocket.on('startControl', function() {
      openControlls();
    });

    queueSocket.on('stopControl', function() {
      closeControlls();
    });

    ESPELHOS.updateQueue = updateQueue;
    ESPELHOS.isController = isController;
  };

  var setupControlls = function() {
    var controllSocket = io('/control');

    var moveRight = function() {
      controllSocket.emit('RIGHT');
    }

    var moveLeft = function() {
      controllSocket.emit('LEFT');
    }

    $('#controller-right-button').bind('click', function() {
      moveRight();
    });

    $('#controller-left-button').bind('click', function() {
      moveLeft();
    });
  };

  var setupMap = function() {
    var map = new google.maps.Map(document.getElementById('video-map'));
  };

  var setupVideos = function() {
    var updateVideoList = function(videos) {
      var elements = videos.map(buildVideoElement);
      $('#video-list').append(elements);
    };

    var buildVideoElement = function(video) {
      return $('<li>').addClass('video-element').text(video.name);
    };

    $.ajax('/api/videos').done(function(videos) {
      updateVideoList(videos);
    });
  };

  ESPELHOS.setupMap = setupMap;

  setupQueue();
  setupControlls();
  setupVideos();

  ESPELHOS.updateQueue();
  ESPELHOS.isController();

  window.ESPELHOS = ESPELHOS;
});
