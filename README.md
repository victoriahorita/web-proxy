# Web Proxy

Projeto desenvolvido para a disciplina de Sistemas para Internet II, que consiste na implementação de um Web Proxy com controle de conteúdo. O proxy atua como intermediário entre o cliente e os servidores da web, recebendo requisições HTTP e decidindo entre:

* Permitir o acesso ao conteúdo;
* Bloquear sites presentes em uma lista negra;
* Filtrar palavras impróprias do conteúdo HTML antes de entregá-lo ao cliente.



## Justificativa da tecnologia escolhida

O projeto foi desenvolvido utilizando Python com Flask.

A escolha do Flask foi feita por ser um framework simples e leve, facilitando a criação rápida de rotas HTTP e a manipulação de requisições e respostas. Além disso, já possuía familiaridade com a linguagem Python, o que tornou o desenvolvimento mais prático e permitiu maior foco na compreensão do funcionamento do protocolo HTTP e da lógica do proxy.

### Vantagens 

* Facilidade de desenvolvimento;
* Código mais organizado e legível;
* Integração simples com JSON;
* Facilidade para testar o proxy localmente.

### Dificuldades 

* Manipulação correta do conteúdo HTML;
* Tratamento de diferentes formatos de resposta.


## Estrutura de pastas

```bash
web-proxy/
│
├── blocked.json            # lista de sites bloqueados
├── log.json                # registro das requisições realizadas
├── main.py                 # arquivo principal do proxy
├── requirements.txt        # dependências do projeto
├── utils.py                # funções auxiliares
├── words.json              # palavras que serão substituídas

````

## Instalação das dependências

### 1. Clonar o repositório

```bash
git clone https://github.com/victoriahorita/web-proxy
```

### 2. Entrar na pasta do projeto

```bash
cd web-proxy
```

### 3. Criar ambiente virtual

Linux/WSL:

```bash
python3 -m venv venv
```

Windows:

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

Linux/WSL:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

## Como executar o proxy

Executar o arquivo principal:

```bash
python main.py
```

O servidor será iniciado em:

```txt
http://localhost:5000
```


## Configuração dos arquivos JSON

O proxy utiliza dois arquivos de configuração:

* `blocked.json`: contém a lista de domínios bloqueados.
* `words.json`: contém as palavras que serão filtradas no conteúdo das páginas.

### Adicionando ou Removendo Sites Bloqueados

Para bloquear ou desbloquear um site, basta editar o arquivo `blocked.json` e adicionar ou remover o domínio desejado.

Exemplo:

```json
{
    "bloqueados": [
        "google.com",
        "github.com",
        "lipsum.com"
    ]
}
```

### Adicionando ou Removendo Palavras Filtradas

Para adicionar ou remover palavras sujeitas à filtragem, edite o arquivo `words.json`.

Exemplo:

```json
{
    "proxy": "******",
    "teste": "******"
}
```

### Atualização Dinâmica das Configurações

As listas de sites bloqueados e palavras filtradas são carregadas a cada requisição processada pelo proxy. Após salvar alterações nos arquivos `blocked.json` ou `words.json`, as novas regras passam a ser utilizadas automaticamente nas próximas requisições, sem a necessidade de reiniciar o servidor.

A opção por utilizar arquivos JSON em vez de implementar endpoints de gerenciamento foi uma decisão de projeto. Como o objetivo principal do trabalho é o desenvolvimento e funcionamento do proxy HTTP, optou-se por uma solução mais simples para a administração das listas, mantendo o foco nas funcionalidades de bloqueio, filtragem e registro das requisições. Ainda assim, a solução permite a atualização dinâmica das regras durante a execução da aplicação.

## Exemplo de uso

Acessar um site através do proxy:

```txt
http://localhost:5000/www.lipsum.com/
```

Se o site estiver bloqueado, o proxy retorna uma página informando o bloqueio.

Se o conteúdo possuir palavras cadastradas em `words.json`, elas serão substituídas automaticamente.


## Tecnologias utilizadas

* Python
* Flask
* Requests
* JSON


## Documentações utilizadas

### Python e bibliotecas

* Flask
  https://flask.palletsprojects.com

* Requests
  https://requests.readthedocs.io

* urllib.parse
  https://docs.python.org/3/library/urllib.parse.html

### HTTP

* MDN Web Docs — HTTP
  https://developer.mozilla.org/pt-BR/docs/Web/HTTP


## Uso de Inteligência Artificial

Foi utilizada a ferramenta ChatGPT como apoio para:

* esclarecimento de dúvidas;
* organização do README;
* auxílio na compreensão do funcionamento do protocolo HTTP e Flask.