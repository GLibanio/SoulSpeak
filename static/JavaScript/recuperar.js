document.getElementById("form_recuperar").addEventListener("submit", function(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const respostaSeguranca = document.getElementById("resposta_seguranca").value;

    fetch('/recuperar_senha', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ email: email, resposta_seguranca: respostaSeguranca }),
    })
    .then(response => {
        if (response.ok) {
            window.location.href = response.url;  // Redireciona se for bem-sucedido
        } else {
            return response.text();
        }
    })
    .then(data => {
        if (data) alert(data);  // Mostra a mensagem de erro, se houver
    })
    .catch(error => alert('Erro ao tentar recuperar senha.'));
});
