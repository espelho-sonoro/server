$(function() {
  var userId = Math.floor(Math.random() * 100 - 1);

  $('#user-id').text('Usuário: ' + userId);

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
});
