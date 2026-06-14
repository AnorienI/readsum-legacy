# renamer_seguro.py
import mysql.connector
from pathlib import Path
import re

BOOKS_DIR = Path("/home/anorien/Área de trabalho/gutenberg_history")

def limpar_nome_arquivo(nome):
    """Remove caracteres que o Linux ou o sistema de arquivos não gostam em nomes."""
    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome)  # Remove caracteres inválidos
    nome_limpo = nome_limpo.replace(" – ", " - ").replace(" — ", " - ")
    return nome_limpo.strip()

def sincronizar_e_renomear():
    # Conecta direto ao seu banco books
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='books'
    )
    cursor = conn.cursor()
    
    # Puxa o ID e o Título do banco
    query = "SELECT gutenberg_id, title FROM history_books_ancient"
    cursor.execute(query)
    livros = cursor.fetchall()
    
    print(f"Iniciando verificação de {len(livros)} registros no banco...\n")
    
    arquivos_renomeados = 0
    arquivos_ignorados = 0
    
    for gutenberg_id, title in livros:
        # Define o nome antigo padrão (ex: 2707.epub)
        nome_antigo_padrao = f"{gutenberg_id}.epub"
        caminho_antigo = BOOKS_DIR / nome_antigo_padrao
        
        # Se o arquivo ID.epub existe, significa que ele escapou da renomeação anterior!
        if caminho_antigo.exists():
            titulo_limpo = limpar_nome_arquivo(title)
            
            # Padrão recomendado: "ID - Titulo.epub" (mantém o ID fácil de achar e o título legível)
            novo_nome = f"{gutenberg_id} - {titulo_limpo}.epub"
            caminho_novo = BOOKS_DIR / novo_nome
            
            try:
                caminho_antigo.rename(caminho_novo)
                print(f"✅ Renomeado: {nome_antigo_padrao} ➔ {novo_nome}")
                arquivos_renomeados += 1
            except Exception as e:
                print(f"❌ Erro ao renomear {nome_antigo_padrao}: {e}")
        else:
            # Se o 2707.epub não existe, ele já deve estar com o nome correto ou não foi baixado
            arquivos_ignorados += 1

    cursor.close()
    conn.close()
    
    print("\n" + "="*40)
    print("Fim do processo de renomeação segura!")
    print(f"Livros atualizados agora: {arquivos_renomeados}")
    print(f"Livros já atualizados ou não encontrados: {arquivos_ignorados}")

if __name__ == "__main__":
    sincronizar_e_renomear()