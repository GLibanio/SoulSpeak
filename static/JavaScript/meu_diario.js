function sendMessage() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const userMessage = userInput.value;

    if (userMessage.trim() === "") {
        return; // Não enviar mensagens vazias
    }

    // Adiciona a mensagem do usuário ao chat
    const userMessageElement = document.createElement('div');
    userMessageElement.textContent = "Você: " + userMessage;
    userMessageElement.classList.add('user-message');
    chatBox.appendChild(userMessageElement);

    // Limpa o campo de input
    userInput.value = '';

    // Envia a mensagem do usuário para o servidor e exibe a resposta do bot
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // Adiciona a resposta do bot ao chat
        const botMessageElement = document.createElement('div');
        botMessageElement.textContent = "Bot: " + data.response;
        botMessageElement.classList.add('bot-message');
        chatBox.appendChild(botMessageElement);

        // Scroll para a última mensagem
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error('Erro:', error);
        const botMessageElement = document.createElement('div');
        botMessageElement.textContent = "Bot: Desculpe, ocorreu um erro ao processar sua mensagem.";
        botMessageElement.classList.add('bot-message');
        chatBox.appendChild(botMessageElement);
    });
}
