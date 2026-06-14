# exporter.py
import csv
from pathlib import Path

RAIZ_PROJETO = Path(__file__).parent
PASTA_OUTPUTS = RAIZ_PROJETO / "outputs"

def get_next_filename(base="readsum", ext=".csv"):
    """Returns next available filename with incrementing number."""
    PASTA_OUTPUTS.mkdir(parents=True, exist_ok=True)
    i = 1
    while (PASTA_OUTPUTS / f"{base}_{i}{ext}").exists():
        i += 1
    return f"{base}_{i}{ext}"

def exportar_top_palavras_csv(dados, nome_arquivo=None):
    PASTA_OUTPUTS.mkdir(parents=True, exist_ok=True)

    if not nome_arquivo:
        nome_arquivo = get_next_filename()  # consistent incrementing instead of timestamp

    caminho_final = PASTA_OUTPUTS / nome_arquivo


    try:
        with open(caminho_final, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor = csv.writer(arquivo, delimiter=';')
            escritor.writerow(['Palavra', 'Frequência'])
            for palavra, freq in dados:
                escritor.writerow([palavra, freq])

        print(f"\n✅ Exportado com sucesso!")
        print(f"📂 Salvo em: {caminho_final}")
        return str(caminho_final)

    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")
        return None