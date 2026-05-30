from flask import Flask, Response
import requests
from utils import create_log, filter_content, blocked_page, load_blocked_sites, load_filter_words
import json
from urllib.parse import urlparse
import re

app = Flask(__name__)

# Proxy
@app.route("/<path:url>")
def proxy(url):
    
    # Lê arquivos json a cada requisição
    filter_words = load_filter_words()
    blocked_list = load_blocked_sites()

    # Valida url
    if not url.startswith(("http://")):
        url = "http://" + url

    parsed_url = urlparse(url)

    if not parsed_url.scheme or not parsed_url.netloc:
        return "URL inválida", 400

    site = parsed_url.netloc


    # Site Bloqueado
    if site in blocked_list:
        create_log(url, 'bloqueado')
        return Response(blocked_page(site))
    
    # Requisição ao servidor
    try:
        response = requests.get(url)
        html_content = response.text

        # Site Filtrado
        blocked_word = False

        for word in filter_words:
            if re.search(re.escape(word), html_content, re.IGNORECASE):
                blocked_word = True
                break

        if blocked_word:
            filter_html = filter_content(html_content, filter_words)
            create_log(url, 'filtrado')

            return Response(
                filter_html,
                content_type=response.headers.get("Content-Type", "text/html")
            )

        # Modo transparente
        else:
            create_log(url, 'permitido')
            return Response(
                html_content,
                content_type=response.headers.get("Content-Type", "text/html")
            )

    except Exception as e:
        return f"Erro ao acessar URL: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)