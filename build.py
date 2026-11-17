"""Gerador do site "Mudanças climáticas, linha por linha".

Uso:  python build.py            -> cria index.html na pasta atual
      python build.py saida.html -> cria o arquivo com outro nome

Só usa a biblioteca padrão do Python. O site gerado não tem JavaScript.
"""
import html
import sys
from pathlib import Path

CSS = r''':root{--ink:#F7EEE5;--mute:#F0DFCF;--line:rgba(255,200,150,.32);--panel:rgba(0,0,0,.55);--accent:#FFB067;--str:#9BE0AE;--kw:#E3A9F2;--cm:#E2CDB9;--r:26px;
  box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:dark}
html{scroll-padding-top:calc(60px + env(safe-area-inset-top,0px));scroll-behavior:smooth;background:#000}
*{box-sizing:border-box}
body{margin:0;color:var(--ink);font:400 1.08rem/1.65 "Nunito","Helvetica Neue",Arial,sans-serif}
body::after{content:"";position:fixed;inset:0;z-index:-1;background:linear-gradient(180deg,#000 0%,#1A0A03 45%,#6E2A08 80%,#B34A0B 100%)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);background:#000;z-index:10}
h1,h2,h3{font-family:"Nunito","Helvetica Neue",Arial,sans-serif;font-weight:800;line-height:1.1;margin:0}
a{color:var(--accent)}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
nav{position:sticky;top:calc(env(safe-area-inset-top,0px) + .6rem);margin:.6rem .8rem 0;border-radius:999px;z-index:5;background:#000;border:1px solid var(--line);
  display:flex;gap:1.2rem;align-items:center;padding:.8rem 1.25rem;overflow-x:auto;white-space:nowrap}
nav .path{font:.85rem "JetBrains Mono",monospace;color:var(--mute);margin-right:auto}
nav a{font:.85rem "JetBrains Mono",monospace;text-decoration:none;color:var(--ink)}
nav a:hover{color:var(--accent)}
main{max-width:1000px;margin:0 auto;padding:0 1.25rem}
section{padding:4.5rem 0 1rem}
.tag{font:.85rem "JetBrains Mono",monospace;color:var(--cm);margin:0 0 .9rem}
h1{font-size:clamp(2.4rem,7vw,4.6rem);font-weight:800;letter-spacing:-.025em;max-width:14ch}
h2{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:700;letter-spacing:-.015em;max-width:24ch}
h3{font-size:1.15rem;font-weight:700;margin-bottom:.35rem}
p{max-width:62ch}
.lead{font-size:1.2rem;color:var(--mute);margin:1.2rem 0 2rem}
.btn{font:800 .95rem "Nunito",sans-serif;background:var(--accent);color:#1A0A02;border:0;border-radius:999px;padding:.8rem 1.5rem;cursor:pointer;text-decoration:none;display:inline-block}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
.btns{display:flex;flex-wrap:wrap;gap:.8rem;margin:0 0 1rem}
.editor{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);margin:2rem 0;overflow:hidden}
.editor header{display:flex;justify-content:space-between;padding:.55rem 1rem;border-bottom:1px solid var(--line);font:.8rem "JetBrains Mono",monospace;color:var(--mute)}
pre{margin:0;padding:1rem 0;overflow-x:auto;font:.92rem/1.75 "JetBrains Mono",ui-monospace,monospace}
pre code{display:block;min-width:max-content}
.ln{display:inline-block;width:2.6rem;text-align:right;padding-right:1rem;color:var(--cm);user-select:none}
.k{color:var(--kw)}.s{color:var(--str)}.c{color:var(--cm)}
.run{border-top:1px solid var(--line);padding:1rem;display:flex;flex-wrap:wrap;gap:1rem 1.5rem;align-items:center}
.run label{font:.9rem "JetBrains Mono",monospace;display:flex;align-items:center;gap:.6rem;cursor:pointer}
.run input{width:1.15rem;height:1.15rem;accent-color:var(--accent)}
#out{font:600 1rem "JetBrains Mono",monospace;margin:0}
#out.ok{color:var(--str)}#out.bad{color:var(--accent)}
.stats{display:grid;overflow:hidden;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));border:1px solid var(--line);border-radius:var(--r);background:var(--panel)}
.stat{padding:1.4rem;border-right:1px solid var(--line)}
.stat:last-child{border-right:0}
.stat b{display:block;font:800 2.6rem/1 "Nunito",sans-serif;color:var(--accent);letter-spacing:-.02em}
.stat span{display:block;margin-top:.5rem;font-size:.95rem;color:var(--mute)}
.stat em{display:block;margin-top:.2rem;font:.78rem "JetBrains Mono",monospace;color:var(--cm);font-style:normal}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.5rem;margin-top:2rem}
.item{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:1.3rem 1.4rem 1.5rem}
.item .var{font:.8rem "JetBrains Mono",monospace;color:var(--accent);margin-bottom:.3rem}
.item p{margin:0;font-size:1rem;color:var(--mute)}
.fix .item{border-color:rgba(155,224,174,.5)}.fix .var{color:var(--str)}
.inter{margin:3.5rem 0 0;padding:1.2rem 1.3rem;border:1px solid var(--line);background:var(--panel);font:.95rem "JetBrains Mono",monospace;color:var(--mute);border-radius:var(--r)}
.inter b{color:var(--accent);margin-right:.6rem}
.slots{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:1.2rem;margin-top:2rem}
.slot{height:170px;border:2px dashed var(--line);border-radius:var(--r);display:grid;place-items:center;font:.85rem "JetBrains Mono",monospace;color:var(--cm);background:var(--panel)}
.cap{margin:.5rem 0 0;font-size:.95rem}.cap small{display:block;font:.75rem "JetBrains Mono",monospace;color:var(--cm)}
.links{list-style:none;padding:0;margin:2rem 0 0;background:var(--panel);border:1px solid var(--line);border-radius:var(--r);overflow:hidden}
.links li+li{border-top:1px solid var(--line)}
.links a{display:flex;justify-content:space-between;gap:1rem;padding:.9rem 1.1rem;text-decoration:none;color:var(--ink);flex-wrap:wrap}
.links a:hover{color:var(--accent)}
.links small{font:.8rem "JetBrains Mono",monospace;color:var(--cm)}
.wx{display:flex;flex-wrap:wrap;gap:.8rem;padding:1rem}
.wx input{flex:1 1 220px;font:1rem "JetBrains Mono",monospace;padding:.8rem 1.2rem;background:#000;color:var(--ink);border:1px solid var(--line);border-radius:999px}
.wxs{padding:0 1rem 1rem;margin:0;font:.85rem "JetBrains Mono",monospace;color:var(--mute)}
.commit{margin:5rem 0 3rem;padding:2.5rem 1.8rem;background:#000;border:1px solid var(--line);border-radius:34px}
.commit h2{max-width:20ch}.commit p{color:var(--mute)}
footer{max-width:1000px;margin:0 auto;padding:1rem 1.25rem 3rem;font:.82rem "JetBrains Mono",monospace;color:var(--mute)}
.wm{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:1rem;margin-top:2rem}
#wm{width:100%;height:auto;display:block;border-radius:18px;background:#0A0502}
#wm .land{fill:#3B2210;stroke:#8A4A1C;stroke-width:.4}
#wm .gr{stroke:rgba(255,200,150,.12);stroke-width:.3}
#wm .dot{fill:var(--accent);stroke:#000;stroke-width:.6}
#wm .ring{fill:none;stroke:var(--accent);stroke-width:.8;animation:pulse 2.2s ease-out infinite}
@keyframes pulse{from{r:2.5;opacity:.9}to{r:9;opacity:0}}
#wm .pt{cursor:pointer;outline:none}
#wm .pt:focus-visible .dot,#wm .pt.on .dot{stroke:#fff;stroke-width:1.2}
.evs{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}
.ev{font:600 .85rem "Nunito",sans-serif;background:transparent;color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:.45rem .9rem;cursor:pointer}
.ev.on{background:var(--accent);color:#1A0A02;border-color:var(--accent)}
@media (prefers-reduced-motion:reduce){#wm .ring{animation:none;opacity:.5;r:6}}
.art{display:block;overflow:hidden;border:1px solid var(--line)}.art svg{width:100%;height:100%;display:block}
  background:#0B0502;border:1px solid var(--line);border-radius:28px;overflow:hidden;display:none;flex-direction:column;box-shadow:0 10px 40px rgba(0,0,0,.6)}
@media (max-width:640px){.stat{border-right:0;border-bottom:1px solid var(--line)}.stat:last-child{border-bottom:0}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}

.ev{text-decoration:none;display:inline-block}
.info{display:none;margin:0;padding:1rem 1.2rem;border:1px solid var(--line);border-radius:20px;background:#000;max-width:none;scroll-margin-top:60vh}
.info.def,.info:target{display:block}
.wm:has(.info:target) .def{display:none}
.info b{display:block;font-size:1.1rem}.info small{display:block;font:.78rem "JetBrains Mono",monospace;color:var(--cm)}
#wm .pt:focus-visible .dot{stroke:#fff;stroke-width:1.2}
'''

