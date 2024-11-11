from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from difflib import get_close_matches
import difflib
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash  # Import para hash de senha
import re  # Para validar email e CPF
from flask_bcrypt import Bcrypt
import os
import json
import unidecode
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

usuarios_espera = []
usuarios_atendimento = {}
mensagens_chat = {}

s = URLSafeTimedSerializer(app.secret_key)

# Base de conhecimento em português
with open('knowledge_base.json', 'r', encoding='utf-8') as file:
    knowledge_base = json.load(file)

# Agora você pode acessar as perguntas e respostas
questions = knowledge_base["questions"]

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_cpf(cpf):
    return re.match(r"^\d{11}$", cpf)


def connect_db():
    conectar = sqlite3.connect('user.db')
    return conectar

    
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
    
#TABELAS

def criar_tabela_login():
    conectar = connect_db()
    cursor = conectar.cursor()

    # Cria a nova tabela com os campos adicionais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nasc DATE NOT NULL,
            nickname TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL,  -- Distinção entre "usuario" e "psicologo"
            pergunta_seguranca TEXT,     -- Pergunta de segurança
            resposta_seguranca TEXT      -- Resposta de segurança
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
    
def criar_tabela_admin():
    conectar = connect_db()
    cursor = conectar.cursor()
    
    # Cria a tabela de administrador, se ainda não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Verifica se já existe um admin com o email especificado
    cursor.execute("SELECT * FROM admin WHERE email = ?", ('admin@admin.com',))
    admin_existente = cursor.fetchone()
    
    # Insere o admin padrão se ele não existir
    if not admin_existente:
        nome_admin = "Admin"
        email_admin = "admin@admin.com"
        senha_admin = "123"
        
        # Criptografa a senha antes de armazená-la
        senha_hash = bcrypt.generate_password_hash(senha_admin).decode('utf-8')
        
        cursor.execute('''
            INSERT INTO admin (nome, email, senha)
            VALUES (?, ?, ?)
        ''', (nome_admin, email_admin, senha_hash))
    
    conectar.commit()
    conectar.close()

def criar_tabela_diario():
    conectar = connect_db()
    cursor = conectar.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            texto_diario TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES usuarios(id)
        );
    ''')
    
    conectar.commit()
    conectar.close()

def criar_tabela_analise_psicologo():
    conectar = connect_db()
    cursor = conectar.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analise_psicologo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nasc DATE NOT NULL,
            nickname TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL,
            pergunta_seguranca TEXT,
            resposta_seguranca TEXT,
            status TEXT DEFAULT 'pendente'
        );
    ''')
    
    conectar.commit()
    conectar.close()
    
def criar_tabela_psicologos_aceitos():
    conectar = connect_db()
    cursor = conectar.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS psicologos_aceitos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            data_nasc DATE NOT NULL,
            nickname TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            tipo_usuario TEXT NOT NULL,     -- Coluna adicionada para tipo de usuário
            pergunta_seguranca TEXT,        -- Pergunta de segurança
            resposta_seguranca TEXT         -- Resposta de segurança
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


 #ROTAS
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def base():
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    conectar = connect_db()
    cursor = conectar.cursor()
    # Busca psicólogos pendentes
    cursor.execute("SELECT * FROM analise_psicologo WHERE status = 'pendente'")
    psicologos_pendentes = cursor.fetchall()
    conectar.close()
    # Renderiza a página com os psicólogos pendentes
    return render_template('admin.html', psicologos=psicologos_pendentes)


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
        adicionar_pontos_se_necessario(user_id)

        conectar = connect_db()
        cursor = conectar.cursor()

        cursor.execute('SELECT nickname FROM usuarios WHERE id = ?', (user_id,))
        nickname = cursor.fetchone()

        if nickname is None:
            return render_template('404.html'), 404

        nickname = nickname[0]
        cursor.execute('SELECT saldo_pontos FROM pontos_usuario WHERE user_id = ?', (user_id,))
        saldo_pontos_row = cursor.fetchone()

        saldo_pontos = saldo_pontos_row[0] if saldo_pontos_row else 0
        conectar.close()

        return render_template('pontos.html', nickname=nickname, saldo_pontos=saldo_pontos)
    else:
        return render_template('login_necessario.html'), 401
    
@app.route('/popup')
def popup():
    return render_template('popup.html')

@app.route('/psicologo')
def psico():
    return render_template('psico_comunicacao.html')

@app.route('/sono')
def sono():
    return render_template('sono.html')

@app.route('/videos')
def videos():
    return render_template('videos.html')

#Conversa

@app.route('/conversa_psicologo')
def conversa_psico():
    return render_template('conversa_psicologo.html')

@app.route('/entrar_espera', methods=['POST'])
def entrar_espera():
    usuario = request.json.get('usuario')
    if usuario not in usuarios_espera:
        usuarios_espera.append(usuario)
    return jsonify({"message": "Usuário adicionado à espera"}), 200

# Endpoint para listar os usuários em espera
@app.route('/listar_espera')
def listar_espera():
    return jsonify({"usuarios": usuarios_espera})

