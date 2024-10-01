

// class login extends Usuario {

//     constructor(email, senha) {
//         this.email = email;
//         this.senha = senha;
//       }

// autenticar() {
      
const API_URL = 'https://66577c2c5c3617052644fefa.mockapi.io/apiv1/users';

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

//       }
// }