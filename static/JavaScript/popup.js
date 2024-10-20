document.addEventListener('DOMContentLoaded', function() {
  setTimeout(openPopup, 1000); 
});

function openPopup() {
  document.getElementById('popup').style.display = 'block';
}

function closePopup() {
  document.getElementById('popup').style.display = 'none';
}

function handleNo() {
  closePopup();
}

function saveAndClose() {
  closePopup();
}

function selectEmoji(emojiId) {
  // Reseta o fundo de todos os emojis
  let emojis = document.querySelectorAll('.emoji');
  emojis.forEach(function(emoji) {
      emoji.style.backgroundColor = '';  // Volta ao estado inicial
  });

  // Destaca o emoji selecionado
  var selectedEmoji = document.getElementById(emojiId);
  selectedEmoji.style.backgroundColor = "lightgreen";  // Muda cor de fundo para o selecionado
}

document.getElementById('button-yes').addEventListener('click', saveAndClose);
