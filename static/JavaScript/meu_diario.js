function typeWriter(text, element, speed = 50) {
    let i = 0;
    element.innerHTML = "";

    function typing() {
      if (i < text.length) {
        element.innerHTML += text.charAt(i);
        i++;
        setTimeout(typing, speed);
      }
    }
    typing();
  }

  function sendMessage() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const userMessage = userInput.value;

    if (userMessage.trim() === "") {
      return;
    }

    const userMessageElement = document.createElement("div");
    userMessageElement.textContent = "Você: " + userMessage;
    userMessageElement.classList.add("user-message");
    chatBox.appendChild(userMessageElement);

    userInput.value = "";

    const typingElement = document.createElement("div");
    typingElement.textContent = "Bot está digitando...";
    typingElement.classList.add("typing-message");
    chatBox.appendChild(typingElement);

    chatBox.scrollTop = chatBox.scrollHeight;

    setTimeout(() => {
      fetch("/get_response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      })
        .then((response) => response.json())
        .then((data) => {
          chatBox.removeChild(typingElement);

          const botMessageElement = document.createElement("div");
          botMessageElement.classList.add("bot-message");
          chatBox.appendChild(botMessageElement);

          typeWriter(data.response, botMessageElement);

          chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch((error) => {
          console.error("Erro:", error);

          chatBox.removeChild(typingElement);

          const botMessageElement = document.createElement("div");
          botMessageElement.textContent = "Bot: Desculpe, ocorreu um erro ao processar sua mensagem.";
          botMessageElement.classList.add("bot-message");
          chatBox.appendChild(botMessageElement);
        });
    }, 2000);
  }

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
  if (!notes) return;
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
                                  <li onclick="saveNoteAsPDF(${id})"><i class="uil uil-save"></i>Salvar</li>
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


function saveNoteAsPDF(id) {
  const note = notes[id];
  const pdfContent = `
      <h1>${note.title}</h1>
      <p>${note.description.replaceAll("\n", "<br/>")}</p>
      <p><em>Data: ${note.date}</em></p>
  `;

  const pdfWindow = window.open("", "_blank");
  pdfWindow.document.write(`
      <html>
          <head>
              <title>${note.title}</title>
          </head>
          <body>
              ${pdfContent}
          </body>
      </html>
  `);
  pdfWindow.document.close();
  pdfWindow.print();  // Abre a caixa de diálogo para salvar em PDF
}
