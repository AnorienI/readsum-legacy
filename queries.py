QUERIES = {
    "ancient": """
        SELECT gutenberg_id, title
        FROM history_books_ancient
    """,

    "pre1900": """
        SELECT gutenberg_id, title
        FROM history_books_ancient
        WHERE publication_year < 1900
    """,

    "alexander": """
        SELECT gutenberg_id, title
        FROM history_books_ancient
        WHERE title LIKE '%Alexander%'
    """,

    "religious": """
        SELECT author, COUNT(*) AS book_count
        FROM history_books_religious
        GROUP BY author
        HAVING COUNT(*) > 1
        ORDER BY book_count DESC;
    """,

    # books with known publication year, sorted chronologically
    "timeline": """
        SELECT gutenberg_id, title
        FROM history_books_ancient
        WHERE publication_year IS NOT NULL
        ORDER BY publication_year ASC
    """,

    # english books only
    "english": """
        SELECT gutenberg_id, title
        FROM history_books_ancient
        WHERE language = 'English'
    """,

    # cross-table: all books from all categories in one shot
    "all_history": """
        SELECT gutenberg_id, title FROM history_books_ancient
        UNION
        SELECT gutenberg_id, title FROM history_books_european
        UNION
        SELECT gutenberg_id, title FROM history_books_general
        UNION
        SELECT gutenberg_id, title FROM history_books_religious
    """,

    # religious books pre-1800
    "religious_ancient": """
        SELECT gutenberg_id, title
        FROM history_books_religious
        WHERE publication_year < 1800
        ORDER BY publication_year ASC
    """,

    # european books in languages other than English
    "european_multilang": """
        SELECT gutenberg_id, title
        FROM history_books_european
        WHERE language != 'English'
        AND language IS NOT NULL
        ORDER BY language
    """
}