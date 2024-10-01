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

    // var userInput = document.getElementById('user-input').value;
    
    closePopup();
  }

  function selectEmoji(emojiId) {
    
    var selectedEmoji = document.getElementById(emojiId);

    
    selectedEmoji.style.backgroundColor = "lightgreen";

    
}

  document.getElementById('button-yes').addEventListener('click', saveAndClose);
