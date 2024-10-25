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


// Search functionality
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

// Logout functionality
logoutButton.onclick = function() {
  if (confirm('Вы уверены, что хотите выйти?')) {
    // In a real app, here you would send a request to the server to log out
    // and then redirect to the login page
    alert('Вы вышли из системы');
    // For demonstration, we'll just reload the page
    window.location.reload();
  }
}