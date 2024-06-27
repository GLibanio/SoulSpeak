// const entrada = document.getElementById('entrada');
// const texto = document.getElementById('texto');

// texto.focus();
// texto.selectionStart = 0;



// texto.addEventListener('input', () => {
// 	entrada.innerHTML = texto.value;
// });

// document.getElementById("sec_diario").addEventListener("submit", function (event) {
// 	event.preventDefault();

// 	const form = event.target;
// 	const formData = new FormData(form);

// 	const DiarioData = {};
// 	formData.forEach((value, key) => {
// 		DiarioData[key] = value;
// 	});

// 	fetch('https://66577c2c5c3617052644fefa.mockapi.io/apiv1/users/1/text_diario', {
// 		method: 'POST',
// 		headers: {
// 			'Content-Type': 'application/json',
// 	   },
// 	   body: JSON.stringify(DiarioData),
//    })
// 		.then(response => {
// 		   if (!response.ok) {
// 				throw new Error('Erro ao salvar :(');
// 		   }
// 			alert('Salvo com sucesso! :)');
// 			form.reset();
// 		})
// 	   .catch(error => {
// 		console.error('Erro:', error);
// 		alert('Erro ao salvar. Por favor, tente novamente.');
// 	});
// });

const addBox = document.querySelector(".add-box"),
popupBox = document.querySelector(".popup-box"),
popupTitle = popupBox.querySelector(".header_popup p"),
closeIcon = popupBox.querySelector(".header_popup i"),
titleTag = popupBox.querySelector("input"),
descTag = popupBox.querySelector("textarea"),
addBtn = popupBox.querySelector("button");

const months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
              "Agosto", "Setembro", "Outubro", "Novembro", "Decembro"];
const notes = JSON.parse(localStorage.getItem("notes") || "[]");
let isUpdate = false, updateId;

addBox.addEventListener("click", () => {
    popupTitle.innerText = "Descreva como você está agora";
    addBtn.innerText = "Salvar";
    popupBox.classList.add("show");
    document.querySelector("body").style.overflow = "hidden";
    if(window.innerWidth > 660) titleTag.focus();
});

closeIcon.addEventListener("click", () => {
    isUpdate = false;
    titleTag.value = descTag.value = "";
    popupBox.classList.remove("show");
    document.querySelector("body").style.overflow = "auto";
});

function showNotes() {
    if(!notes) return;
    document.querySelectorAll(".note").forEach(li => li.remove());
    notes.forEach((note, id) => {
        let filterDesc = note.description.replaceAll("\n", '<br/>');
        let liTag = `<div class="note_set">
					 <li class="note">
                        <div class="details">
                            <p>${note.title}</p>
                            <span>${filterDesc}</span>
                        </div>
                        <div class="bottom-content">
                            <span>${note.date}</span>
                            <div class="settings">
                                <i onclick="showMenu(this)" class="uil uil-ellipsis-h"></i>
                                <ul class="menu">
                                    <li onclick="updateNote(${id}, '${note.title}', '${filterDesc}')"><i class="uil uil-pen"></i>Editar</li>
                                    <li onclick="deleteNote(${id})"><i class="uil uil-trash"></i>Deletar</li>
                                </ul>
                            </div>
                        </div>
                    </li>
					</div>`;
        addBox.insertAdjacentHTML("afterend", liTag);
    });
}
showNotes();

function showMenu(elem) {
    elem.parentElement.classList.add("show");
    document.addEventListener("click", e => {
        if(e.target.tagName != "I" || e.target != elem) {
            elem.parentElement.classList.remove("show");
        }
    });
}

function deleteNote(noteId) {
    let confirmDel = confirm("Tem certeza que quer deletar?");
    if(!confirmDel) return;
    notes.splice(noteId, 1);
    localStorage.setItem("notes", JSON.stringify(notes));
    showNotes();
}

function updateNote(noteId, title, filterDesc) {
    let description = filterDesc.replaceAll('<br/>', '\r\n');
    updateId = noteId;
    isUpdate = true;
    addBox.click();
    titleTag.value = title;
    descTag.value = description;
    popupTitle.innerText = "Update a Note";
    addBtn.innerText = "Update Note";
}

addBtn.addEventListener("click", e => {
    e.preventDefault();
    let title = titleTag.value.trim(),
    description = descTag.value.trim();

    if(title || description) {
        let currentDate = new Date(),
        month = months[currentDate.getMonth()],
        day = currentDate.getDate(),
        year = currentDate.getFullYear();

        let noteInfo = {title, description, date: `${day} de ${month}, ${year}`}
        if(!isUpdate) {
            notes.push(noteInfo);
        } else {
            isUpdate = false;
            notes[updateId] = noteInfo;
        }
        localStorage.setItem("notes", JSON.stringify(notes));
        showNotes();
        closeIcon.click();
    }
});