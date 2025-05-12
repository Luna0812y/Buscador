import re
import navegar
from tabulate import tabulate

# Pesos
PESO_TERMO = 5
PESO_LINK_RECEBIDO = 10
PESO_AUTOREFERENCIA = -15

# Conta quantas vezes o termo aparece como palavra inteira
def contar_ocorrencias(termo, texto):
    padrao = r'\b' + re.escape(termo.lower()) + r'\b'
    return len(re.findall(padrao, texto))

def calcular_pontuacao(termo, url, dados):
    ocorrencias = contar_ocorrencias(termo, dados['texto'])
    pontos_termo = ocorrencias * PESO_TERMO

    links_recebidos = len(dados.get('recebe_de', set()))
    pontos_links = links_recebidos * PESO_LINK_RECEBIDO

    autorreferente = url in dados.get('links', [])
    pontos_autorreferencia = PESO_AUTOREFERENCIA if autorreferente else 0

    total = pontos_termo + pontos_links + pontos_autorreferencia

    return {
        'url': url,
        'termos_pontos': pontos_termo,
        'links_pontos': pontos_links,
        'autoreferente_pontos': pontos_autorreferencia,
        'total': total
    }

def ranquear_paginas(termo):
    resultados = []
    for url, dados in navegar.dados_paginas.items():
        pontuacao = calcular_pontuacao(termo, url, dados)
        resultados.append(pontuacao)

    resultados.sort(key=lambda x: x['total'], reverse=True)
    return resultados

def exibir_ranking(pontuacoes):
    headers = ["Posição", "Página", "Termos", "Links", "Autorreferência", "Total"]
    tabela = []

    for i, p in enumerate(pontuacoes, start=1):
        linha = [
            i,
            p['url'].split("/")[-1],
            p['termos_pontos'],
            p['links_pontos'],
            p['autoreferente_pontos'],
            p['total']
        ]
        tabela.append(linha)

    print("\nRanking das páginas:\n")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    termo = input("🔎 Digite o termo para buscar: ").strip().lower()
    resultado = ranquear_paginas(termo)
    exibir_ranking(resultado)
