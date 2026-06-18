# database.py
import mysql.connector
from mysql.connector import Error
from pathlib import Path
import re
from queries import QUERIES
from dotenv import load_dotenv
import os

load_dotenv()

# O Path.home() detecta automaticamente o diretório do usuário atual (/home/nome_do_usuario)
BOOKS_DIR = Path.home() / "Área de trabalho" / "gutenberg"

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'history')
    )
        return connection

    except Error as e:
        print(f"Erro ao conectar ao MariaDB: {e}")
        return None

def limpar_texto(texto):
    """Remove caracteres especiais para facilitar a comparação de nomes."""
    if not texto:
        return ""
    texto = str(texto)  # <-- fix: garante que é string.
    return re.sub(r'[^a-zA-Z0-9]', '', texto).lower()

def get_books(query_name):

    connection = get_connection()

    if not connection:
        return []

    try:
        cursor = connection.cursor()

        query = QUERIES[query_name]["sql"]

        cursor.execute(query)

       
        resultados = cursor.fetchall()


        caminhos_validos = []
        
        # Listamos todos os arquivos .epub que realmente existem na sua pasta física
        arquivos_reais = list(BOOKS_DIR.glob("*.epub"))
        
        
        for gutenberg_id, title in resultados:
            id_str = str(gutenberg_id)
            titulo_limpo = limpar_texto(title)
            
            arquivo_encontrado = None
            
            # Varre os arquivos do HD procurando pelo ID ou pelo Título
            for arquivo in arquivos_reais:
                nome_arquivo_limpo = limpar_texto(arquivo.name)
                
                # Condição 1: O arquivo começa com o ID (ex: 2707...)
                # Condição 2: O nome do arquivo contém o título do livro
                if arquivo.name.startswith(id_str) or (titulo_limpo and titulo_limpo in nome_arquivo_limpo):
                    arquivo_encontrado = arquivo
                    break
            
            # Só adicionamos à lista se o arquivo REALMENTE existir no HD
            if arquivo_encontrado and arquivo_encontrado.exists():
                caminhos_validos.append(str(arquivo_encontrado))
                
    except Error as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            
    return caminhos_validos


def run_report(query_name):

    connection = get_connection()

    if not connection:
        return []

    try:
        cursor = connection.cursor()

        query = QUERIES[query_name]["sql"]

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()