ARTE = [
    r'''<svg viewBox="0 0 300 170" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Ilustração de uma geleira derretendo ao pôr do sol"><defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B0A04"/><stop offset="1" stop-color="#C2550E"/></linearGradient></defs><rect width="300" height="170" fill="url(#g1)"/><circle cx="225" cy="98" r="22" fill="#FFB067"/><polygon points="0,118 45,55 85,92 130,38 190,118 240,78 300,120 300,170 0,170" fill="#2A140A"/><polygon points="130,38 112,66 124,62 132,72 142,60 152,66" fill="#F2F8FA"/><polygon points="45,55 32,76 42,72 50,80 58,70" fill="#F2F8FA"/><polygon points="0,128 70,114 150,122 210,110 300,124 300,170 0,170" fill="#BFE3EE"/><rect y="142" width="300" height="28" fill="#0E3B4A"/><polygon points="60,146 74,132 90,146" fill="#F2F8FA"/><polygon points="180,148 192,138 208,148" fill="#DCEFF5"/><path d="M92 122v14M132 124v10M176 118v16" stroke="#7CCBE0" stroke-width="2" stroke-linecap="round"/></svg>''',
    r'''<svg viewBox="0 0 300 170" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Ilustração de uma fazenda solar no semiárido"><defs><linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A0F04"/><stop offset="1" stop-color="#E8801F"/></linearGradient></defs><rect width="300" height="170" fill="url(#g2)"/><circle cx="70" cy="72" r="26" fill="#FFD08A"/><rect y="106" width="300" height="64" fill="#7A3A12"/><g fill="#16384B" stroke="#7CCBE0" stroke-width=".6"><polygon points="40,112 80,112 74,126 34,126"/><polygon points="95,112 135,112 129,126 89,126"/><polygon points="150,112 190,112 184,126 144,126"/><polygon points="205,112 245,112 239,126 199,126"/><polygon points="20,132 70,132 62,150 12,150"/><polygon points="85,132 135,132 127,150 77,150"/><polygon points="150,132 200,132 192,150 142,150"/><polygon points="215,132 265,132 257,150 207,150"/></g><path d="M268 108v-22M268 98h-8v-8M268 94h8v-10" stroke="#5E9C5A" stroke-width="3.5" stroke-linecap="round" fill="none"/></svg>''',
    r'''<svg viewBox="0 0 300 170" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Ilustração de uma cidade costeira com a maré alta invadindo as ruas"><rect width="300" height="170" fill="#10080A"/><circle cx="255" cy="30" r="12" fill="#F7EEE5"/><g fill="#2B1B14"><rect x="20" y="70" width="30" height="70"/><rect x="55" y="50" width="28" height="90"/><rect x="88" y="80" width="34" height="60"/><rect x="128" y="40" width="30" height="100"/><rect x="165" y="75" width="32" height="65"/><rect x="202" y="58" width="28" height="82"/><rect x="236" y="85" width="40" height="55"/></g><g fill="#FFB067"><rect x="28" y="80" width="6" height="8"/><rect x="62" y="62" width="6" height="8"/><rect x="70" y="90" width="6" height="8"/><rect x="98" y="92" width="6" height="8"/><rect x="136" y="54" width="6" height="8"/><rect x="142" y="80" width="6" height="8"/><rect x="174" y="88" width="6" height="8"/><rect x="210" y="70" width="6" height="8"/><rect x="246" y="96" width="6" height="8"/></g><rect y="122" width="300" height="48" fill="#0E3B4A" opacity=".9"/><path d="M0 122q15-7 30 0t30 0 30 0 30 0 30 0 30 0 30 0 30 0 30 0 30 0" stroke="#7CCBE0" stroke-width="2" fill="none"/></svg>''',
]

