# main2.py
import database
import epub_reader
import analysis  # <--- O seu novo motor com NLTK
import exporter
import sys
import nltk
import os
os.environ['NLTK_DATA'] = '/home/anorien/nltk_data'  # already downloaded
nltk.data.path.append('/home/anorien/nltk_data')

# Suppress download messages
import logging
logging.getLogger('nltk').setLevel(logging.ERROR)

query_name = sys.argv[1] if len(sys.argv) > 1 else "ancient"

caminhos_validos = database.get_books(query_name)
if not caminhos_validos:
    print("❌ Nenhum arquivo encontrado.")
    sys.exit(1) 

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
    query_name = sys.argv[1] if len(sys.argv) > 1 else "ancient"
    caminhos_validos = database.get_books(query_name)
    if not caminhos_validos:
        print("❌ Nenhum arquivo encontrado.")
        return

    caminhos_teste = caminhos_validos[:4]
    print(f"\n[+] Extraindo texto de {len(caminhos_teste)} livros...")
    textos = [epub_reader.extract_text(c) for c in caminhos_teste if epub_reader.extract_text(c)]

    while True:
        opcao = exibir_menu(query_name)
        
        if opcao not in MENU_OPTIONS:
            print("❌ Opção inválida.")
            continue
            
        label, func = MENU_OPTIONS[opcao]
        
        if func is None:  # Sair
            break
            
        print(f"\n⏳ Processando: {label}...")
        resultado = func(textos)
        
        print(f"\n=== {label.upper()} ===")
        for item, freq in resultado:
            print(f"{item:<25} : {freq}")
            
        salvar = input("\nExportar? (s/n): ").lower().strip()
        if salvar == 's':
            nome = exporter.get_next_filename(base=f"readsum_{query_name}_{opcao}")
            exporter.exportar_top_palavras_csv(resultado, nome_arquivo=nome)


   
                
        elif opcao == "2":
            break

if __name__ == "__main__":
    main()