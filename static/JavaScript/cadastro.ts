interface Pessoa {
    id: number;
    nome: string;
    email: string;
    senha: string;
}

const element = document.getElementById("Pessoa-form");
if (element) {
    element.addEventListener("submit", function(event: Event) {
        event.preventDefault();

        const form = event.target as HTMLFormElement;
        const formData = new FormData(form);
        const formDataObject = Object.fromEntries(formData.entries());
        const pessoaData: Pessoa = formDataObject as unknown as Pessoa;
        
    
        fetch('https://66577c2c5c3617052644fefa.mockapi.io/apiv1/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pessoaData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao cadastrar o usuário');
            }
            alert('Usuário cadastrado com sucesso!');
            window.location.href = 'login.html';
            form.reset();
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao cadastrar o usuário. Por favor, tente novamente.');
        });
    });
}
