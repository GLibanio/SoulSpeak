from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches

app = Flask(__name__)

# Base de conhecimento em português
knowledge_base = {
    "questions": [
        {"question": "Ola", 
        "answer": "Olá! Como posso te ajudar?"},   
    ]
}

def find_best_match(user_question, questions):
    # Use get_close_matches para encontrar a melhor correspondência
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

@app.route('/')
def base():
    return render_template('home.html')

@app.route('/ed_emocional')
def ed_emocional():
    return render_template('ed_emocional.html')

@app.route('/alimentacao')
def alimentacao():
    return render_template('alimentacao.html')

@app.route('/autocuidado')
def autocuidado():
    return render_template('autocuidado.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/Exercicio')
def Exercicio():
    return render_template('Exercicio.html')

@app.route('/Hidratar')
def Hidratar():
    return render_template('Hidratar.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/indicacoes')
def indicacoes():
    return render_template('indicacoes.html')

@app.route('/inter_social')
def inter_social():
    return render_template('inter_social.html')

@app.route('/livros')
def livros():
    return render_template('livros.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/meu_diario')
def meu_diario():
    return render_template('meu_diario.html')
    

@app.route('/podcasts')
def podcasts():
    return render_template('podcasts.html')

@app.route('/pontos')
def pontos():
    return render_template('pontos.html')

@app.route('/popup')
def popup():
    return render_template('popup.html')

@app.route('/sono')
def sono():
    return render_template('sono.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    # Captura a entrada do usuário
    user_input = request.json['message']
    
    # Encontre a melhor correspondência na base de perguntas
    best_match = find_best_match(user_input.lower(), [q["question"].lower() for q in knowledge_base["questions"]])
    
    print(f"Entrada do usuário: {user_input}")
    print(f"Melhor correspondência: {best_match}")
    
    if best_match:
        # Se encontrar a correspondência, retornar a resposta correspondente
        for q in knowledge_base["questions"]:
            if q["question"].lower() == best_match:
                response = q["answer"]
                break
    else:
        # Resposta padrão caso não haja correspondência
        response = "Desculpe, eu não sei a resposta."
    
    print(f"Resposta: {response}")

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)
