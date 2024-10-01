from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches

app = Flask(__name__)

# Base de conhecimento em português
knowledge_base = {
    "questions": [
        {"question": "Ola", 
         "answer": "Olá! Como posso te ajudar?"},
        {"question": "Como posso lidar com a incerteza sobre meu futuro?", 
         "answer": "Lidar com a incerteza pode ser difícil, mas focar no presente e em ações que você pode controlar é um bom começo."},
        {"question": "E se eu nunca encontrar uma carreira que me faça feliz?", 
         "answer": "É normal ter essas preocupações. Experimente explorar diferentes áreas e interesses para descobrir o que realmente te faz feliz."},
        {"question": "Como posso parar de me comparar com outras pessoas da minha idade?", 
         "answer": "Lembre-se de que cada pessoa tem seu próprio ritmo. Foque em seu crescimento pessoal e nas suas conquistas."},
        {"question": "O que eu faço quando sinto que estou ficando para trás na vida?", 
         "answer": "É importante lembrar que o sucesso não é uma corrida. Defina seus próprios objetivos e siga no seu ritmo."},
        {"question": "Como posso lidar com a pressão da minha família sobre meu futuro?", 
         "answer": "Converse abertamente com sua família sobre seus sentimentos e tente encontrar um meio-termo entre suas expectativas e as deles."},
        {"question": "Como faço para aceitar que não tenho tudo planejado ainda?", 
         "answer": "Aceitar a incerteza faz parte do crescimento. Concentre-se em dar pequenos passos em direção aos seus objetivos."},
        {"question": "Será que minhas decisões erradas agora vão arruinar meu futuro?", 
         "answer": "Erros fazem parte do aprendizado. Use-os como oportunidades para crescer e evoluir."},
        {"question": "É normal sentir que tudo é muito incerto e fora de controle?", 
         "answer": "Sim, é completamente normal. Foque nas áreas da sua vida onde você pode fazer mudanças e evoluir."},
        {"question": "Como posso lidar com a ansiedade de não saber se vou conseguir um emprego depois de me formar?", 
         "answer": "Tente planejar pequenas etapas, como estágios ou desenvolvimento de habilidades, para aumentar suas chances de sucesso."},
        {"question": "Existe alguma técnica rápida para reduzir minha ansiedade quando penso no futuro?", 
         "answer": "Tente técnicas de respiração profunda, meditação ou dar uma caminhada para reduzir a ansiedade."},
        {"question": "Como posso encontrar algo que me motive, mesmo quando estou desanimado?", 
         "answer": "Procure atividades que você goste ou que te desafiem. Conectar-se com outras pessoas também pode ajudar."},
        {"question": "E se eu nunca atingir os objetivos que eu esperava para minha vida?", 
         "answer": "Objetivos podem mudar ao longo do tempo. Reavalie o que é importante para você e ajuste suas expectativas de acordo."},
        {"question": "Como posso ter esperança em um mundo tão incerto?", 
         "answer": "Encontre pequenas razões para ser grato e focar no que você pode controlar. Isso ajuda a construir esperança aos poucos."},
        {"question": "O que posso fazer para me sentir mais no controle do meu futuro?", 
         "answer": "Defina metas alcançáveis e estabeleça um plano de ação para cada uma. Pequenas vitórias aumentam a sensação de controle."},
        {"question": "Como eu posso saber se estou no caminho certo?", 
         "answer": "Avalie regularmente seus objetivos e veja se estão alinhados com seus valores e sonhos. Ajustes são normais no percurso."},
        {"question": "Estou muito estressado.",
         "answer": "Entendo. O estresse pode ser desgastante. O que tem te deixado mais sobrecarregado ultimamente?"},
        {"question": "Sinto que estou sempre triste.",
         "answer": "Sinto muito por você estar passando por isso. Você gostaria de compartilhar mais sobre o que tem causado essa tristeza?"},
        {"question": "Não estou conseguindo dormir bem.",
         "answer": "Dormir mal pode afetar muito nosso bem-estar. Tem algo específico que está te impedindo de descansar?"},
        {"question": "Estou tendo problemas com meus amigos.",
         "answer": "É normal enfrentar desafios em relacionamentos. O que exatamente está acontecendo?"},
        {"question": "Não me sinto bem comigo mesmo.",
         "answer": "Muitos passam por isso em algum momento. O que te faz sentir assim?"},
        {"question": "Estou sem motivação para fazer as coisas.",
         "answer": "É difícil quando a motivação some. Tem algo que costumava te animar que você poderia tentar novamente?"},
        {"question": "Me sinto muito sozinho.",
         "answer": "Sentir solidão pode ser doloroso. Você gostaria de falar sobre isso ou talvez buscar formas de se conectar com os outros?"},
        {"question": "Estou me sentindo ansioso.",
         "answer": "A ansiedade pode ser difícil de lidar. O que você acha que está causando essa ansiedade?"},
        {"question": "Não consigo me concentrar.",
         "answer": "A falta de concentração pode ser frustrante. Tem algo específico que está te distraindo?"},
        {"question": "Sinto que não tenho apoio.",
         "answer": "É importante se sentir apoiado. Você gostaria de explorar maneiras de encontrar suporte?"},
        {"question": "Estou me sentindo sobrecarregado.",
         "answer": "Entendo, isso pode ser muito difícil. Quais são as principais coisas que estão te sobrecarregando agora?"},
        {"question": "Sinto raiva frequentemente.",
         "answer": "A raiva é uma emoção normal, mas pode ser intensa. O que costuma te deixar assim?"},
        {"question": "Não sei como lidar com meus sentimentos.",
         "answer": "É normal se sentir perdido às vezes. Que tipo de sentimentos você está enfrentando?"},
        {"question": "Estou preocupado com o futuro.",
         "answer": "Preocupações sobre o futuro podem ser angustiante. O que especificamente te preocupa?"},
        {"question": "Sinto que ninguém me entende.",
         "answer": "Isso pode ser muito solitário. Você gostaria de compartilhar mais sobre como se sente?"},
        {"question": "Estou tendo dificuldades no trabalho.",
         "answer": "Isso pode ser desafiador. O que está acontecendo no trabalho que tem te preocupado?"},
        {"question": "Estou lidando com uma perda.",
         "answer": "Sinto muito pela sua perda. Você gostaria de falar sobre isso ou sobre como se sente?"},
        {"question": "Sinto que estou estagnado.",
         "answer": "É comum sentir-se assim às vezes. O que você gostaria de mudar em sua vida?"},
        {"question": "Me sinto culpado por tudo.",
         "answer": "Sentir culpa pode ser pesado. O que está te fazendo sentir assim?"},
        {"question": "Estou tendo dificuldades para lidar com mudanças.",
         "answer": "Mudanças podem ser desafiadoras e assustadoras. O que especificamente está te incomodando nessas mudanças?"}
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
