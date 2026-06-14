# downloader.py
import requests
import mysql.connector
from pathlib import Path
import time

DOWNLOAD_DIR = Path("/home/anorien/Área de trabalho/gutenberg")
DOWNLOAD_DIR.mkdir(exist_ok=True)

db = mysql.connector.connect(
    host='localhost', user='root', password='', database='history'
)
cursor = db.cursor()

tables = ['ancient', 'american', 'european', 'religious', 'medieval', 'universities', 'archaeology']

total_downloaded = 0
total_skipped = 0
total_failed = 0

for table in tables:
    cursor.execute(f"SELECT gutenberg_id, title FROM {table} WHERE gutenberg_id IS NOT NULL")
    books = cursor.fetchall()
    print(f"\n[+] {table}: {len(books)} books to check")

    for gutenberg_id, title in books:
        epub_path = DOWNLOAD_DIR / f"{gutenberg_id}.epub"

        if epub_path.exists():
            print(f"  ⏭️  Already exists: {gutenberg_id}")
            total_skipped += 1
            continue

        url = f"https://www.gutenberg.org/ebooks/{gutenberg_id}.epub.noimages"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                epub_path.write_bytes(response.content)
                print(f"  ✅ {gutenberg_id} - {title[:50]}")
                total_downloaded += 1
            else:
                print(f"  ❌ {gutenberg_id} - HTTP {response.status_code}")
                total_failed += 1
        except Exception as e:
            print(f"  ❌ {gutenberg_id} - {e}")
            total_failed += 1

        time.sleep(2)

cursor.close()
db.close()

print(f"\n{'='*40}")
print(f"✅ Downloaded : {total_downloaded}")
print(f"⏭️  Skipped    : {total_skipped}")
print(f"❌ Failed     : {total_failed}")
print(f"{'='*40}")