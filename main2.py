import sys
import os
import database
from queries import QUERIES
# import epub_reader e nltk se forem usados no bloco de report

def principal():
    # 1. TRATAMENTO DO --list
    if len(sys.argv) < 2:
        print("❌ Uso: python3 main.py <nome_da_query> ou python3 main.py --list")
        return

    query_name = sys.argv[1]

    if query_name == "--list":
        print("\n📋 Queries disponíveis:")
        for nome, dados in QUERIES.items():
            print(f"  - {nome} ({dados.get('type', 'sem tipo')})")
        return

    if query_name not in QUERIES:
        print(f"❌ Query '{query_name}' não encontrada no arquivo queries.py.")
        return

    # Pega o tipo da query (corpus ou report)
    query_type = QUERIES[query_name].get("type", "corpus")

    # =================================================================
    # FLUXO 1: CORPUS (Apenas Banco de Dados, direto e rápido)
    # =================================================================
    if query_type == "corpus":
        print(f"\n[+] Executando busca de Corpus para: {query_name}")
        caminhos_validos = database.get_books(query_name)
        
        if not caminhos_validos:
            print("❌ Nenhum arquivo físico encontrado para este corpus.")
            return
            
        print(f"✅ Sucesso! Encontrados {len(caminhos_validos)} arquivos válidos para o corpus.")
        for path in caminhos_validos:
            print(f"  -> {os.path.basename(path)}")
        return  # Finaliza aqui, sem passar pela análise pesada

    # =================================================================
    # FLUXO 2: REPORT (Processamento Estatístico / NLTK)
    # =================================================================
    elif query_type == "report":
        print(f"\n[+] Executando Relatório Avançado para: {query_name}")
        caminhos_validos = database.get_books(query_name)
        
        if not caminhos_validos:
            print("❌ Nenhum arquivo encontrado para gerar o relatório.")
            return

        # Aqui entra a sua lógica pesada do NLTK que limita os livros,
        # extrai o texto com epub_reader e monta os gráficos/tabelas.
        print(f"📊 Analisando {len(caminhos_validos)} livros com NLTK...")
        # (Seu código antigo de extração e menu do NLTK entra aqui)

if __name__ == "__main__":
    principal()