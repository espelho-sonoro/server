$(function() {
  var ESPELHOS = ESPELHOS || {};

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
      $('#title').text('Controlling motherfucker');
      console.debug('Started controlling');
    };

    $('#join-queue-button').bind('click', function() {
      queueSocket.emit('enterQueue');
    });

    $('#test-refresh-queue-button').bind('click', function() {
      console.debug('Refreshing queue');
      queueSocket.emit('list');
    });

    $('#test-gain-control-button').bind('click', function() {
      console.debug('Gaining control');
      queueSocket.emit('gainControl');
    });

    $('#test-join-queue-button').bind('click', function() {
      console.debug('Joining queue');
      queueSocket.emit('enterQueue');
    });

    queueSocket.on('updateQueue', function(queue) {
      console.debug('Updating queue: ', queue);
      refreshQueue(queue);
    });

    queueSocket.on('startControl', function() {
      console.debug('Starting to control');
      alert('Controlando!');
    });

    queueSocket.on('stopControl', function() {
      console.debug('Stoping control');
      alert('Descontrolando!');
    });

    queueSocket.emit('list');
  };

  var setupControlls = function() {
    var controllSocket = io('/control');

    $('#test-right-button').bind('click', function() {
      console.debug('Emitting right');
      controllSocket.emit('RIGHT');
    });

    $('#test-left-button').bind('click', function() {
      console.debug('Emitting left');
      controllSocket.emit('LEFT');
    });

  };

  setupChat();
  setupQueue();
  setupControlls();

  window.ESPELHOS = ESPELHOS;
});
