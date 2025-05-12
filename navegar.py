import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url_inicial = "https://luna0812y.github.io/Buscador/paginas/matrix.html"

visitadas = set()
dados_paginas = {}

# Função para ler também os arquivo do head de index.html
def extrair_metadados(soup):
    """Extrai os conteúdos dos atributos 'content' das tags <meta>."""
    metadados = []
    for meta in soup.find_all('meta'):
        content = meta.get('content')
        if content:
            metadados.append(content.lower())
    return " ".join(metadados)

def mesmo_dominio(url1, url2):
    """
    Verifica se duas URLs pertencem ao mesmo domínio.
    """
    dominio1 = urlparse(url1).netloc
    dominio2 = urlparse(url2).netloc
    return dominio1 == dominio2

# Função para visitar páginas dinamicamente
def crawler(url_raiz):
    fila = [url_raiz]

    while fila:
        url = fila.pop(0)
        if url in visitadas:
            continue

        try:
            resposta = requests.get(url)
            if resposta.status_code != 200:
                print(f"[!] Falha ao acessar {url} (status {resposta.status_code})")
                continue
        except Exception as e:
            print(f"[!] Erro ao acessar {url}: {e}")
            continue

        soup = BeautifulSoup(resposta.text, 'html.parser')
        meta_text = extrair_metadados(soup)
        title = soup.title.string.lower() if soup.title and soup.title.string else ''
        body_text = soup.body.get_text(separator=' ', strip=True).lower() if soup.body else ''
        texto = title + " " + meta_text + " " + body_text

        links = []
        for a in soup.find_all('a', href=True):
            link_completo = urljoin(url, a['href'])
            if mesmo_dominio(url, link_completo):
                links.append(link_completo)
                if link_completo not in visitadas and link_completo not in fila:
                    fila.append(link_completo)

        dados_paginas[url] = {
            'texto': texto,
            'links': links
        }

        visitadas.add(url)
        print(f"[✔] Visitado: {url}")

crawler(url_inicial)

def computar_autoridade():
    for origem, dados in dados_paginas.items():
        for destino in dados['links']:
            if destino in dados_paginas:
                if 'recebe_de' not in dados_paginas[destino]:
                    dados_paginas[destino]['recebe_de'] = set()
                dados_paginas[destino]['recebe_de'].add(origem)

computar_autoridade()