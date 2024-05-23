// metodo login
const API_URL = '#';

async function login(email, senha) {
    try {
        const response = await fetch(`${API_URL}?email=${email}`);
        const usuario = await response.json();

        if (usuario.length > 0) {
            const user = usuario[0];
            if (user.senha === senha) {
                localStorage.setItem('userEmail', email);
                window.location.href = 'home.html';
            } else {
                alert('Usuário ou senha inválidos');
            }
        } else {
            alert('Usuário não encontrado');
        }
    } catch (error) {
        console.error('Erro ao tentar logar:', error);
    }
}

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;
    login(email, senha);
});