# ---------------------------------------------------------------------------
# DADOS: edite aqui os textos, eventos do mapa e links
# ---------------------------------------------------------------------------
DATA_LEVANTAMENTO = "17/11/2026"

NAV = [("estado", "estado"), ("causas", "causas"), ("consequencias", "consequências"),
       ("solucoes", "soluções"), ("poluicao", "poluição"), ("mapa", "mapa"),
       ("sites", "sites"), ("previsao", "previsão")]

STATS = [("+1,3 °C", "aquecimento médio global", "acima da era pré-industrial (IPCC AR6)"),
         ("424 ppm", "CO₂ na atmosfera", "maior concentração em 800 mil anos"),
         ("−12,2%", "gelo marinho por década", "mínimo do Ártico medido em setembro")]

CAUSAS = [
    ("energia_e_transporte", "Energia e transporte", "Cerca de 75% das emissões globais de CO₂ vêm da queima de combustíveis fósseis para eletricidade, indústria e transporte."),
    ("desmatamento", "Desmatamento", "Florestas derrubadas deixam de capturar carbono, e o estoque que guardavam volta para a atmosfera."),
    ("agropecuaria", "Agropecuária", "Metano do gado, óxido nitroso de fertilizantes e mudança no uso do solo respondem por quase um quinto das emissões."),
    ("industria_e_consumo", "Indústria e consumo", "Cimento, aço, plásticos e bens duráveis mantêm uma demanda constante de energia fóssil."),
]
CONSEQUENCIAS = [
    ("calor_extremo", "Calor extremo", "Ondas de calor mais longas e intensas elevam a mortalidade, sobrecarregam hospitais e reduzem a produtividade."),
    ("chuva_e_seca", "Chuva e seca", "O ciclo da água ficou mais violento: chuvas concentradas causam enchentes, enquanto regiões inteiras enfrentam estiagens prolongadas."),
    ("nivel_do_mar", "Nível do mar", "O gelo derretido e a expansão térmica da água já ameaçam cidades costeiras e deltas onde vivem centenas de milhões de pessoas."),
    ("biodiversidade", "Biodiversidade", "Espécies não conseguem migrar na velocidade das mudanças, e recifes de coral sofrem branqueamento em massa."),
    ("alimentacao", "Alimentação", "Safras mais instáveis elevam o preço dos alimentos e pressionam a segurança alimentar global."),
    ("saude_e_cidades", "Saúde e cidades", "Ilhas de calor, doenças tropicais em novas áreas e interrupções de energia tornam a vida urbana mais vulnerável."),
]
SOLUCOES = [
    ("renovaveis *= 3", "Triplicar renováveis", "Solar e eólica já são as formas mais baratas de gerar eletricidade em boa parte do mundo."),
    ("ecossistemas.restaurar()", "Restaurar ecossistemas", "Florestas, manguezais e solos degradados podem voltar a funcionar como sumidouros de carbono."),
    ("cidades.adaptar()", "Adaptar cidades", "Drenagem, arborização, telhados claros e alerta precoce salvam vidas com tecnologia já disponível."),
    ("carbono.precificar()", "Precificar carbono", "Colocar preço nas emissões redireciona investimento e acelera a troca da matriz fóssil."),
]
POLUICAO = [
    ("ar", "Ar", "Segundo a OMS, quase toda a população mundial respira ar acima dos limites recomendados. A poluição do ar está ligada a milhões de mortes prematuras por ano."),
    ("plasticos", "Plásticos", "Estimativas do PNUMA apontam que de 19 a 23 milhões de toneladas de plástico vazam todo ano para rios, lagos e mares."),
    ("agua_e_solo", "Água e solo", "Esgoto sem tratamento, agrotóxicos e resíduos industriais contaminam rios, aquíferos e solos, e chegam à comida e à água de beber."),
    ("mesma_fonte", "Mesma fonte", "A queima de combustíveis solta CO₂ e também material particulado e outros poluentes. Cortar fósseis reduz emissões e melhora o ar ao mesmo tempo."),
]
INTERLUDIOS = {
    "estado": ("interlúdio_01", "Geleira em recuo: o gelo que derrete hoje define o nível do mar das próximas décadas."),
    "causas": ("interlúdio_02", "Fazenda solar no semiárido: a mesma região que sofre com a seca pode se tornar produtora de energia."),
    "consequencias": ("interlúdio_03", "Maré alta em cidade costeira: a água que invade a rua já é rotina em centenas de cidades."),
}
LEGENDAS = [("Derretimento glacial", "módulo 01 · registro visual"),
            ("Fazenda solar no semiárido", "módulo 02 · registro visual"),
            ("Cidade costeira em maré alta", "módulo 03 · registro visual")]