# Endpoint para puxar o usuário da lista de espera para o atendimento
@app.route('/puxar_usuario', methods=['POST'])
def puxar_usuario():
    usuario = request.json.get('usuario')
    if usuario in usuarios_espera:
        usuarios_espera.remove(usuario)
        usuarios_atendimento[usuario] = True
        mensagens_chat[usuario] = []
    return jsonify({"message": "Usuário puxado para atendimento"}), 200

# Endpoint para verificar o status do usuário (espera/atendimento)
@app.route('/verificar_status', methods=['POST'])
def verificar_status():
    usuario = request.json.get('usuario')
    status = 'em atendimento' if usuarios_atendimento.get(usuario) else 'em espera'
    return jsonify({"status": status})

# Endpoint para enviar e receber mensagens no chat
@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    usuario = request.json.get('usuario')
    message = request.json.get('message')
    if usuario in usuarios_atendimento:
        mensagens_chat[usuario].append({"sender": "Paciente", "message": message})
        # Resposta simulada do psicólogo
        resposta = f"Resposta automática do Psicólogo para: {message}"
        mensagens_chat[usuario].append({"sender": "Psicólogo", "message": resposta})
        return jsonify({"resposta": resposta}), 200
    return jsonify({"error": "Usuário não está em atendimento"}), 400

#CHATBOT

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unidecode.unidecode(texto)
    return texto

# Função para correção ortográfica
def corrigir_ortografia(texto):
    return str(TextBlob(texto).correct())

