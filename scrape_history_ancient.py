import requests
from bs4 import BeautifulSoup
import mysql.connector
from urllib.parse import urljoin
import time
import re


# Connect to MariaDB
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='history'
)

cursor = db.cursor()

# Base URL for "History - Ancient" category
# base_url = 'https://www.gutenberg.org/ebooks'
base_url = 'https://www.gutenberg.org/ebooks/bookshelf/659'

start_index = 0
books_per_page = 25
total_inserted = 0

while True:
    url = f"{base_url}?start_index={start_index}"
    print(f"Fetching {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all book containers
    books = soup.select(".booklink")
    if not books:
        print("No more books found. Ending pagination.")
        break

    for book in books:
        title_tag = book.select_one(".title")
        title = title_tag.text.strip() if title_tag else 'No Title'
        if len(title) > 255:
            title = title[:252] + 'etc'  # Leave 3 characters for 'etc'

        # Language extraction logic
        # List of common languages to match against
        known_languages = [
        'English', 'French', 'German', 'Spanish', 'Italian', 'Dutch', 'Russian', 'Chinese', 'Greek', 'Modern Greek', 'Esperanto',
        'Japanese', 'Korean', 'Arabic', 'Portuguese', 'Hindi', 'Bengali', 'Turkish', 'Swedish', 'Finnish', 'Tagalog', 'Latin',
        'Modern Greek (1453-'
        # add more as needed
]

        # Extract language from title
        match = re.search(r'\(([^)]+)\)', title)
        if match:
            content = match.group(1).strip()
            # Check if content matches any known language (case-insensitive)
            if any(lang.lower() == content.lower() for lang in known_languages):
                language = content
                # Remove the language part from the title
                title = re.sub(r'\s*\([^)]+\)', '', title).strip()
            else:
                # If not a known language, default
                language = 'English'
        else:
            language = 'English'

        author_tag = book.select_one(".subtitle")
        author = author_tag.text.strip() if author_tag else 'Unknown Author'
        if len(author) > 255:
            author = author[:247] + ' and more'  # Leave 8 characters for ' and more'
        link_tag = book.find('a', class_='link')
        relative_url = link_tag['href'] if link_tag else None
        book_url = urljoin(base_url, relative_url) if relative_url else ''

                # 🌟 Extract category 🌟
        category = "Hist-Ancient"  # You can hardcode it for now
        # Or extract dynamically if you can locate a category tag

        # Extract publication year from title or subtitle
        year_match = re.search(r'\b(1[0-9]{3}|20[0-9]{2})\b', title + ' ' + author)
        publication_year = int(year_match.group(1)) if year_match else None


        # Extract gutenberg_id from URL e.g. /ebooks/46976
        gutenberg_id = None
        if relative_url:
            id_match = re.search(r'/ebooks/(\d+)', relative_url)
            gutenberg_id = int(id_match.group(1)) if id_match else None
        
        # Insert into database
        cursor.execute("""
            INSERT IGNORE INTO ancient (title, author, book_url, category, publication_year, language, gutenberg_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (title, author, book_url, category, publication_year, language, gutenberg_id))

        print(f"{title} - {author} - {book_url} - {category} -{publication_year} {language}")

        
        total_inserted += 1
        print(f"Inserted: {title} by {author}")

    db.commit()
    start_index += books_per_page
    time.sleep(1)  # Be polite to the server

cursor.close()
db.close()

print(f"Total books inserted: {total_inserted}")