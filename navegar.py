import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

url_inicial = "https://luna0812y.github.io/Buscador/paginas/matrix.html"

visitadas = set()
dados_paginas = {}

def mesmo_dominio(url_base, url_destino):
    """Garante que o link é interno (do mesmo domínio base)."""
    base = urlparse(url_base)
    destino = urlparse(url_destino)
    return base.netloc == destino.netloc

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
        texto = soup.get_text().lower()
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