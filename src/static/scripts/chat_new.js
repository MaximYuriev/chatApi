const userList = document.getElementById('userList');
const chatHeader = document.getElementById('chatHeader');
const messages = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const searchButton = document.getElementById('searchButton');
const searchModal = document.getElementById('searchModal');
const closeModal = document.getElementsByClassName('close')[0];
const searchInput = document.getElementById('searchInput');
const searchSubmit = document.getElementById('searchSubmit');
const logoutButton = document.getElementById('logoutButton');

let currentUser = null;
let socket = null;
messagePollingInterval = null;

async function populateUserList() {
  const response = await fetch('/user/all_user')
  const users = await response.json()
  console.log(users)
  userList.innerHTML = '';
  users.forEach(user => {
    const userItem = document.createElement('div');
    userItem.classList.add('user-item');
    userItem.textContent = user.username;
    userItem.addEventListener('click', () => selectUser(user));
    userList.appendChild(userItem);
  });
}

populateUserList();

async function selectUser(user) {
  currentUser = user;
  chatHeader.innerHTML = `<span>Чат с ${user.username}</span>`;
  messageInput.disabled = false;
  sendButton.disabled = false;
  messages.innerHTML = '';


  document.querySelectorAll('.user-item').forEach(item => {
    item.classList.remove('active');
    if (item.textContent === user.username) {
      item.classList.add('active');
    }
  });
  connectWebSocket()
  await loadMessages(user.user_id)
  //startMessagePolling(user.user_id)
}
async function loadMessages(userId) {
    try {
        const response = await fetch(`/chat/message/${userId}`);
        const messages = await response.json();
        console.log(messages)
        const messagesContainer = document.getElementById('messages');
        messages['data'].map(message =>
            addMessageToChat(message.content, userId == message.recipient_id?'sent':'received')
        ).join('');
    } catch (error) {
        console.error('Ошибка загрузки сообщений:', error);
    }
}

function connectWebSocket(){
    if (socket) socket.close();

    socket = new WebSocket(`ws://localhost:8000/chat/ws/${currentUser.user_id}`);

    socket.onopen = () => console.log('WebSocket соединение установлено');

    socket.onmessage = function(event){
        const incomingMessage = JSON.parse(event.data);
        console.log(incomingMessage)
        if (incomingMessage.recipient_id === currentUser.user_id) {
            addMessageToChat(incomingMessage.content, 'sent');
        }
        else if (incomingMessage.sender_id === currentUser.user_id){
            addMessageToChat(incomingMessage.content, 'received')
        }
    };

    socket.onclose = () => console.log('WebSocket соединение закрыто');
}

async function sendMessage() {
  const messageText = messageInput.value.trim();
  if (messageText && currentUser) {
    const message = {"recipient_id": currentUser.user_id, "content": messageText}
    await fetch('/chat/message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(message)
    });
    socket.send(JSON.stringify(message));
    messageInput.value = '';
  }
}

function addMessageToChat(text, type) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message', type);
  messageElement.textContent = text;
  messages.appendChild(messageElement);
  messages.scrollTop = messages.scrollHeight;
}

function startMessagePolling(userId) {
    clearInterval(messagePollingInterval);
    messagePollingInterval = setInterval(() => loadMessages(userId), 1000);
}

sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});


searchButton.onclick = function() {
  searchModal.style.display = "block";
}

closeModal.onclick = function() {
  searchModal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == searchModal) {
    searchModal.style.display = "none";
  }
}

searchSubmit.onclick = function() {
  const searchName = searchInput.value.trim().toLowerCase();
  const foundUser = users.find(user => user.name.toLowerCase() === searchName);
  if (foundUser) {
    selectUser(foundUser);
    searchModal.style.display = "none";
    searchInput.value = '';
  } else {
    alert('Пользователь не найден');
  }
}


logoutButton.onclick = function() {
  if (confirm('Вы уверены, что хотите выйти?')) {

    alert('Вы вышли из системы');

    window.location.reload();
  }
}