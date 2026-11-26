import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave_super_secreta_ecologia"

def init_db():
    conn = sqlite3.connect("ecologia.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT PRIMARY KEY,
            senha TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autor TEXT NOT NULL,
            texto TEXT NOT NULL,
            curtidas INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            acao TEXT NOT NULL,
            detalhe TEXT NOT NULL,
            feito INTEGER DEFAULT 0
        )
    """)

    cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, senha) VALUES (?, ?)", ("admin", "1234"))
    
    cursor.execute("SELECT COUNT(*) FROM dicas")
    if cursor.fetchone()[0] == 0:
        dicas_iniciais = [
            ("Sistema", "Reduza o consumo de plásticos descartáveis: eles levam séculos no tempo ecológico para se decompor.", 5),
            ("Sistema", "Plante espécies nativas da sua região para acelerar a sucessão ecológica local.", 3),
            ("Sistema", "Economize água e energia para diminuir a pressão sobre os ecossistemas naturais.", 4)
        ]
        cursor.executemany("INSERT INTO dicas (autor, texto, curtidas) VALUES (?, ?, ?)", dicas_iniciais)
        
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    sucesso = ""
    
    if request.method == "POST":
        acao = request.form.get("acao")
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()

        conn = sqlite3.connect("ecologia.db")
        cursor = conn.cursor()

        if acao == "entrar":
            cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
            if cursor.fetchone():
                session["usuario"] = usuario
                conn.close()
                return redirect(url_for("painel"))
            else:
                erro = "Usuário ou senha incorretos!"
                
        elif acao == "cadastrar":
            if not usuario or not senha:
                erro = "Preencha usuário e senha para cadastrar."
            else:
                try:
                    cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
                    conn.commit()
                    sucesso = f"Conta '{usuario}' criada com sucesso! Faça login."
                except sqlite3.IntegrityError:
                    erro = "Esse nome de usuário já existe! Escolha outro."
        conn.close()

    return render_template("login.html", erro=erro, sucesso=sucesso)

@app.route("/painel", methods=["GET", "POST"])
def painel():
    if "usuario" not in session:
        return redirect(url_for("login"))

    usuario_atual = session["usuario"]
    conn = sqlite3.connect("ecologia.db")
    cursor = conn.cursor()

    if request.method == "POST":
        tipo_form = request.form.get("tipo_form")
        
        if tipo_form == "dica":
            nova_dica = request.form.get("nova_dica", "").strip()
            if nova_dica:
                cursor.execute("INSERT INTO dicas (autor, texto, curtidas) VALUES (?, ?, 0)", (usuario_atual, nova_dica))
                conn.commit()
                conn.close()
                return redirect(url_for("painel", aviso="Dica publicada no mural!") + "#mural-dicas")
                
        elif tipo_form == "curtir_dica":
            dica_id = request.form.get("dica_id")
            cursor.execute("UPDATE dicas SET curtidas = curtidas + 1 WHERE id = ?", (dica_id,))
            conn.commit()
            conn.close()
            return redirect(url_for("painel", aviso="Você apoiou uma dica!") + "#mural-dicas")

        elif tipo_form == "meta":
            acao_meta = request.form.get("acao_meta", "").strip()
            detalhe_meta = request.form.get("detalhe_meta", "").strip()
            if acao_meta and detalhe_meta:
                cursor.execute("INSERT INTO metas (usuario, acao, detalhe, feito) VALUES (?, ?, ?, 0)", (usuario_atual, acao_meta, detalhe_meta))
                conn.commit()
                conn.close()
                return redirect(url_for("painel", aviso="Nova meta semanal salva!") + "#secao-sustentavel")

        elif tipo_form == "concluir_meta":
            meta_id = request.form.get("meta_id")
            cursor.execute("UPDATE metas SET feito = 1 WHERE id = ? AND usuario = ?", (meta_id, usuario_atual))
            conn.commit()
            conn.close()
            return redirect(url_for("painel", aviso="Meta marcada como concluída!") + "#secao-sustentavel")

    cursor.execute("SELECT id, autor, texto, curtidas FROM dicas ORDER BY curtidas DESC, id DESC")
    dicas_db = [{"id": row[0], "autor": row[1], "texto": row[2], "curtidas": row[3]} for row in cursor.fetchall()]

    cursor.execute("SELECT id, acao, detalhe, feito FROM metas WHERE usuario = ? ORDER BY id DESC", (usuario_atual,))
    metas_db = [{"id": row[0], "acao": row[1], "detalhe": row[2], "feito": bool(row[3])} for row in cursor.fetchall()]

    cursor.execute("""
        SELECT u.usuario, COUNT(m.id) as total_concluidas
        FROM usuarios u
        LEFT JOIN metas m ON u.usuario = m.usuario AND m.feito = 1
        GROUP BY u.usuario
        ORDER BY total_concluidas DESC, u.usuario ASC
        LIMIT 5
    """)
    ranking_db = [{"usuario": row[0], "pontos": row[1]} for row in cursor.fetchall()]
    conn.close()

    metas_concluidas = sum(1 for m in metas_db if m["feito"])
    metas_pendentes = len(metas_db) - metas_concluidas

    if metas_concluidas >= 5:
        status_usuario = "🌱 Economizador Consciente (Mestre Sustentável)"
        cor_status = "#52b788"
        pode_certificado = True
    elif metas_concluidas >= 2:
        status_usuario = "🌿 No Caminho Certo (Praticante Ecológico)"
        cor_status = "#40916c"
        pode_certificado = False
    else:
        status_usuario = "⚡ Em Alerta (Gastador / Precisa de Hábitos Sustentáveis)"
        cor_status = "#e63946"
        pode_certificado = False

    conceitos = [
        {
            "titulo": "Tempo Ecológico",
            "tempo": "Anos a Séculos",
            "descricao": "Sucessão ecológica, ciclos sazonais e recuperação de florestas após incêndios.",
            "imagem": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=500&q=60"
        },
        {
            "titulo": "Tempo Evolutivo",
            "tempo": "Milhares a Milhões de Anos",
            "descricao": "Seleção natural, mutações genéticas e adaptação profunda das espécies.",
            "imagem": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=500&q=60"
        },
        {
            "titulo": "Tempo Geológico",
            "tempo": "Milhões a Bilhões de Anos",
            "descricao": "Movimento das placas tectônicas, formação de montanhas e eras glaciais.",
            "imagem": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=500&q=60"
        }
    ]

    frases = [
        "“A natureza não faz nada em vão.” — Aristóteles",
        "“O que sabemos é uma gota; o que ignoramos é um oceano.” — Isaac Newton",
        "“Na natureza, nada se cria, nada se perde, tudo se transforma.” — Antoine Lavoisier"
    ]

    data_hoje = datetime.now().strftime("%d/%m/%Y")

    return render_template(
        "index.html",
        usuario=usuario_atual,
        conceitos=conceitos,
        dicas=dicas_db,
        frases=frases,
        metas=metas_db,
        metas_concluidas=metas_concluidas,
        metas_pendentes=metas_pendentes,
        total_dicas_usuario=sum(1 for d in dicas_db if d["autor"] == usuario_atual),
        status_usuario=status_usuario,
        cor_status=cor_status,
        pode_certificado=pode_certificado,
        ranking=ranking_db,
        data_hoje=data_hoje
    )

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
