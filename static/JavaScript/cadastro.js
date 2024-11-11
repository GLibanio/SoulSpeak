// Função para abrir o popup de termos
function openTerms() {
    var modal = document.getElementById('popup');
    modal.style.display = "block";

    // Fechar o popup ao clicar no "X"
    var closeBtn = document.getElementsByClassName("close")[0];
    closeBtn.onclick = function() {
        modal.style.display = "none";
    };

    // Fechar o popup ao clicar fora dele
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}

// Função para aceitar os termos e habilitar o checkbox
function acceptTerms() {
    document.getElementById('terms').disabled = false; // Habilita o checkbox
    document.getElementById('popup').style.display = "none"; // Fecha o popup de termos
}

// Verifica se o checkbox de termos está marcado e habilita o botão de envio
document.getElementById('terms').addEventListener('change', function() {
    var submitButton = document.getElementById('submit_button');
    submitButton.disabled = !this.checked; // Habilita/desabilita o botão de envio
});

// Função para mostrar popups (erro ou sucesso)
function showPopup(message) {
    var popup = document.getElementById('popup_message');
    popup.textContent = message;
    var modal = document.getElementById('popup');
    modal.style.display = "block";
}

// Função para realizar o cadastro via AJAX
document.getElementById('form_cadastro').onsubmit = function(event) {
    event.preventDefault();

    var formData = new FormData(this);

    fetch('/cadastro', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // Verifica o tipo de usuário para definir a mensagem
            const tipoUsuario = formData.get('tipo_usuario');
            if (tipoUsuario === 'psicologo') {
                showPopup('Cadastro realizado! Aguarde até que seja aprovado pelo administrador.');
            } else {
                showPopup('Cadastro realizado com sucesso! Redirecionando para login...');
                setTimeout(function() {
                    window.location.href = '/login';
                }, 3000);  // Redireciona após 3 segundos
            }
        } else {
            // Erro no cadastro
            showPopup('Erro: ' + data.error);
        }
    })
    .catch(error => {
        showPopup('Ocorreu um erro inesperado. Tente novamente.');
    });
};
