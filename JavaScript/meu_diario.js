const entrada = document.getElementById('entrada');
const texto = document.getElementById('texto');

texto.focus();
texto.selectionStart = 0;



texto.addEventListener('input', () => {
	entrada.innerHTML = texto.value;
});

document.getElementById("sec_diario").addEventListener("submit", function (event) {
	event.preventDefault();

	const form = event.target;
	const formData = new FormData(form);

	const DiarioData = {};
	formData.forEach((value, key) => {
		DiarioData[key] = value;
	});

	fetch('https://66577c2c5c3617052644fefa.mockapi.io/apiv1/users/1/text_diario', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
	   },
	   body: JSON.stringify(DiarioData),
   })
		.then(response => {
		   if (!response.ok) {
				throw new Error('Erro ao salvar :(');
		   }
			alert('Salvo com sucesso! :)');
			form.reset();
		})
	   .catch(error => {
		console.error('Erro:', error);
		alert('Erro ao salvar. Por favor, tente novamente.');
	});
});