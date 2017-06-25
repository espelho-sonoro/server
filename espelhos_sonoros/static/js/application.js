$(function() {
  var ESPELHOS = ESPELHOS || {};

  function setupQueue() {
    var queueSocket = io('/queue');

    var buildQueueEntry = function(index, name) {
      var badge = $('<span>').addClass('badge').text(index);
      var userEntry = $('<p>').append(badge).append(name);
      return $('<div>').addClass('item').append(userEntry);
    };

    function updateQueueDiv(queue) {
      var queueDiv = $('#queue-list');
      queueDiv.empty();
      queue.forEach(function(element, index) {
        var entry = buildQueueEntry(index, element.name);
        queueDiv.append(entry);
      });
    };

    function openControlls() {
      $('#controller-container-commands').removeClass('hidden');
      $('#controller-container-join-queue').addClass('hidden');
    };

    function closeControlls() {
      $('#controller-container-commands').addClass('hidden');
      $('#controller-container-join-queue').removeClass('hidden');
    };

    function isController() {
      queueSocket.emit('isController');
    };

    function updateQueue() {
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

  function setupControlls() {
    var controllSocket = io('/control');

    function moveRight() {
      controllSocket.emit('RIGHT');
    };

    function moveLeft() {
      controllSocket.emit('LEFT');
    };

    $('#controller-right-button').bind('click', function() {
      moveRight();
    });

    $('#controller-left-button').bind('click', function() {
      moveLeft();
    });
  };

  function setupMap() {
    var mapOpts = {
        zoom: 5,
        mapTypeId: 'satellite',
        center: {
          lat: 0,
          lng: 0
      }
    };

    return new google.maps.Map($('#video-map').get(0), mapOpts);
  };

  function setupVideos(map) {
    var infoWindows = [];
    var bounds = new google.maps.LatLngBounds();

    function createMarker(video) {
      var latLng = new google.maps.LatLng(video.lat, video.lng);
      return new google.maps.Marker({position: latLng});
    };

    function closeAllInfoWindows() {
      infoWindows.forEach(function(iw) { iw.close(); });
    };

    function createBandCampPlayer(album, track) {
      if (!album || !track) return $('<div>');
      var url = 'https://bandcamp.com/EmbeddedPlayer/album=' + album + '/size=small/bgcol=ffffff/linkcol=0687f5/track=' + track + '/transparent=true';
      return $('<iframe>')
        .addClass('bandcamp-embedded-player')
        .attr('src', url)
        .attr('seamless', '')
        .append($('<a>')
          .attr('href', 'http://espelhosonoro.bandcamp.com/album/espelho-sonoro')
          .text('Espelho Sonoro by Espelho Sonoro'));
    };

    function createInfoWindow(video) {
      var content = $('<div>')
        .append($('<h5>')
          .text(video.title))
        .append($('<div>')
          .append($('<iframe>')
            .attr('src', 'https://youtube.com/embed/' + video.id)
            .attr('frameborder', 0)))
        .append($('<div>')
          .append(createBandCampPlayer(video.bandcampAlbum, video.bandcampTrack)))
        .html();
      return new google.maps.InfoWindow({content: content});
    };

    function createListElement(video) {
      return $('<button>').text(video.title)
        .addClass('list-group-item');
    };

    function videoHasPosition(video) {
      return video.lat && video.lng;
    };

    function addVideo(video, map, bounds, videoList) {
      var listElement = createListElement(video);
      videoList.append(listElement);

      if (videoHasPosition(video)) {
        var marker = createMarker(video);
        var infoWindow = createInfoWindow(video);

        infoWindows.push(infoWindow);

        function setListeners(fn) {
          listElement.off('click');
          google.maps.event.clearListeners(marker, 'click');

          listElement.on('click', fn);
          marker.addListener('click', fn);
        };

        function selectVideo() {
          videoList.children('.active').removeClass('active');
          listElement.addClass('active');

          closeAllInfoWindows();
          infoWindow.open(map, marker);

          setListeners(deselectVideo);
        };

        function deselectVideo() {
          listElement.removeClass('active');
          infoWindow.close();

          setListeners(selectVideo);
        };

        setListeners(selectVideo);
        marker.setMap(map);
        infoWindow.addListener('closeclick', deselectVideo);
        bounds.extend({lat: video.lat, lng: video.lng});
      }
    };

    function updateVideoList(map, videos) {
      var videoList = $('#video-list');

      videos.forEach(function(video) {
        addVideo(video, map, bounds, videoList);
      });

      map.fitBounds(bounds);
    };

    $.getJSON('/api/videos', function(videos) {
      updateVideoList(map, videos);
    });
  };

  window.ESPELHOS = ESPELHOS;

  setupQueue();
  setupControlls();
  var map = setupMap();
  setupVideos(map);
});
