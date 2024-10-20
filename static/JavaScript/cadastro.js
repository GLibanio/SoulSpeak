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
    document.getElementById('terms').disabled = false; // Habilita a checkbox
    document.getElementById('popup').style.display = "none"; // Fecha o popup
}

// Verifica se a checkbox de termos está marcada e habilita o botão de envio
document.getElementById('terms').addEventListener('change', function() {
    var submitButton = document.getElementById('submit_button');
    if (this.checked) {
        submitButton.disabled = false; // Habilita o botão de envio
    } else {
        submitButton.disabled = true; // Desabilita o botão se desmarcar
    }
});

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
            // Cadastro bem-sucedido
            showPopup('Cadastro realizado com sucesso! Redirecionando para login...');
            setTimeout(function() {
                window.location.href = '/login';
            }, 3000);  // Redireciona após 3 segundos
        } else {
            // Erro no cadastro
            showPopup('Erro: ' + data.error);
        }
    })
    .catch(error => {
        showPopup('Ocorreu um erro inesperado. Tente novamente.');
    });
};
