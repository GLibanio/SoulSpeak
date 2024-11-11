document.getElementById("form_redefinir").addEventListener("submit", function(event) {
    event.preventDefault();

    const novaSenha = document.getElementById("nova_senha").value;
    const email = new URLSearchParams(window.location.search).get('email');  // Extrai o e-mail da URL

    // Verifica se o e-mail foi capturado da URL
    if (!email) {
        alert('Erro: E-mail não encontrado na URL');
        return;
    }

    // Preenche o campo oculto com o e-mail
    document.getElementById("email_hidden").value = email;

    fetch(`/resetar_senha`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ nova_senha: novaSenha, email: email }),  // Inclui o e-mail no corpo da requisição
    })
    .then(response => {
        if (response.ok) {
            return response.text().then(data => {
                alert(data);  // Mensagem de sucesso ou erro
                if (data === 'Senha redefinida com sucesso!') {
                    window.location.href = '/login';  // Redireciona para a página de login
                }
            });
        } else {
            return response.text().then(data => alert(data));
        }
    })
    .catch(error => alert('Erro ao tentar redefinir a senha.'));
});

