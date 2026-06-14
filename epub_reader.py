# epub_reader.py
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text(file_path):
    """Abre o arquivo EPUB e extrai todo o texto limpo dele."""
    try:
        # Abre o EPUB usando a biblioteca ebooklib
        book = epub.read_epub(str(file_path), options={'ignore_extra': True})
        extracted_text = ""
        
        # Percorre as seções internas do livro (capítulos/páginas em HTML)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Remove as tags HTML e joga o texto limpo na string
                soup = BeautifulSoup(item.get_content(), "html.parser")
                extracted_text += soup.get_text() + " "
                
        return extracted_text
        
    except Exception as e:
        print(f"Erro ao ler o arquivo EPUB [{file_path}]: {e}")
        return ""