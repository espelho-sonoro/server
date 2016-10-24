$(function() {

  var setupVideo = function() {
    var videoSocket = io('/video');

    var rotateFrame = function(x, y) {
      videoSocket.emit('rotate', {x:x, y:y});
    };

    $('#leftButton').bind('click', function() {
      rotateFrame(0, 0.2);
    });

    $('#rightButton').bind('click', function() {
      rotateFrame(0, -0.2);
    });
  };

  var setupChat = function() {
    var chatSocket = io('/chat');

    var formatMessage = function(message) {
      return message.user + ': ' + message.text;
    };

    var addMessage = function(message) {
      $('#messages-container > ul').append($('<li>').text(formatMessage(message)));
    };

    var sendMessage = function(message) {
      chatSocket.emit('new-message', message);
    };

    chatSocket.on('new-message', function(message) {
      addMessage(message);
    });

    $('#send-message-button').bind('click', function() {
      var textArea = $('#send-message-text');
      var textMessage = textArea.val();
      textArea.val('');
      var message= {user: userId, text: textMessage};
      sendMessage(message);
    });

    $('#send-message-text').bind('keydown', function(event) {
      if (event.keyCode == 13) {
        $('#send-message-button').click();
      }
    });
  };

  var setupQueue = function() {
    var queueSocket = io('/queue');

    var buildQueueEntry = function(index, name) {
      var badge = $('<span>').addClass('badge').text(index);
      var userEntry = $('<p>').append(badge).append(name);
      return $('<div>').addClass('item').append(userEntry);
    };

    var refreshQueue = function (queue) {
      var newQueue = queue.map(function(element, index) {
        return buildQueueEntry(index, element.name);
      });
      $('#queue-list').empty().append(newQueue);
    };

    var openControlls = function() {
      $('.control-buttons').removeClass('disabled');
    };

    $('#join-queue-button').bind('click', function() {
      queueSocket.emit('join');
    });

    queueSocket.on('updateList', function(queue) {
      refreshQueue(queue);
    });

    queueSocket.on('controlling', function(queue) {
      openControlls();
    });

    $.get('/queue').done(function(queue) { refreshQueue(queue) });

    window.ESPELHOS = window.ESPELHOS || {};
    window.ESPELHOS.refreshQueue = refreshQueue;
  };

  setupVideo();
  setupChat();
  setupQueue();
});
