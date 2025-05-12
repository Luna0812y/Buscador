import re
import navegar
from tabulate import tabulate

# Função para buscar o termo na página e contar a frequência
def contar_ocorrencias(termo, texto):
    return len(re.findall(termo, texto, flags=re.IGNORECASE))  # Ignora maiúsculas/minúsculas

# Função para calcular a pontuação de cada página com base nos critérios
def calcular_pontuacao(termo, url, dados):
    # Contagem de termos
    termos_pontos = contar_ocorrencias(termo, dados['texto']) * 10
    
    # Contagem de links recebidos
    links_pontos = len(dados.get('recebe_de', [])) * 10
    
    # Penalidade por autoreferência
    autoreferente_pontos = -15 if url in dados['links'] else 0
    
    # Cálculo da pontuação final
    pontuacao_total = termos_pontos + links_pontos + autoreferente_pontos
    
    return {
        'url': url,
        'termos_pontos': termos_pontos,
        'links_pontos': links_pontos,
        'autoreferente_pontos': autoreferente_pontos,
        'pontuacao_total': pontuacao_total
    }

# Função para ranquear as páginas com base na pontuação
def ranquear_paginas(termo):
    pontuacoes = []
    
    for url, dados in navegar.dados_paginas.items():
        # Calcula a pontuação de cada página
        pontuacao = calcular_pontuacao(termo, url, dados)
        pontuacoes.append(pontuacao)

    # Ordena as páginas pela pontuação total e pelos critérios de desempate
    pontuacoes.sort(key=lambda x: (
        x['pontuacao_total'],
        -len(navegar.dados_paginas[x['url']]['links']),  # Maior número de links recebidos
        -contar_ocorrencias(termo, navegar.dados_paginas[x['url']]['texto']),  # Maior quantidade de termos encontrados
        x['autoreferente_pontos']  # Penalidade por autoreferência
    ), reverse=True)
    
    return pontuacoes

# Função para exibir o ranking de forma amigável
def exibir_ranking(pontuacoes):
    headers = ["Página", "Termos", "Links", "Autorreferência", "Pontuação", "Total"]
    tabela = []

    for pontuacao in pontuacoes:
        linha = [
            pontuacao['url'],
            pontuacao['termos_pontos'],
            pontuacao['links_pontos'],
            pontuacao['autoreferente_pontos'],
            pontuacao['pontuacao_total'],
            pontuacao['pontuacao_total']  # Repetido como no seu exemplo
        ]
        tabela.append(linha)

    print("\nRanking das páginas:\n")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))


# Exemplo de busca por "Matrix"
termo_busca = "Matrix"
pontuacoes = ranquear_paginas(termo_busca)
exibir_ranking(pontuacoes)
