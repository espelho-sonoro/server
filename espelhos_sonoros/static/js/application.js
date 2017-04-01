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

    var mapKey = 'AIzaSyD2PJY61U_oha8c38oR-18xRFw2OD5dMeM';
    var mapSrc = 'https://maps.googleapis.com/maps/api/js?callback=ESPELHOS.mapCallback&key=' + mapKey;
    var mapScript = $('<script>').attr('src', mapSrc).appendTo('body');

    var addMapMakers = function(map) {
      var bounds = new google.maps.LatLngBounds();
      var infoWindows = [];
      var videoList = $('#video-list').children('a').each(function(idx, child) {
        var videoId = $(child).data('video-id');
        var videoTitle = $(child).text().trim();
        var lat = $(child).data('lat');
        var lng = $(child).data('lng');

        if (lat !== 'None' && lng !== 'None') {
          var videoLocation = new google.maps.LatLng(lat, lng);

          var markerOpts = {
            map: map,
            title: videoId,
            position: videoLocation
          };

          var marker = new google.maps.Marker(markerOpts);
          var infoWindow = new google.maps.InfoWindow({
            content: videoTitle
          });

          infoWindows.push(infoWindow);

          var openInfoWindow = function() {
            $(child).siblings('a').removeClass('active');
            $(child).toggleClass('active');
            infoWindows.forEach(function(iw) { iw.close(); });
            infoWindow.open(map, marker);
          };

          var closeInfoWindow = function() {
            $(child).removeClass('active');
          };

          infoWindow.addListener('closeclick', closeInfoWindow);
          marker.addListener('click', openInfoWindow);
          $(child).on('click', openInfoWindow);

          bounds.extend(videoLocation);
        }
      });
      map.fitBounds(bounds);
    };

    var mapCallback = function() {
      var map = new google.maps.Map(document.getElementById('video-map'), {
          zoom: 5,
          center: {
            lat: 0,
            lng: 0
        }
      });
      addMapMakers(map);
    };

    ESPELHOS.mapCallback = mapCallback;
  };

  var setupVideos = function() {
    var videoList = $('#video-list').children('li')
  };

  setupMap();
  setupQueue();
  setupControlls();
  setupVideos();

  window.ESPELHOS = ESPELHOS;
});