LINKS_POLUICAO = [
    ("OMS, poluição do ar", "https://www.who.int/health-topics/air-pollution", "who.int"),
    ("PNUMA, poluição por plásticos", "https://www.unep.org/plastic-pollution", "unep.org"),
    ("IQAir, qualidade do ar no mundo", "https://www.iqair.com", "iqair.com"),
]
LINKS_SITES = [
    ("IPCC, Painel Intergovernamental sobre Mudanças Climáticas", "https://www.ipcc.ch", "ipcc.ch"),
    ("NASA Climate", "https://climate.nasa.gov", "climate.nasa.gov"),
    ("NOAA Climate", "https://www.noaa.gov/climate", "noaa.gov/climate"),
    ("Agência Internacional de Energia", "https://www.iea.org", "iea.org"),
    ("Observatório do Clima", "https://www.oc.eco.br", "oc.eco.br"),
    ("INPE, Instituto Nacional de Pesquisas Espaciais", "https://www.gov.br/inpe", "gov.br/inpe"),
]
LINKS_MAPAS = [
    ("Mapa ao vivo: GDACS", "https://www.gdacs.org", True),
    ("Incêndios: NASA FIRMS", "https://firms.modaps.eosdis.nasa.gov/map/", False),
    ("ReliefWeb", "https://reliefweb.int/disasters", False),
    ("Windy", "https://www.windy.com", False),
]

