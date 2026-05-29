import json
from datetime import datetime 
import re 

# Logs
def create_log(url, action):
    with open("log.json", "a", encoding="utf-8") as f:

        log = {
            "id": "req" + datetime.now().strftime("%H%M%S%f"),
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "url": url,
            "acao": action}
        
        f.write(json.dumps(log, ensure_ascii=False) + "\n")


# Filtro palavrões
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
        <body style="
            font-family: Arial;
            background-color: #111;
            color: white;
            text-align: center;
            padding: 60px;
        ">
            <img src="https://img.icons8.com/?size=100&id=63652&format=png&color=000000"
            style="width: 100px; margin-top: 10px;">

            <h1 style="color: red;">Acesso Bloqueado</h1>
            <p>O site <b>{url}</b> foi bloqueado pelo proxy.</p>
        </body>
    </html>
    """
