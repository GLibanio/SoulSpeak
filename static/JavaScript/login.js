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
        .then(response => response.json())
        .then(data => {
            const popup = document.getElementById('popup');
            const popupMessage = document.getElementById('popup_message');
            const closePopup = document.getElementById('closePopup');

            if (data.success) {
                popupMessage.innerText = "Login bem-sucedido!";
                popup.style.display = 'block';
                setTimeout(() => {
                    // Redireciona com base no tipo de usuário
                    if (data.tipo_usuario === 'admin') {
                        window.location.href = "/admin";
                    } else if (data.tipo_usuario === 'psicologo') {
                        window.location.href = "/psicologo";
                    } else {
                        window.location.href = "/home";
                    }
                }, 2000);
            } else {
                popupMessage.innerText = 'Erro: ' + data.error;
                popup.style.display = 'block';
            }

            closePopup.onclick = function() {
                popup.style.display = 'none';
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

window.onclick = function(event) {
    const popup = document.getElementById('popup');
    if (event.target === popup) {
        popup.style.display = 'none';
    }
};