# (nome, tipo, (longitude, latitude), descrição) — para acrescentar um evento, copie uma linha
EVENTOS = [
    ("Santa Catarina, Brasil", "Temporais", (-50.5, -27.3), "Temporais entre 4 e 5 de novembro: 671 ocorrências em 76 municípios, segundo o governo do estado."),
    ("Brasil, seca", "Seca", (-48, -14), "Em 3 de novembro, a Defesa Civil Nacional reconheceu emergência em 44 municípios de 13 estados; os reconhecimentos refletem a seca em curso."),
    ("Costa Espacial, Flórida (EUA)", "Inundação", (-80.7, 28.3), "Duas chuvas de intensidade rara (cerca de 1 em 1.000 anos) em sequência. O estado declarou emergência após inundações no sul do condado de Brevard."),
    ("Sudoeste dos EUA", "Inundação", (-111, 34), "Cheias recordes de rios e alertas de enxurrada no início de novembro, com sucessivas rajadas de umidade vindas do Pacífico."),
    ("Apalaches do sul (EUA)", "Inundação", (-82, 36.5), "Cheias recordes dentro de uma grande tempestade que afetou mais de 120 milhões de pessoas em mais de 35 estados."),
    ("Portugal", "Tempestade", (-8, 39.5), "Tempestade Claudia, em 15 de novembro: ao menos 3 mortos e dezenas de feridos, muitos por causa de inundações."),
]

