function typeWriter(text, element, speed = 50) {
    let i = 0;
    element.innerHTML = '';  // Limpa o texto anterior

    function typing() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(typing, speed); // Controla a velocidade da digitação
        }
    }
    typing();
}

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

    // Adiciona a mensagem "Bot está digitando..."
    const typingElement = document.createElement('div');
    typingElement.textContent = "Bot está digitando...";
    typingElement.classList.add('typing-message');
    chatBox.appendChild(typingElement);

    // Scroll para a última mensagem
    chatBox.scrollTop = chatBox.scrollHeight;

    // Simular o delay da resposta do bot
    const typingDelay = 2000; // 2 segundos de delay para simular digitação

    setTimeout(() => {
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
            // Remove a mensagem de "Bot está digitando..."
            chatBox.removeChild(typingElement);

            // Cria um elemento para a resposta do bot
            const botMessageElement = document.createElement('div');
            botMessageElement.classList.add('bot-message');

            // Adiciona a resposta do bot ao chat
            chatBox.appendChild(botMessageElement);

            // Exibe a resposta letra por letra
            typeWriter(data.response, botMessageElement);

            // Scroll para a última mensagem
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            console.error('Erro:', error);

            // Remove a mensagem de "Bot está digitando..."
            chatBox.removeChild(typingElement);

            // Exibe a mensagem de erro
            const botMessageElement = document.createElement('div');
            botMessageElement.textContent = "Bot: Desculpe, ocorreu um erro ao processar sua mensagem.";
            botMessageElement.classList.add('bot-message');
            chatBox.appendChild(botMessageElement);
        });
    }, typingDelay); // Delay de 2 segundos antes de enviar a mensagem do bot
}
