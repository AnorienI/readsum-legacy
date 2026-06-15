import re
from collections import Counter
import nltk

# Você só precisa rodar essas duas linhas UMA vez na vida para baixar os dicionários gramaticais
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('averaged_perceptron_tagger_eng', quiet=True)# Baixa a versão em inglês mais recente para garantir
 

def contar_apenas_substantivos(lista_textos, n=20):
    counter = Counter()
    
    for texto in lista_textos:
        if not texto:
            continue
            
        # 1. O NLTK precisa tokenizar o texto (separar em palavras mantendo a estrutura da frase)
        palavras = nltk.word_tokenize(texto.lower())
        
        # 2. O POS Tagger analisa o contexto e retorna tuplas: ('history', 'NN'), ('ancient', 'JJ')
        # 'NN' significa Noun (Substantivo) e 'JJ' significa Adjective (Adjetivo)
        palavras_classificadas = nltk.pos_tag(palavras)
        
        # 3. Filtramos apenas o que nos interessa
        substantivos = [
            palavra for palavra, tag in palavras_classificadas
            if tag in ('NN', 'NNS', 'NNP', 'NNPS') and palavra.isalpha() and len(palavra) > 2
        ]
        
        counter.update(substantivos)

        return counter.most_common(n)
        

def contar_por_pos(lista_textos, pos='VB', n=20):
    """Conta palavras por categoria gramatical. pos='VB' verbos, 'JJ' adjetivos etc."""
    # POS tags para verbos: VB, VBD, VBG, VBN, VBP, VBZ
    # POS tags para adjetivos: JJ, JJR, JJS
    pos_map = {
        'VB': ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'),
        'JJ': ('JJ', 'JJR', 'JJS'),
    }
    tags_alvo = pos_map.get(pos, (pos,))
    counter = Counter()

    for texto in lista_textos:
        if not texto:
            continue
        palavras = nltk.word_tokenize(texto.lower())
        palavras_classificadas = nltk.pos_tag(palavras)
        filtradas = [
            palavra for palavra, tag in palavras_classificadas
            if tag in tags_alvo and palavra.isalpha() and len(palavra) > 2
        ]
        counter.update(filtradas)

    return counter.most_common(n)


def palavras_mais_longas(lista_textos, n=20):
    """Retorna as palavras únicas mais longas encontradas nos textos."""
    todas = set()

    for texto in lista_textos:
        if not texto:
            continue
        palavras = nltk.word_tokenize(texto.lower())
        todas.update(p for p in palavras if p.isalpha() and len(p) > 4 and p.isascii())

    ordenadas = sorted(todas, key=len, reverse=True)[:n]
    # Returns (palavra, length) to fit the display loop in main.py
    return [(p, len(p)) for p in ordenadas]


def frases_mais_longas(lista_textos, n=10):
    """Retorna as frases mais longas por número de palavras."""
    todas = []

    for texto in lista_textos:
        if not texto:
            continue
        frases = nltk.sent_tokenize(texto)
        todas.extend(frases)

    ordenadas = sorted(todas, key=lambda f: len(f.split()), reverse=True)[:n]
    # Returns (frase_truncada, word_count) to fit the display loop
    return [(f[:80] + '...' if len(f) > 80 else f, len(f.split())) for f in ordenadas]


def hapax_legomena(lista_textos, n=20):
    """Palavras que aparecem apenas uma vez — indicador de riqueza vocabular."""
    counter = Counter()

    for texto in lista_textos:
        if not texto:
            continue
        palavras = nltk.word_tokenize(texto.lower())
        counter.update(p for p in palavras if p.isalpha() and len(p) > 3)

    hapax = [(palavra, freq) for palavra, freq in counter.items() if freq == 1]
    return hapax[:n]


def densidade_lexical(lista_textos):
    """Proporção de palavras de conteúdo (substantivos, verbos, adjetivos) vs total."""
    tags_conteudo = ('NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG',
                     'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS')
    total = 0
    conteudo = 0

    for texto in lista_textos:
        if not texto:
            continue
        palavras = nltk.word_tokenize(texto.lower())
        classificadas = nltk.pos_tag(palavras)
        total += len(classificadas)
        conteudo += sum(1 for _, tag in classificadas if tag in tags_conteudo)

    if total == 0:
        return [("Sem dados", 0)]

    densidade = round((conteudo / total) * 100, 2)
    # Returns list of tuples to fit the display loop in main.py
    return [("Total de palavras", total),
            ("Palavras de conteúdo", conteudo),
            ("Densidade lexical (%)", densidade)]


    