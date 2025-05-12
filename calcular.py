import re
import navegar
import csv
from tabulate import tabulate

# Pesos
PESO_TERMO = 5
PESO_LINK_RECEBIDO = 10
PESO_AUTOREFERENCIA = -15

def contar_ocorrencias(termo, texto):
    """Conta quantas vezes o termo aparece no texto como palavra inteira."""
    padrao = r'\b' + re.escape(termo.lower()) + r'\b'
    ocorrencias = len(re.findall(padrao, texto.lower()))
    # print(f"[DEBUG] Termo '{termo}' - Ocorrências: {ocorrencias}")
    return ocorrencias

def calcular_pontuacao(termo, url, dados):
    """Calcula a pontuação total da página com base nos critérios."""
    pontos_termo = contar_ocorrencias(termo, dados['texto']) * PESO_TERMO
    pontos_links = len(dados.get('recebe_de', set())) * PESO_LINK_RECEBIDO
    pontos_autorreferencia = PESO_AUTOREFERENCIA if url in dados.get('links', []) else 0

    total = pontos_termo + pontos_links + pontos_autorreferencia

    # print(f"[DEBUG] {url} - Termos: {pontos_termo}, Links: {pontos_links}, Autorreferência: {pontos_autorreferencia}, Total: {total}")

    return {
        'url': url,
        'termos_pontos': pontos_termo,
        'links_pontos': pontos_links,
        'autoreferente_pontos': pontos_autorreferencia,
        'total': total
    }

def ranquear_paginas(termo):
    """Avalia e ranqueia todas as páginas pelo termo."""
    resultados = []
    for url, dados in navegar.dados_paginas.items():
        pontuacao = calcular_pontuacao(termo, url, dados)
        if pontuacao['termos_pontos'] > 0:
            resultados.append(pontuacao)
    return sorted(resultados, key=lambda x: x['total'], reverse=True)

def salvar_resultados_csv(termo, resultados):
    """Salva os resultados da busca em um arquivo CSV."""
    nome_arquivo = f"resultados_{termo.replace(' ', '_')}.csv"
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Posição", "Página", "Termos", "Links", "Autorreferência", "Total"])
        for i, p in enumerate(resultados, start=1):
            writer.writerow([i, p['url'].split("/")[-1].lower(), p['termos_pontos'], p['links_pontos'], p['autoreferente_pontos'], p['total']])
    print(f"[✔] Resultados salvos no arquivo '{nome_arquivo}'.")

def exibir_ranking(resultados):
    """Exibe o ranking das páginas na tela."""
    if not resultados:
        print("\n⚠️ Nenhuma página contém o termo buscado.\n")
        return

    headers = ["Posição", "Página", "Termos", "Links", "Autorreferência", "Total"]
    tabela = [
        [i+1, r['url'].split("/")[-1].lower(), r['termos_pontos'], r['links_pontos'], r['autoreferente_pontos'], r['total']]
        for i, r in enumerate(resultados)
    ]
    print("\n📊 Ranking das páginas:\n")
    print(tabulate(tabela, headers=headers, tablefmt="grid"))

def buscar_e_exibir(termo):
    """Executa o processo completo para um termo."""
    print(f"\n🔎 Buscando pelo termo: '{termo}'")
    resultados = ranquear_paginas(termo)
    exibir_ranking(resultados)
    salvar_resultados_csv(termo, resultados)

if __name__ == "__main__":
    termos_iniciais = ['matrix', 'ficção científica', 'realidade', 'universo', 'viagem']

    for termo in termos_iniciais:
        buscar_e_exibir(termo)

    while True:
        termo_usuario = input("\n📝 Digite outro termo para buscar (ou 'sair' para encerrar): ").strip()

        if termo_usuario.lower() in ['sair', 'exit', 'q', 'quit']:
            print("👋 Encerrando o programa.")
            break
        elif termo_usuario:
            print(f"\n🔎 Buscando pelo termo: '{termo_usuario}'")
            resultados = ranquear_paginas(termo_usuario)
            exibir_ranking(resultados)
            
            if resultados:
                salvar = input("💾 Deseja salvar os resultados em CSV? (s/n): ").strip().lower()
                if salvar == 's':
                    salvar_resultados_csv(termo_usuario, resultados)
                else:
                    print("📂 Salvamento ignorado.")