# Contornos simplificados dos continentes, em "longitude,latitude"
TERRA = [
    "-168,66 -141,70 -95,72 -80,68 -62,58 -55,48 -67,44 -76,36 -81,30 -80,25 -90,29 -97,26 -97,19 -90,21 -87,16 -83,9 -78,8 -82,8 -87,13 -95,16 -105,20 -110,24 -113,31 -117,32 -124,40 -125,48 -135,58 -150,60 -165,60",
    "-73,78 -60,82 -30,83 -20,75 -22,70 -43,60 -52,65 -58,75",
    "-78,8 -72,12 -62,10 -50,0 -35,-6 -39,-15 -48,-26 -58,-38 -65,-42 -68,-52 -72,-54 -75,-48 -73,-38 -71,-28 -70,-18 -76,-14 -81,-5 -80,0 -77,5",
    "-10,36 -9,43 -1,46 -5,48 2,51 8,54 10,57 5,62 14,68 28,71 45,68 60,70 80,73 105,77 140,72 170,70 180,66 170,60 160,55 142,52 135,43 129,35 122,30 121,22 108,18 106,10 100,8 103,1 98,8 92,22 80,15 77,8 73,18 67,25 57,25 59,22 52,16 43,13 35,28 34,31 36,36 27,37 26,41 23,38 19,40 15,38 12,44 8,44 3,43 -1,37 -6,36",
    "-6,36 10,37 20,32 32,31 35,28 43,12 51,12 41,-2 40,-15 35,-24 32,-29 20,-35 12,-18 9,-1 8,4 -8,4 -17,14 -17,21 -10,30",
    "114,-22 122,-18 130,-12 137,-12 142,-11 146,-19 153,-26 150,-37 141,-38 131,-31 115,-34",
    "-5,50 1,51 0,55 -3,58 -6,56",
    "130,31 135,34 141,38 142,44 140,41 132,35",
]


# ---------------------------------------------------------------------------
# FUNÇÕES: montam o HTML
# ---------------------------------------------------------------------------
def esc(texto):
    return html.escape(texto, quote=False)


def cartoes(itens):
    cards = "".join(
        f'<div class="item"><div class="var">{esc(v)}</div><h3>{esc(t)}</h3><p>{esc(p)}</p></div>'
        for v, t, p in itens)
    return f'<div class="grid">{cards}</div>'


def lista_links(itens):
    li = "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)} <small>{d}</small></a></li>'
        for t, u, d in itens)
    return f'<ul class="links">{li}</ul>'


def interludio(chave):
    nome, texto = INTERLUDIOS[chave]
    return f'<div class="inter"><b>{nome} &gt;_</b>{esc(texto)}</div>'


def secao(id_, tag, titulo, lead, miolo="", classe=""):
    cls = f' class="{classe}"' if classe else ""
    return (f'<section id="{id_}"{cls}><p class="tag"># {tag}</p><h2>{esc(titulo)}</h2>'
            f'<p class="lead">{esc(lead)}</p>{miolo}</section>')


def xy(lon, lat):
    """Projeção equirretangular: longitude/latitude -> coordenadas do SVG (360 x 180)."""
    return lon + 180, 90 - lat


