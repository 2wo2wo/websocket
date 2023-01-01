const roomName = JSON.parse(document.getElementById('room-name').textContent);
  const userId = JSON.parse(document.getElementById('user_id').textContent);

  const chatSocket = new WebSocket(
      'ws://'
      + window.location.host
      + '/ws/chat/'
      + roomName
      + '/'
  );

  chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      console.log(data)
      elMessage(data.message)

  };

  chatSocket.onclose = function(e) {
      console.error('Chat socket closed unexpectedly');
  };

  document.querySelector('#chat-message-input').focus();
  document.querySelector('#chat-message-input').onkeyup = function(e) {
      if (e.keyCode === 13) {  // enter, return
          document.querySelector('#chat-message-submit').click();
      }
  };

  function createSender(message) {
    const top = document.createElement('div')
    top.classList.add('chat__conversation-board__message-container')
    const child = document.createElement('div')
    child.classList.add("chat__conversation-board__message__context")
    const child_of_child = document.createElement('div')
    child_of_child.classList.add('chat__conversation-board__message__bubble')
    const textMessage = document.createElement('span')
    textMessage.textContent = message
    child_of_child.appendChild(textMessage)
    child.appendChild(child_of_child)
    top.appendChild(child)
    return top
  }

  function elMessage(message){
      let a = document.getElementById('chat_board');
      const fragment = document.createDocumentFragment();
      const li = fragment
      .appendChild(createSender(message));
      a.appendChild(fragment)
  }

  document.querySelector('#chat-message-submit').onclick = function(e) {
      const messageInputDom = document.querySelector('#chat-message-input');
      const message = messageInputDom.value;

      chatSocket.send(JSON.stringify({
          'user_id':userId,
          'message': message
      }));

      messageInputDom.value = '';
  };
