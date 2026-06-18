QUERIES = {
    "ancient": {
        "type": "corpus",
        "description": "General collection of ancient history books (capped at 100 entries)",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            LIMIT 100
        """
    },
    
    "ancient_greek": {
        "type": "corpus",
        "description": "Books focused on Ancient Greece, Athens, and classic Greek philosophers like Plato and Aristotle",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE title LIKE '%Greek%'
            OR title LIKE '%Greece%'
            OR title LIKE '%Athens%'
            OR title LIKE '%Plato%'
            OR title LIKE '%Aristotle%'
        """
    },

    "ancient_roman": {
        "type": "corpus",
        "description": "Works relating to the Roman Empire, Rome, Caesar, and classical writers like Cicero",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE title LIKE '%Roman%'
            OR title LIKE '%Rome%'
            OR title LIKE '%Caesar%'
            OR title LIKE '%Cicero%'
        """
    },

    "ancient_pre1500": {
        "type": "corpus",
        "description": "Early historical works and texts originally written or set before the year 1500",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE publication_year < 1500
        """
    },

    "ancient_english":  {
        "type": "corpus",
        "description": "A sample subset of 50 ancient history books translated into or written in English",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE language = 'English'
            LIMIT 50
        """
    },

    "pre1900": {
        "type": "corpus",
        "description": "Historical texts published prior to the 20th century (before 1900)",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE publication_year < 1900
        """
    },

    "alexander": {
        "type": "report",
        "description": "Books specifically mentioning Alexander the Great or related Macedonian/Hellenistic history",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE title LIKE '%Alexander%'
        """
    },

    "religious-authors": {
        "type": "report",
        "description": "Statistical report counting prolific religious authors with more than one work",
        "sql": """
            SELECT author, COUNT(*) AS book_count
            FROM religious
            GROUP BY author
            HAVING COUNT(*) > 1
            ORDER BY book_count DESC;
        """
    },

    "timeline": {
        "type": "corpus",
        "description": "Chronologically ordered history corpus tracking works by known publication year",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE publication_year IS NOT NULL
            ORDER BY publication_year ASC
        """
    },

    "english": {
        "type": "corpus",
        "description": "Full collection of history texts available in the English language",
        "sql": """
            SELECT gutenberg_id, title
            FROM ancient
            WHERE language = 'English'
        """
    },

    "all_history": {
        "type": "corpus",
        "description": "Master cross-table aggregation uniting ancient, european, general, and religious texts",
        "sql": """
            SELECT gutenberg_id, title FROM ancient
            UNION
            SELECT gutenberg_id, title FROM european
            UNION
            SELECT gutenberg_id, title FROM general
            UNION
            SELECT gutenberg_id, title FROM religious
        """
    },

    "religious_ancient": {
        "type": "corpus",
        "description": "Early spiritual and religious texts published prior to the industrial era (pre-1800)",
        "sql": """
            SELECT gutenberg_id, title
            FROM religious
            WHERE publication_year < 1800
            ORDER BY publication_year ASC
        """
    },

    "european_multilang": {
        "type": "corpus",
        "description": "European collection texts written in original languages (excluding English translations)",
        "sql": """
            SELECT gutenberg_id, title
            FROM european
            WHERE language != 'English'
            AND language IS NOT NULL
            ORDER BY language
        """
    },

    "stoics":  {
        "type": "corpus",
        "description": "Philosophical texts highlighting Stoicism, Roman emperors, and early patristic/mystic writers",
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
        """
    },

    "gnostics":  {
        "type": "corpus",
        "description": "Esoteric, Gnostic, and Neoplatonic philosophical texts (including Plotinus and Origen)",
        "sql": """
            SELECT gutenberg_id, title FROM religious
            WHERE title LIKE '%Gnostic%'
            OR title LIKE '%Neoplatoni%'
            OR title LIKE '%Plotinus%'
            OR title LIKE '%Origen%'
        """
    },

    "jena_romantics":  {
        "type": "corpus",
        "description": "German Idealism and Romanticism texts featuring Schiller, Hegel, Schelling, and Novalis",
        "sql": """
            SELECT gutenberg_id, title FROM european
            WHERE title LIKE '%Schiller%'
            OR title LIKE '%Novalis%'
            OR title LIKE '%Schlegel%'
            OR title LIKE '%Schelling%'
            OR title LIKE '%Hegel%'
            OR title LIKE '%Fichte%'
        """
    },

    "wittgenstein": {
        "type": "corpus",
        "description": "Early 20th-century analytic philosophy and logic corpus (Wittgenstein, Russell, Frege)",
        "sql": """
            SELECT gutenberg_id, title FROM european
            WHERE title LIKE '%Wittgenstein%'
            OR title LIKE '%Russell%'
            OR title LIKE '%Frege%'
        """
    },

    # --- NOVAS QUERIES DO TIPO REPORT ---

    "report_lang_distribution": {
        "type": "report",
        "description": "Statistical report showing the most frequent languages across the entire European catalog",
        "sql": """
            SELECT language, COUNT(*) AS volume
            FROM european
            WHERE language IS NOT NULL
            GROUP BY language
            ORDER BY volume DESC;
        """
    },

    "report_century_volume": {
        "type": "report",
        "description": "Chronological report grouping the 'ancient' catalog books by century to see density",
        "sql": """
            SELECT (publication_year DIV 100) * 100 AS century, COUNT(*) AS volume
            FROM ancient
            WHERE publication_year IS NOT NULL
            GROUP BY century
            ORDER BY century ASC;
        """
    },

    "report_category_share": {
        "type": "report",
        "description": "High-level overview displaying the total number of books managed in each primary database table",
        "sql": """
            SELECT 'Ancient History' AS category, COUNT(*) AS total_books FROM ancient
            UNION ALL
            SELECT 'European Literary/Philosophy', COUNT(*) FROM european
            UNION ALL
            SELECT 'General History Collection', COUNT(*) FROM general
            UNION ALL
            SELECT 'Religious & Spiritual Texts', COUNT(*) FROM religious;
        """
    }
}