import json
import os
import re
from datetime import datetime
from html import escape
from urllib.parse import quote


# Ler arquivos Json
def load_blocked_sites():
    with open("blocked.json", "r", encoding="utf-8") as file:
        blocked_list = json.load(file)["bloqueados"]
        return blocked_list

def load_filter_words():
    with open("words.json", "r", encoding="utf-8") as file:
        filter_words = json.load(file)
        return filter_words


# Logs
def create_log(url, action):
    with open("log.json", "a", encoding="utf-8") as f:

        log = {
            "id": "req" + datetime.now().strftime("%H%M%S%f"),
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "url": url,
            "acao": action}
        
        f.write(json.dumps(log, ensure_ascii=False) + "\n")


# Filtro conteúdo
def filter_content(html, words):
    for blocked_word, replace_word in words.items():
        pattern = re.compile(re.escape(blocked_word), re.IGNORECASE)
        html = pattern.sub(replace_word, html)
    return html


# Página de bloqueio
def blocked_page(url):
    return f"""
    <html>
        <head><title>Site Bloqueado</title></head>
        <body style="font-family: Arial; background-color: #111; color: white; text-align: center; padding: 60px;">
            <img src="https://img.icons8.com/?size=100&id=63652&format=png&color=000000" style="width: 100px; margin-top: 10px;"/>
            <h1 style="color: red;">Acesso Bloqueado</h1>
            <p>O site <b>{url}</b> foi bloqueado pelo proxy.</p>
            <a href="/" style="color: #FFFFFF; text-decoration: none; font-size: 1.2em;">Voltar à Busca</a>
        </body>
    </html>
    """

# Página inicial
def home_page():
    return """
    <html>
        <head>
            <title>Web Proxy</title>
            <style> 
                body {display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; margin:0; 
                font-family:Arial,sans-serif; background:#f8f9fa}
                h1 {margin-bottom:30px; color:#202124;}
                .search-box {width:90%; max-width:560px;}
                .search-box form {display:flex; align-items:center; background:white; border:1px solid #dfe1e5; border-radius:24px; padding:4px 6px 4px 20px;}
                .search-box form:focus-within {box-shadow:0 1px 6px rgba(32,33,36,.28);}
                input[type=text] {flex:1; border:none; outline:none; font-size:18px; padding:10px 0; background:transparent;}
                button {display:flex; align-items:center; justify-content:center; width:40px; height:40px; border:none; background:transparent; border-radius:50%; cursor:pointer;}
                button:hover {background:#f1f3f4;}
                .actions {margin-top:30px;}
                .actions a {margin:0 10px; padding:10px 20px; background:#e8eaed; color:#202124; text-decoration:none; border-radius:4px; font-size:14px;}
            </style>
        </head>
        <body>
            <h1>Web Proxy</h1>
            <div class="search-box">
                <form action="/" method="get">
                    <input type="text" name="url" placeholder="Digite o site" />
                    <button type="submit" aria-label="Acessar"><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="#4285F4"><path d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg></button>
                </form>
            </div>
            <div class="actions"><a href="/blocked">Sites Bloqueados</a><a href="/words">Alterar Filtros</a></div>
        </body>
    </html>
    """

# CSS das páginas (sites bloqueados e palavras filtradas)
page_style = """
    body {display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 100vh; margin: 0; font-family: Arial, sans-serif; background: #f8f9fa}

    .container {max-width: 600px; width: 90%; background: white;
    padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,.1)}

    h2 {margin-top: 0; color: #202124}
    ul {list-style: none; padding: 0}
    li {margin: 8px 0}
    a {color: #1a73e8; text-decoration: none}
    form {margin-top: 20px; display: flex; gap: 8px;}

    input[type=text] {flex: 1; padding: 8px;border: 1px solid #dadce0;border-radius: 4px}
    button {padding: 8px 12px; background: #4285F4; color: white; border: none; border-radius: 4px; cursor: pointer}
    .back {margin-top: 20px;}
"""

# Página de sites bloqueados
def blocked_sites_page(blocked_list):
    rows = "".join(
        f"<li>{escape(site)} <a href='/blocked/remove?site={quote(site)}'>Excluir</a></li>"
        for site in blocked_list
    )
    return f"""
    <html>
        <head>
            <title>Sites Bloqueados</title>
            <style>{page_style}</style>
        </head>
        <body>
            <div class="container">
                <h2>Lista de Sites Bloqueados</h2>
                <ul>{rows}</ul>
                <form action='/blocked/add' method='post'>
                    <input type='text' name='site' placeholder='Novo site' />
                    <button type='submit'>Adicionar</button>
                </form>
                <div class="back"><a href="/">Voltar à Busca</a></div>
            </div>
        </body>
    </html>
    """


# Página de palavras filtradas
def filter_words_page(words_dict):
    """Página de gerenciamento das palavras de filtro."""
    rows = "".join(
        f"<li>{escape(bw)} → {escape(rw)} <a href='/words/remove?word={quote(bw)}'>Excluir</a></li>"
        for bw, rw in words_dict.items()
    )
    return f"""
    <html>
        <head>
            <title>Palavras de Filtro</title>
            <style>{page_style}</style>
        </head>
        <body>
            <div class="container">
                <h2>Palavras de Filtro</h2>
                <ul>{rows}</ul>
                <form action='/words/add' method='post'>
                    <input type='text' name='blocked' placeholder='Palavra bloqueada' />
                    <input type='text' name='replace' placeholder='Substituir por' />
                    <button type='submit'>Adicionar</button>
                </form>
                <div class="back"><a href="/">Voltar à Busca</a></div>
            </div>
        </body>
    </html>
    """