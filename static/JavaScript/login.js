document.getElementById("form_login").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    if (email && senha) {
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ email: email, senha: senha }),
        })
        .then(response => response.text())
        .then(data => {
            // Prepara o popup
            const popup = document.getElementById('popup');
            const popupMessage = document.getElementById('popup_message');
            const closePopup = document.getElementById('closePopup');

            if (data.includes('Você entrou')) {
                popupMessage.innerText = data;  // Mensagem de sucesso
                popup.style.display = 'block';  // Mostra o popup
                setTimeout(() => {
                    window.location.href = "home";  // Redireciona após 2 segundos
                }, 2000);
            } else {
                popupMessage.innerText = 'Erro: ' + data;  // Mensagem de erro
                popup.style.display = 'block';  // Mostra o popup
            }

            closePopup.onclick = function() {
                popup.style.display = 'none';  // Fecha o popup
            };
        })
        .catch((error) => {
            console.error('Erro:', error);
            alert('Ocorreu um erro inesperado. Tente novamente.');
        });
    } else {
        alert('Por favor, insira todos os dados.');
    }
});

// Para fechar o popup quando clicar fora dele
window.onclick = function(event) {
    const popup = document.getElementById('popup');
    if (event.target === popup) {
        popup.style.display = 'none';
    }
};