def pontos(contorno):
    pares = [xy(*map(float, p.split(","))) for p in contorno.split()]
    return " ".join(f"{x:g},{y:g}" for x, y in pares)


def mapa():
    svg = ['<svg id="wm" viewBox="0 8 360 142" role="img" aria-label="Mapa-múndi com eventos extremos recentes">']
    for lon in range(-150, 151, 30):
        svg.append(f'<line x1="{lon + 180}" y1="0" x2="{lon + 180}" y2="180" class="gr"/>')
    for lat in range(-60, 61, 30):
        svg.append(f'<line x1="0" y1="{90 - lat}" x2="360" y2="{90 - lat}" class="gr"/>')
    for contorno in TERRA:
        svg.append(f'<polygon points="{pontos(contorno)}" class="land"/>')
    botoes, infos = [], ['<p class="info def">Escolha um ponto no mapa.</p>']
    for i, (nome, tipo, (lon, lat), desc) in enumerate(EVENTOS):
        x, y = xy(lon, lat)
        svg.append(f'<a href="#ev-{i}" class="pt" aria-label="{esc(nome)}">'
                   f'<circle cx="{x:g}" cy="{y:g}" r="2.5" class="ring"/>'
                   f'<circle cx="{x:g}" cy="{y:g}" r="2.4" class="dot"/></a>')
        botoes.append(f'<a class="ev" href="#ev-{i}">{esc(nome)}</a>')
        infos.append(f'<p class="info" id="ev-{i}"><b>{esc(nome)}</b>'
                     f'<small>{tipo} · levantamento de {DATA_LEVANTAMENTO}</small>{esc(desc)}</p>')
    svg.append("</svg>")
    return ('<div class="wm">' + "".join(svg) + '<div class="evs">' + "".join(botoes) + "</div>"
            + "".join(infos) + "</div>")


def botoes_mapas():
    bt = "".join(f'<a class="btn{"" if principal else " ghost"}" href="{u}" target="_blank" rel="noopener">{t}</a>'
                 for t, u, principal in LINKS_MAPAS)
    return f'<div class="btns" style="margin-top:1.2rem">{bt}</div>'


def registros():
    figs = "".join(
        f'<figure style="margin:0"><div class="slot art">{svg}</div>'
        f'<figcaption class="cap">{leg}<small>{mod}</small></figcaption></figure>'
        for svg, (leg, mod) in zip(ARTE, LEGENDAS))
    return f'<div class="slots">{figs}</div>'


def previsao():
    return ('<div class="editor"><header><span>previsao.py</span><span>python 3</span></header>'
            '<form class="wx" action="https://www.google.com/search" method="get" target="_blank" rel="noopener">'
            '<input name="q" type="text" value="previsão do tempo em " aria-label="Busca de previsão do tempo" autocomplete="off">'
            '<button class="btn" type="submit">Ver previsão</button></form>'
            '<p class="wxs"># digite o município no fim do texto; a previsão abre em outra aba</p></div>')


