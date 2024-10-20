from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
from difflib import get_close_matches
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  # Import para hash de senha
import re  # Para validar email e CPF
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

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

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_cpf(cpf):
    return re.match(r"^\d{11}$", cpf)


def connect_db():
    conectar = sqlite3.connect('user.db')
    return conectar

def criar_tabela_login():
    conectar = connect_db()
    cursor = conectar.cursor()

    # Excluindo a tabela existente e recriando com os novos campos
    cursor.execute('DROP TABLE IF EXISTS usuarios')

    # Criando a tabela unificada para usuários e psicólogos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nasc DATE NOT NULL,
            nickname TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL -- Novo campo para distinguir entre "usuario" e "psicologo"
        );
    ''')
    
    conectar.commit()
    conectar.close()

def criar_tabela_pontos():
    conectar = connect_db()
    cursor = conectar.cursor()

    # Criando a tabela de pontos associada ao usuário
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS pontos_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            saldo_pontos INTEGER DEFAULT 0,  -- Saldo de pontos do usuário
            ultimo_ganho TIMESTAMP,           -- Campo para armazenar a última vez que ganhou pontos
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios(id) -- Chave estrangeira para usuários
        );
    ''')

    conectar.commit()
    conectar.close()
    
def adicionar_pontos_se_necessario(user_id):
    conectar = connect_db()
    cursor = conectar.cursor()

    cursor.execute('SELECT ultimo_ganho, saldo_pontos FROM pontos_usuario WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        ultimo_ganho, saldo_pontos = result
        print(f"Último ganho: {ultimo_ganho}, Saldo atual: {saldo_pontos}")  # Para depuração
        if ultimo_ganho is None or (datetime.now() - datetime.fromisoformat(ultimo_ganho)).total_seconds() >= 300:
            novo_saldo = saldo_pontos + 5
            cursor.execute('UPDATE pontos_usuario SET saldo_pontos = ?, ultimo_ganho = ? WHERE user_id = ?', 
                           (novo_saldo, datetime.now(), user_id))
            conectar.commit()
            print(f"Novos pontos adicionados. Saldo atualizado: {novo_saldo}")  # Para depuração
    else:
        print("Usuário não encontrado.")  # Para depuração

    conectar.close()



def criar_tabela_chat():
    conectar = connect_db()
    cursor = conectar.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mensagem TEXT NOT NULL,
            resposta TEXT NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conectar.commit()
    conectar.close()

# Função para inserir mensagens e respostas no chat temporário
def inserir_mensagem(mensagem, resposta):
    conectar = connect_db()
    cursor = conectar.cursor()
    
    cursor.execute('''
        INSERT INTO chat_usuario (mensagem, resposta)
        VALUES (?, ?)
    ''', (mensagem, resposta))
    
    conectar.commit()
    conectar.close()

# Função para apagar as mensagens após 24 horas
def apagar_mensagens_anteriores():
    conectar = connect_db()
    cursor = conectar.cursor()
    
    # Calcular a data limite (24 horas atrás)
    limite = datetime.now() - timedelta(hours=24)
    
    cursor.execute('''
        DELETE FROM chat_usuario
        WHERE data_hora < ?
    ''', (limite,))
    
    conectar.commit()
    conectar.close()



@app.route('/')
def base():
    return render_template('index.html')

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
    if "user_id" in session:
        user_id = session['user_id']
        adicionar_pontos_se_necessario(user_id)  # Aqui

        conectar = connect_db()
        cursor = conectar.cursor()

        cursor.execute('SELECT nickname FROM usuarios WHERE id = ?', (user_id,))
        nickname = cursor.fetchone()

        if nickname is None:
            return "Usuário não encontrado", 404

        nickname = nickname[0]
        cursor.execute('SELECT saldo_pontos FROM pontos_usuario WHERE user_id = ?', (user_id,))
        saldo_pontos_row = cursor.fetchone()

        saldo_pontos = saldo_pontos_row[0] if saldo_pontos_row else 0
        conectar.close()

        return render_template('pontos.html', nickname=nickname, saldo_pontos=saldo_pontos)
    else:
        return jsonify({"success": False, "message": "Usuário não logado."})
    
@app.route('/popup')
def popup():
    return render_template('popup.html')

@app.route('/sono')
def sono():
    return render_template('sono.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

# Função para encontrar a melhor correspondência com base na similaridade
def find_best_match(user_input, possible_questions):
    # Usa a função get_close_matches do difflib para encontrar a correspondência mais próxima
    matches = get_close_matches(user_input, possible_questions, n=1, cutoff=0.6)  # n=1 retorna a melhor correspondência
    if matches:
        return matches[0]
    return None

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

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            cpf = request.form['cpf']
            data_nasc = request.form['data_nasc']
            nickname = request.form['nickname']
            email = request.form['email']
            senha = request.form['senha']
            tipo_usuario = request.form['tipo_usuario']

            # Hash da senha
            hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')

            conectar = connect_db()
            cursor = conectar.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, cpf, data_nasc, nickname, email, senha, tipo_usuario)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, cpf, data_nasc, nickname, email, hashed_senha, tipo_usuario))

            conectar.commit()
            conectar.close()

            return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template('cadastro.html')  # Renderiza o formulário se for um GET

