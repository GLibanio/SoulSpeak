const entrada = document.getElementById('entrada');
const texto = document.getElementById('texto');

entrada.focus();
entrada.selectionStart = 0;



entrada.addEventListener('input', () => {
	texto.innerHTML = entrada.value;
});