def find_best_match(user_input, questions):
    # Normaliza e corrige a entrada do usuário
    user_input = corrigir_ortografia(normalizar_texto(user_input))
    
    # Normaliza as perguntas na base de conhecimento
    normalized_questions = [normalizar_texto(q["question"]) for q in questions]
    
    # Encontra a pergunta mais semelhante
    matches = difflib.get_close_matches(user_input, normalized_questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

@app.route('/get_response', methods=['POST'])
def get_response():
    # Captura e processa a entrada do usuário
    user_input = request.json['message']
    user_input = normalizar_texto(corrigir_ortografia(user_input))
    
    # Encontre a melhor correspondência na base de perguntas
    best_match = find_best_match(user_input, questions)
    
    if best_match:
        # Retorna a resposta correspondente
        for q in knowledge_base["questions"]:
            if normalizar_texto(q["question"]) == best_match:
                response = q["answer"]
                break
    else:
        # Resposta padrão caso não haja correspondência
        response = "Desculpe, eu não sei a resposta."
    
    return jsonify({"response": response})

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    if request.method == 'POST':
        try:
            # Recebendo os dados do formulário
            nome = request.form['nome']
            cpf = request.form['cpf']
            data_nasc = request.form['data_nasc']
            nickname = request.form['nickname']
            email = request.form['email']
            senha = request.form['senha']
            tipo_usuario = request.form['tipo_usuario']
            pergunta_seguranca = request.form['pergunta_seguranca']
            resposta_seguranca = request.form['resposta_seguranca'].strip().lower()  # Normaliza sem hash

            # Hash da senha para maior segurança
            hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')

            conectar = connect_db()
            cursor = conectar.cursor()

            # Verificar se o e-mail já está cadastrado
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                return jsonify({'error': 'Este e-mail já está cadastrado.'}), 400

            # Inserir na tabela de análise se for psicólogo
            if tipo_usuario == 'psicologo':
                cursor.execute('''
                    INSERT INTO analise_psicologo (nome, cpf, data_nasc, nickname, email, senha, tipo_usuario, pergunta_seguranca, resposta_seguranca, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendente')
                ''', (nome, cpf, data_nasc, nickname, email, hashed_senha, tipo_usuario, pergunta_seguranca, resposta_seguranca))
            else:
                cursor.execute('''
                    INSERT INTO usuarios (nome, cpf, data_nasc, nickname, email, senha, tipo_usuario, pergunta_seguranca, resposta_seguranca)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (nome, cpf, data_nasc, nickname, email, hashed_senha, tipo_usuario, pergunta_seguranca, resposta_seguranca))

            conectar.commit()
            conectar.close()
            
            return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
        except Exception as e:
            return jsonify({'error': f'Erro ao cadastrar usuário: {str(e)}'}), 500
        
        
@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if not email or not senha:
            return jsonify({'error': 'Por favor, forneça um email e senha.'}), 400

        conectar = connect_db()
        cursor = conectar.cursor()

        # Verifica se o login é de um administrador
        cursor.execute('SELECT * FROM admin WHERE email = ?', (email,))
        admin = cursor.fetchone()

        if admin:
            # Se o usuário é administrador, verifica a senha
            stored_password_hash = admin[3]  # Coluna de senha na tabela admin
            if bcrypt.check_password_hash(stored_password_hash, senha):
                session['user_id'] = admin[0]
                session['tipo_usuario'] = 'admin'
                return jsonify({'success': True, 'tipo_usuario': 'admin'}), 200
            else:
                return jsonify({'error': 'Usuário ou senha incorretos!'}), 401

        # Verifica se o usuário está na tabela 'usuarios'
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if not user:
            # Se o usuário não está em 'usuarios', tenta buscar em 'psicologos_aceitos'
            cursor.execute('SELECT * FROM psicologos_aceitos WHERE email = ?', (email,))
            user = cursor.fetchone()
            is_psicologo = True if user else False
        else:
            is_psicologo = False

        conectar.close()

        # Verifica a senha do usuário ou psicólogo encontrado
        if user:
            stored_password_hash = user[6]
            if bcrypt.check_password_hash(stored_password_hash, senha):
                session['user_id'] = user[0]
                session['tipo_usuario'] = 'psicologo' if is_psicologo else 'usuario'
                return jsonify({'success': True, 'tipo_usuario': session['tipo_usuario']}), 200
            else:
                return jsonify({'error': 'Usuário ou senha incorretos!'}), 401
        else:
            return jsonify({'error': 'Usuário não encontrado!'}), 404

    except Exception as e:
        return jsonify({'error': f"Erro ao realizar login: {str(e)}"}), 400
    
    
#RECUPERAR SENHA

@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        resposta_usuario = request.form.get('resposta_seguranca').strip().lower()

        # Verificação rápida se os campos estão preenchidos
        if not email or not resposta_usuario:
            return 'E-mail e resposta de segurança são obrigatórios.', 400

        conectar = connect_db()
        cursor = conectar.cursor()

        # Verifica a resposta de segurança no banco
        cursor.execute('SELECT resposta_seguranca FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        conectar.close()

        if not user:
            return 'E-mail não encontrado.', 400

        resposta_armazenada = user[0].strip().lower()
        print(f"Resposta armazenada: '{resposta_armazenada}', Resposta do usuário: '{resposta_usuario}'")
        if resposta_armazenada != resposta_usuario:
            return 'Resposta de segurança incorreta.', 400

        # Redireciona para a redefinição de senha
        return redirect(url_for('resetar_senha', email=email))

    return render_template('recuperar_senha.html')

# Rota para redefinir a senha
@app.route('/resetar_senha', methods=['GET', 'POST'])
def resetar_senha():
    if request.method == 'POST':
        email = request.form.get('email')  # Agora pega o e-mail do corpo da requisição
        nova_senha = request.form['nova_senha']
        print(f"Email recebido no POST: {email}")  # Print para depuração

        if not email:
            return 'Erro: E-mail não encontrado na requisição.', 400

        senha_hash = bcrypt.generate_password_hash(nova_senha).decode('utf-8')
        
        conectar = connect_db()
        cursor = conectar.cursor()
        
        # Atualiza a senha
        cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (senha_hash, email))
        conectar.commit()

        # Verifique se alguma linha foi afetada
        if cursor.rowcount == 0:
            conectar.close()
            return 'Erro: Nenhum registro foi atualizado. E-mail não encontrado.', 400

        conectar.close()
        return 'Senha redefinida com sucesso!', 200

    # Caso seja um método GET, apenas retorna a página
    email = request.args.get('email')
    print(f"Tentando redefinir senha para o email: {email}")
    return render_template('resetar_senha.html', email=email)


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
    
    
#Aprovar Psico
@app.route('/admin/psicologos_pendentes')
def admin_psicologos_pendentes():
    conectar = connect_db()
    cursor = conectar.cursor()

    cursor.execute("SELECT * FROM analise_psicologo WHERE status = 'pendente'")
    psicologos_pendentes = cursor.fetchall()
    conectar.close()

    return render_template('admin.html', psicologos=psicologos_pendentes)

from flask import jsonify

@app.route('/admin/aprovar_psicologo/<int:id>', methods=['POST'])
def aprovar_psicologo(id):
    conectar = connect_db()
    cursor = conectar.cursor()
    
    # Move o psicólogo para a tabela 'psicologos_aceitos'
    cursor.execute('''
        INSERT INTO psicologos_aceitos (nome, cpf, data_nasc, nickname, email, senha, tipo_usuario, pergunta_seguranca, resposta_seguranca)
        SELECT nome, cpf, data_nasc, nickname, email, senha, tipo_usuario, pergunta_seguranca, resposta_seguranca
        FROM analise_psicologo WHERE id = ?
    ''', (id,))
    
    # Atualiza o status para "aprovado" na tabela de análise
    cursor.execute("UPDATE analise_psicologo SET status = 'aprovado' WHERE id = ?", (id,))
    conectar.commit()
    conectar.close()
    
    return jsonify({'success': True})

@app.route('/admin/reprovar_psicologo/<int:id>', methods=['POST'])
def reprovar_psicologo(id):
    conectar = connect_db()
    cursor = conectar.cursor()

    # Atualiza o status para "reprovado" na tabela de análise
    cursor.execute("UPDATE analise_psicologo SET status = 'reprovado' WHERE id = ?", (id,))
    conectar.commit()
    conectar.close()

    return jsonify({'success': True})

    
if __name__ == '__main__':
    criar_tabela_login()
    criar_tabela_chat()
    criar_tabela_pontos()
    criar_tabela_admin()
    criar_tabela_diario()
    criar_tabela_analise_psicologo()
    criar_tabela_psicologos_aceitos()
    
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