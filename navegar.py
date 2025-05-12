import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URLs das 5 páginas fornecidas
urls_iniciais = [
    "https://seuusuario.github.io/nomedoprojeto/blade_runner.html",
    "https://seuusuario.github.io/nomedoprojeto/duna.html",
    "https://seuusuario.github.io/nomedoprojeto/matrix.html",
    "https://seuusuario.github.io/nomedoprojeto/interestellar.html",
    "https://seuusuario.github.io/nomedoprojeto/mochileiro.html"
]

# Estruturas de dados globais
visitadas = set()
dados_paginas = {}

# Função para rodar o crawler
def crawler(url_inicial):
    fila = [url_inicial]  # Inicia a fila com a URL inicial

    while fila:
        url = fila.pop(0)  # Pega a primeira URL da fila
        if url in visitadas:
            continue  # Se já foi visitada, pula para a próxima

        try:
            resposta = requests.get(url)
            if resposta.status_code != 200:
                print(f"[!] Falha ao acessar {url} (status {resposta.status_code})")
                continue
        except Exception as e:
            print(f"[!] Erro ao acessar {url}: {e}")
            continue

        # Processa o conteúdo da página
        soup = BeautifulSoup(resposta.text, 'html.parser')
        texto = soup.get_text().lower()  # Pega o texto da página
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]  # Extrai links

        # Armazena os dados da página
        dados_paginas[url] = {
            'texto': texto,
            'links': links
        }

        visitadas.add(url)  # Marca a URL como visitada

        # Adiciona os links à fila para processamento
        for link in links:
            if link not in visitadas:
                fila.append(link)

# Inicia o crawler para cada página fornecida
for url in urls_iniciais:
    crawler(url)

# Função para mapear as páginas que apontam para cada uma
def computar_autoridade():
    for origem, dados in dados_paginas.items():
        for destino in dados['links']:
            if destino in dados_paginas:
                if 'recebe_de' not in dados_paginas[destino]:
                    dados_paginas[destino]['recebe_de'] = set()
                dados_paginas[destino]['recebe_de'].add(origem)

# Mapeia a autoridade das páginas
computar_autoridade()

# Exibe os dados das páginas para verificação
for url, dados in dados_paginas.items():
    print(f"\nPágina: {url}")
    print(f"Texto: {dados['texto'][:200]}...")  # Exibe os primeiros 200 caracteres do texto
    print(f"Links: {dados['links']}")
    print(f"Recebe de: {dados.get('recebe_de', 'Nenhum link apontando para ela')}")
