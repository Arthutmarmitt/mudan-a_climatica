from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "chave_super_secreta_ecologia"

usuarios_cadastrados = {
    "admin": "1234"
}

dicas_lista = [
    {"autor": "Sistema", "texto": "Reduza o consumo de plásticos descartáveis: eles levam séculos no tempo ecológico para se decompor."},
    {"autor": "Sistema", "texto": "Plante espécies nativas da sua região para acelerar a sucessão ecológica local."},
    {"autor": "Sistema", "texto": "Economize água e energia para diminuir a pressão sobre os ecossistemas naturais."}
]

metas_usuarios = {
    "admin": [
        {"acao": "Economia de Água", "detalhe": "Reduzi o tempo no banho em 2 minutos.", "feito": True},
        {"acao": "Economia de Energia", "detalhe": "Desliguei aparelhos da tomada em stand-by.", "feito": False}
    ]
}

@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    sucesso = ""
    
    if request.method == "POST":
        acao = request.form.get("acao")
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()

        if acao == "entrar":
            if usuario in usuarios_cadastrados and usuarios_cadastrados[usuario] == senha:
                session["usuario"] = usuario
                if usuario not in metas_usuarios:
                    metas_usuarios[usuario] = []
                return redirect(url_for("painel"))
            else:
                erro = "Usuário ou senha incorretos!"
                
        elif acao == "cadastrar":
            if not usuario or not senha:
                erro = "Preencha usuário e senha para cadastrar."
            elif usuario in usuarios_cadastrados:
                erro = " Esse nome de usuário já existe! Escolha outro."
            else:
                usuarios_cadastrados[usuario] = senha
                metas_usuarios[usuario] = []
                sucesso = f"Conta '{usuario}' criada! Agora faça login."

    return render_template("login.html", erro=erro, sucesso=sucesso)

@app.route("/painel", methods=["GET", "POST"])
def painel():
    if "usuario" not in session:
        return redirect(url_for("login"))

    usuario_atual = session["usuario"]

    if request.method == "POST":
        tipo_form = request.form.get("tipo_form")
        
        if tipo_form == "dica":
            nova_dica = request.form.get("nova_dica", "").strip()
            if nova_dica:
                dicas_lista.append({
                    "autor": usuario_atual,
                    "texto": nova_dica
                })
        elif tipo_form == "meta":
            acao_meta = request.form.get("acao_meta", "").strip()
            detalhe_meta = request.form.get("detalhe_meta", "").strip()
            if acao_meta and detalhe_meta:
                metas_usuarios[usuario_atual].append({
                    "acao": acao_meta,
                    "detalhe": detalhe_meta,
                    "feito": False
                })

        return redirect(url_for("painel") + "#secao-sustentavel")

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

    return render_template(
        "index.html",
        usuario=usuario_atual,
        conceitos=conceitos,
        dicas=dicas_lista,
        frases=frases,
        metas=metas_usuarios.get(usuario_atual, [])
    )

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)