QUERIES = {
    "ancient": {
        "type": "corpus",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            LIMIT 100
        """
    },
    
    
    "ancient_greek": {
        "type": "corpus",
        "sql": """
        SELECT gutenberg_id, title
        FROM ancient
        WHERE title LIKE '%Greek%'
        OR title LIKE '%Greece%'
        OR title LIKE '%Athens%'
        OR title LIKE '%Plato%'
        OR title LIKE '%Aristotle%'
    """},

    "ancient_roman": {
        "type": "corpus",
        "sql": """
        SELECT gutenberg_id, title
        FROM ancient
        WHERE title LIKE '%Roman%'
        OR title LIKE '%Rome%'
        OR title LIKE '%Caesar%'
        OR title LIKE '%Cicero%'
    """},

    "ancient_pre1500": {
        "type": "corpus",
        "sql": """
        SELECT gutenberg_id, title
        FROM ancient
        WHERE publication_year < 1500
    """},

    "ancient_english":  {
        "type": "corpus",
        "sql":"""
        SELECT gutenberg_id, title
        FROM ancient
        WHERE language = 'English'
        LIMIT 50
    """},

    "pre1900": {
        "type": "corpus",
        "sql":"""
        SELECT gutenberg_id, title
        FROM ancient
        WHERE publication_year < 1900
    """},

    "alexander": {
        "type": "corpus",
        "sql":"""
        SELECT gutenberg_id, title
        FROM ancient
        WHERE title LIKE '%Alexander%'
    """},

    "religious-authors": {
        "type": "report",
        "sql": """
            SELECT author, COUNT(*) AS book_count
            FROM religious
            GROUP BY author
        HAVING COUNT(*) > 1
        ORDER BY book_count DESC;
    """},

    # books with known publication year, sorted chronologically
    "timeline": {
        "type": "corpus",
        "sql": """
        SELECT gutenberg_id, title
        FROM ancient
        WHERE publication_year IS NOT NULL
        ORDER BY publication_year ASC
    """},

    # english books only
    "english": {
        "type": "corpus",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
        WHERE language = 'English'
    """},

    # cross-table: all books from all categories in one shot
    "all_history": {
        "type": "corpus",
        "sql":"""
        SELECT gutenberg_id, title FROM ancient
        UNION
        SELECT gutenberg_id, title FROM european
        UNION
        SELECT gutenberg_id, title FROM general
        UNION
        SELECT gutenberg_id, title FROM religious
    """},

    # religious books pre-1800
    "religious_ancient": {
        "type": "corpus",
        "sql": """
            SELECT gutenberg_id, title
            FROM religious
            WHERE publication_year < 1800
            ORDER BY publication_year ASC
        """
    },

    # european books in languages other than English
    "european_multilang": {
        "type": "corpus",
        "sql": """
            SELECT gutenberg_id, title
            FROM european
            WHERE language != 'English'
            AND language IS NOT NULL
            ORDER BY language
    """},

    "stoics":  {
        "type": "corpus",
        "sql": """
        SELECT gutenberg_id, title FROM ancient
        WHERE title LIKE '%Stoic%'
        OR title LIKE '%Marcus Aurelius%'
        OR title LIKE '%Epictetus%'
        OR title LIKE '%Seneca%'
        OR title LIKE '%Zeno%'
        OR title LIKE '%mystic%'
        OR title LIKE '%Hermetic%'
        OR title LIKE '%Clement%'
        OR title LIKE '%Tertullian%'
    """},

    "gnostics":  {
"type": "corpus",
        "sql":"""
        SELECT gutenberg_id, title FROM religious
        WHERE title LIKE '%Gnostic%'
        OR title LIKE '%Neoplatoni%'
        OR title LIKE '%Plotinus%'
        OR title LIKE '%Origen%'
    """},

    "jena_romantics":  {
        "type": "corpus",
        "sql": """
        SELECT gutenberg_id, title FROM european
        WHERE title LIKE '%Schiller%'
        OR title LIKE '%Novalis%'
        OR title LIKE '%Schlegel%'
        OR title LIKE '%Schelling%'
        OR title LIKE '%Hegel%'
        OR title LIKE '%Fichte%'
    """},

    "wittgenstein": {
        "type": "corpus",
        "sql": """
            SELECT gutenberg_id, title FROM european
            WHERE title LIKE '%Wittgenstein%'
            OR title LIKE '%Russell%'
        OR title LIKE '%Frege%'
    """
}}