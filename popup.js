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
    
    var selectedEmoji = document.getElementById(emojiId);

    
    selectedEmoji.style.backgroundColor = "Green";

    
}

  document.getElementById('button-yes').addEventListener('click', saveAndClose);
