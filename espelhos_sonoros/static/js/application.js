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

    var setupVideos = function(map) {
      $.ajax('/api/videos').done(function(videos) {
        addVideos(map, videos);
      });
    };

    var createListElement = function(video) {
      return $('<button>').text(video.title)
        .addClass('list-group-item');
    };

    var createMarker = function(video) {
      var latLng = new google.maps.LatLng(video.lat, video.lng);
      return new google.maps.Marker({position: latLng});
    };

    var createInfoWindow = function(video) {
      var content = $('<div>')
        .append($('<h3>').text(video.title))
        .append($('<div>').append($('<a>')
                .attr('target', '_blank')
                .attr('href', video.url)
                .text('Assistir no Youtube')))
        .html();
      return new google.maps.InfoWindow({content: content});
    };

    var videoHasPosition = function(video) {
      return video.lat && video.lng;
    };

    var addVideos = function(map, videos) {
      var bounds = new google.maps.LatLngBounds();
      var infoWindows = [];
      var videoList = $('#video-list');

      videos.forEach(function(video) {
        var listElement = createListElement(video);
        videoList.append(listElement);

        if (videoHasPosition(video)) {
          var marker = createMarker(video);
          var infoWindow = createInfoWindow(video);

          infoWindows.push(infoWindow);

          var setListeners = function(fn) {
            listElement.off('click');
            listElement.on('click', fn);
            google.maps.event.clearListeners(marker, 'click');
            marker.addListener('click', fn);
          };

          var selectVideo = function() {
            videoList.children('.active').removeClass('active');
            listElement.addClass('active');

            infoWindows.forEach(function(iw) { iw.close(); });
            infoWindow.open(map, marker);

            setListeners(deselectVideo);
          };

          var deselectVideo = function() {
            listElement.removeClass('active');
            infoWindow.close();

            setListeners(selectVideo);
          };

          setListeners(selectVideo);
          marker.setMap(map);
          infoWindow.addListener('closeclick', deselectVideo);
          bounds.extend({lat: video.lat, lng: video.lng});
        }
      });

      map.fitBounds(bounds);
    };

    var mapOpts = {
        zoom: 5,
        center: {
          lat: 0,
          lng: 0
      }
    };

    var map = new google.maps.Map($('#video-map').get(0), mapOpts);
    setupVideos(map);
  };

  setupQueue();
  setupControlls();
  setupMap();

  window.ESPELHOS = ESPELHOS;
});
