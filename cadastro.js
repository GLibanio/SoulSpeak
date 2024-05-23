document.getElementById("Pessoa-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const PessoaData = {};
    formData.forEach((value, key) => {
        PessoaData[key] = value;
    });

    fetch('#', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(PessoaData),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao cadastrar o usuario');
            }
            alert('usuario cadastrado com sucesso!');
            window.location.href = 'login.html';
            form.reset();
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao cadastrar o usuario. Por favor, tente novamente.');
        });
});