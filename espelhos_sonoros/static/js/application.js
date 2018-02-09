$(function() {
  var ESPELHOS = ESPELHOS || {};

  function setupAudioStream() {
    $('#audio-stream').on('error', function(evt) {
      console.debug(evt);
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

    var map = $('#video-map').get(0);
    if (map !== null && map !== undefined) {
      return new google.maps.Map(map, mapOpts);
    } else {
      return undefined;
    }
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

  var map = setupMap();
  if (map != undefined) {
    setupVideos(map);
  }
  setupAudioStream();
});
