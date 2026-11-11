from flask import Flask, Response, request, redirect
import requests
import json
from urllib.parse import urlparse
import re
from utils import (
    create_log, filter_content, blocked_page, load_blocked_sites, load_filter_words, 
    home_page, blocked_sites_page, filter_words_page)

app = Flask(__name__)

# Tela inicial
@app.route('/')
def home():
    target_url = request.args.get('url')
    if target_url:
        return proxy(target_url)
    return home_page()

# Proxy
@app.route('/<path:url>')
def proxy(url):
    # Lê os arquivos json a cada requisição
    filter_words = load_filter_words()
    blocked_list = load_blocked_sites()

    # Valida url
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed_url = urlparse(url)

    if not parsed_url.scheme or not parsed_url.netloc:
        return "URL inválida", 400

    site = parsed_url.netloc
    normalize_site = site.lower().removeprefix("www.")
    blocked_norm = [s.lower().removeprefix("www.") for s in blocked_list]

    # Site bloqueado
    if normalize_site in blocked_norm:
        create_log(url, 'bloqueado')
        return Response(blocked_page(site))

    # Requisição ao servidor
    try:
        response = requests.get(url)
        html_content = response.text
        blocked_word = any(re.search(re.escape(word), html_content, re.IGNORECASE) for word in filter_words)

        # Site filtrado
        if blocked_word:
            filter_html = filter_content(html_content, filter_words)
            create_log(url, 'filtrado')
            return Response(filter_html, content_type=response.headers.get("Content-Type", "text/html"))

        # Modo transparente
        create_log(url, 'permitido')
        return Response(html_content, content_type=response.headers.get("Content-Type", "text/html"))
    except Exception as e:
        return f"Erro ao acessar URL: {str(e)}", 500


# Sites bloqueados
@app.route('/blocked')
def blocked_sites():
    return blocked_sites_page(load_blocked_sites())


@app.route('/blocked/add', methods=['POST'])
def blocked_add():
    site = request.get('site', '').strip()
    if site:
        sites = load_blocked_sites()
        if site not in sites:
            sites.append(site)
            with open("blocked.json", "w", encoding="utf-8") as f:
                json.dump({"bloqueados": sites}, f, ensure_ascii=False, indent=4)
    return redirect('/blocked')


@app.route('/blocked/remove')
def blocked_remove():
    site = requests.get('site')
    if site:
        sites = load_blocked_sites()
        if site in sites:
            sites.remove(site)
            with open("blocked.json", "w", encoding="utf-8") as f:
                json.dump({"bloqueados": sites}, f, ensure_ascii=False, indent=4)
    return redirect('/blocked')


# Palavras de filtro
@app.route('/words')
def words_page():
    return filter_words_page(load_filter_words())


@app.route('/words/add', methods=['POST'])
def words_add():
    blocked = request.form.get('blocked', '').strip()
    replace = request.form.get('replace', '').strip()
    if blocked and replace:
        words = load_filter_words()
        words[blocked] = replace
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=4)
    return redirect('/words')


@app.route('/words/remove')
def words_remove():
    word = requests.get('word')
    if word:
        words = load_filter_words()
        if word in words:
            del words[word]
            with open("words.json", "w", encoding="utf-8") as f:
                json.dump(words, f, ensure_ascii=False, indent=4)
    return redirect('/words')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)