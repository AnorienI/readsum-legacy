import sys
import os
import logging
from pathlib import Path

# Configuração e Supressão de Logs do NLTK
os.environ['NLTK_DATA'] = '/home/anorien/nltk_data'
import nltk
nltk.data.path.append('/home/anorien/nltk_data')
logging.getLogger('nltk').setLevel(logging.ERROR)

# Importações dos módulos do pipeline
import database
import epub_reader
import analysis  
import exporter
from queries import QUERIES

# Menu de opções original do NLTK
MENU_OPTIONS = {
    "1": ("Top 20 substantivos mais comuns",        lambda textos: analysis.contar_apenas_substantivos(textos, n=20)),
    "2": ("Top 20 verbos mais comuns",              lambda textos: analysis.contar_por_pos(textos, pos='VB', n=20)),
    "3": ("Top 20 adjetivos mais comuns",           lambda textos: analysis.contar_por_pos(textos, pos='JJ', n=20)),
    "4": ("Palavras mais longas (top 20)",          lambda textos: analysis.palavras_mais_longas(textos, n=20)),
    "5": ("Frases mais longas (top 10)",            lambda textos: analysis.frases_mais_longas(textos, n=10)),
    "6": ("Palavras únicas (hapax legomena)",       lambda textos: analysis.hapax_legomena(textos, n=20)),
    "7": ("Densidade lexical",                      lambda textos: analysis.densidade_lexical(textos)),
    "8": ("Sair", None),
}

def exibir_menu(query_name):
    print("\n" + "="*45)
    print(f"   READSUM — {query_name.upper()}")
    print("="*45)
    for key, (label, _) in MENU_OPTIONS.items():
        print(f"  {key}. {label}")
    print("="*45)
    return input("Escolha uma opção: ")

def main():
    # 1. Tratamento e validação dos argumentos de entrada
    if len(sys.argv) < 2:
        print("❌ Uso: python3 main.py <nome_da_query> ou python3 main.py --list")
        return

    query_name = sys.argv[1]

    # Intercepta o --list antes de tocar no banco de dados para evitar KeyError
    if query_name == "--list":
        print("\n📋 Queries e Corpora Disponíveis:")
        print("-" * 50)
        for nome, dados in QUERIES.items():
            q_type = dados.get('type', 'corpus')
            desc = dados.get('description', 'Sem descrição disponível.')
            print(f"  🔹 {nome:<20} | Tipo: {q_type:<6} | {desc}")
        print("-" * 50)
        return

    if query_name not in QUERIES:
        print(f"❌ Query '{query_name}' não encontrada no arquivo queries.py.")
        return

    # 2. Busca todos os arquivos cadastrados e válidos (Retorna tuplas de caminho e título)
    caminhos_validos = database.get_books(query_name)
    if not caminhos_validos:
        print("❌ Nenhum arquivo físico correspondente foi encontrado.")
        return

    print(f"\n[+] Executando: '{query_name}'")
    print(f"✅ Encontrados {len(caminhos_validos)} arquivos válidos vinculados no disco.")
    
    # Listagem inicial dos livros encontrados com seus IDs e títulos reais
    # Listagem inicial dos livros encontrados com seus IDs e títulos reais
    print("-" * 75)
    for livro in caminhos_validos:
        # Verifica se o retorno é uma string pura (apenas o caminho do arquivo)
        if isinstance(livro, str):
            path = livro
            # Como não veio título do banco, usamos o nome do arquivo limpo como título temporário
            titulo = os.path.basename(path).replace(".epub", "").capitalize()
        else:
            # Se for uma tupla/lista do banco de dados, extrai com segurança
            path = livro[-1]
            titulo = livro[1] if len(livro) > 1 else os.path.basename(path).replace(".epub", "")

        id_gutenberg = os.path.basename(path).replace(".epub", "")
        print(f"  -> [{id_gutenberg:<6}] {titulo}")
    print("-" * 75)

    # 3. Extração de Texto de TODOS os livros encontrados (Sem limite de 5)
    # 3. Extração de Texto de TODOS os livros encontrados
    print(f"\n⏳ Extraindo texto de todos os {len(caminhos_validos)} livro(s)...")
    
    textos = []
    for i, livro in enumerate(caminhos_validos, start=1):
        # Mesma checagem segura para o caminho e título
        if isinstance(livro, str):
            path = livro
            titulo = os.path.basename(path).replace(".epub", "").capitalize()
        else:
            path = livro[-1]
            titulo = livro[1] if len(livro) > 1 else os.path.basename(path).replace(".epub", "")
        
        print(f"  [{i}/{len(caminhos_validos)}] Processando: {titulo[:45]}...", end="", flush=True)
        
        texto_extraido = epub_reader.extract_text(path)
        if texto_extraido:
            textos.append(texto_extraido)
            print(" PRONTO!")
        else:
            print(" FALHOU!")
    if not textos:
        print("❌ Falha crítica: Nenhum texto válido pôde ser extraído dos ePubs.")
        return

    # 4. Loop interativo universal do menu
    while True:
        opcao = exibir_menu(query_name)
        
        if opcao not in MENU_OPTIONS:
            print("❌ Opção inválida.")
            continue
            
        label, func = MENU_OPTIONS[opcao]
        
        if func is None or opcao == "8":  # Sair
            break
            
        print(f"\n⏳ Executando análise estatística: {label}...")
        resultado = func(textos)
        
        print(f"\n=== {label.upper()} ===")
        
        # Tratamento de exibição para formatos diferentes (Densidade Lexical vs Listas de Frequência)
        if isinstance(resultado, list):
            for item, freq in resultado:
                print(f"  {item:<25} : {freq}")
            
            # Sistema de exportação CSV original
            salvar = input("\nExportar resultado para CSV? (s/n): ").lower().strip()
            if salvar == 's':
                nome = exporter.get_next_filename(base=f"readsum_{query_name}_{opcao}")
                exporter.exportar_top_palavras_csv(resultado, nome_arquivo=nome)
        else:
            # Exibição direta caso o retorno seja um valor único/float (Ex: Densidade Lexical)
            print(f"  Resultado: {resultado}")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()