def pagina():
    nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in NAV)
    stats = "".join(f'<div class="stat"><b>{n}</b><span>{d}</span><em>{f}</em></div>' for n, d, f in STATS)
    secoes = [
        secao("estado", "estado_do_sistema",
              "O clima já saiu dos parâmetros em que a civilização foi escrita.",
              "A temperatura média do planeta subiu cerca de 1,3 °C desde a era pré-industrial. Parece pouco, mas num sistema em equilíbrio por milênios é como alterar uma constante no topo de um arquivo gigantesco: todas as funções abaixo respondem.",
              "<p>Os sinais não são hipotéticos. Ondas de calor recordes, chuvas concentradas em poucas horas, secas prolongadas e oceanos mais quentes e mais ácidos aparecem nos dados ano após ano.</p>"
              + interludio("estado")),
        secao("causas", "origem_do_problema",
              "Uma variável explica quase tudo: a queima de combustíveis fósseis.",
              "O efeito estufa é natural e mantém o planeta habitável. O problema é o excedente: desde 1850, carvão, petróleo e gás somaram mais CO₂ do que o sistema consegue absorver.",
              cartoes(CAUSAS) + interludio("causas")),
        secao("consequencias", "saida_do_sistema",
              "Os efeitos não estão no futuro do código: estão em execução agora.",
              "Cada fração de grau adiciona energia ao sistema. Essa energia não desaparece: ela se reorganiza em eventos extremos.",
              cartoes(CONSEQUENCIAS) + interludio("consequencias")),
        secao("solucoes", "correcoes",
              "O que ainda dá tempo de executar, e o que já é adaptação obrigatória.",
              "A ciência é direta: cada décima de grau evitada reduz danos. As soluções existem e são tecnicamente viáveis; o gargalo é a velocidade de implementação.",
              cartoes(SOLUCOES), "fix"),
        secao("poluicao", "poluicao", "Poluição e clima saem da mesma chaminé.",
              "São problemas diferentes, mas com causas em comum. A queima de combustíveis, o descarte de resíduos e a agropecuária intensiva sujam o ar, a água e o solo, e ainda aquecem o planeta.",
              cartoes(POLUICAO) + lista_links(LINKS_POLUICAO)),
        secao("mapa", "mapa_de_desastres", "Eventos extremos acontecendo agora pelo mundo.",
              f"Toque nos pontos para ver o que aconteceu. O mapa mostra um levantamento de {DATA_LEVANTAMENTO} feito em relatos recentes; para acompanhar em tempo real, use os mapas abaixo.",
              mapa()
              + '<p style="font-size:.95rem;margin-top:1rem">Cada evento é estudado caso a caso pela ciência de atribuição. O que os dados mostram é que a mudança climática torna chuvas intensas, calor extremo e secas mais frequentes e mais fortes.</p>'
              + botoes_mapas()),
        secao("registros", "registros_visuais", "Três cenas do sistema em mudança.",
              "Ilustrações que resumem o que o texto descreve: o gelo que recua, a energia que pode vir do sol e a água que chega às cidades.",
              registros()),
        secao("sites", "outros_sites", "Outros lugares com o mesmo conteúdo.",
              "Portais, institutos e repositórios abertos para continuar a leitura fora daqui.",
              lista_links(LINKS_SITES)),
        secao("previsao", "previsão_do_tempo", "O tempo de agora, na cidade que você escolher.",
              "Digite o nome do município e execute a consulta. A previsão abre em outra aba, com dados de serviços meteorológicos abertos.",
              previsao()),
    ]
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mudanças climáticas, linha por linha · clima.py</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Nunito:wght@400;600;800&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<nav aria-label="Seções"><span class="path">~/planeta/clima.py</span>{nav}</nav>
<main>
<section style="padding-top:3.5rem">
<p class="tag"># leitura aberta · clima.py</p>
<h1>Mudanças climáticas, linha por linha.</h1>
<p class="lead">O planeta é um sistema de variáveis conhecidas: energia, carbono, água e tempo. Esta página lê o código-fonte do clima: o que já mudou, o que continua rodando e quais correções dependem de nós.</p>
<div class="btns"><a class="btn" href="#estado">Começar a leitura</a></div>
<div class="stats">{stats}</div>
</section>
{"".join(secoes)}
<div class="commit"><p class="tag"># commit -m</p><h2>Commit final: cortar emissões pela metade até 2030.</h2><p>O código do clima é aberto e roda em tempo real. O que muda o resultado não é um comentário no arquivo: é o que entra na branch principal.</p></div>
</main>
<footer>Conteúdo educativo. Dados baseados no IPCC AR6, NOAA e Agência Internacional de Energia.</footer>
</body>
</html>
"""


if __name__ == "__main__":
    saida = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    saida.write_text(pagina(), encoding="utf-8")
    print(f"Site gerado em {saida} ({saida.stat().st_size} bytes)")