# Função de login com verificação segura de senha
@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        email = request.form['email']
        senha = request.form['senha']

        conectar = connect_db()
        cursor = conectar.cursor()

        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        conectar.close()

        if user and bcrypt.check_password_hash(user[6], senha):  # Verifica a senha
            session['user_id'] = user[0]  # Armazenando o user_id na sessão
            tipo_usuario = user[7]
            if tipo_usuario == 'psicologo':
                return 'Você entrou como psicólogo!', 200
            else:
                return 'Você entrou como usuário!', 200
        else:
            return 'Usuário ou senha incorretos!', 401
    except Exception as e:
        return str(e), 400


def alterar_tabela_pontos():
    conectar = connect_db()
    cursor = conectar.cursor()
    
    try:
        # Tenta adicionar a coluna 'ultimo_ganho' se não existir
        cursor.execute('ALTER TABLE pontos_usuario ADD COLUMN ultimo_ganho TIMESTAMP')
    except sqlite3.OperationalError as e:
        # Se a tabela já tiver a coluna, apenas imprime a mensagem de erro
        print(f"Erro ao alterar a tabela: {e}")
    
    conectar.commit()
    conectar.close()

@app.route('/pontos/status', methods=['GET'])
def status_pontos():
    if "user_id" in session:
        user_id = session['user_id']
        conectar = connect_db()
        cursor = conectar.cursor()
        cursor.execute('SELECT saldo_pontos FROM pontos_usuario WHERE user_id = ?', (user_id,))
        saldo_pontos_row = cursor.fetchone()
        saldo_pontos = saldo_pontos_row[0] if saldo_pontos_row else 0
        conectar.close()
        print(f"Saldo de pontos para o usuário {user_id}: {saldo_pontos}")  # Debugging
        return jsonify({"saldo_pontos": saldo_pontos})
    else:
        return jsonify({"success": False, "message": "Usuário não logado."}), 401
    
if __name__ == '__main__':
    # Exclua o arquivo user.db antes de executar para garantir que as tabelas sejam criadas novamente
    criar_tabela_login()
    criar_tabela_chat()
    criar_tabela_pontos()
    
    # Chama a função para alterar a tabela de pontos
    alterar_tabela_pontos()
    
    conectar = connect_db()
    cursor = conectar.cursor()
    cursor.execute('SELECT id FROM usuarios')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        adicionar_pontos_se_necessario(usuario[0])
    conectar.close()
    
    apagar_mensagens_anteriores()
    app.run(debug=True)