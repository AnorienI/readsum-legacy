# ReadSum

ReadSum is a modular Python pipeline for large-scale analysis of digital books 
(EPUB). It combines web-scraped corpora, relational databases, and natural 
language processing (NLP) techniques to perform statistical analysis across 
hundreds or thousands of texts.

The project was originally developed to analyze historical works from Project 
Gutenberg and has evolved into a reusable framework for corpus exploration and 
text mining.

## Features

### Corpus Management

* Stores book metadata in MariaDB/MySQL
* Maps database records to local EPUB files
* Supports large collections of digital books

### Text Extraction

* Reads EPUB files in batch
* Extracts textual content with BeautifulSoup
* Removes HTML tags and formatting artifacts
* Produces clean text suitable for analysis

### Linguistic Analysis

Current analyses include:

* Most common nouns
* Most common verbs
* Most common adjectives
* Longest words
* Longest sentences
* Hapax legomena (words appearing only once)
* Lexical density calculations

The analysis engine is query-driven and can be extended with new analytical 
functions.

### Reporting

* CSV export compatible with LibreOffice Calc and Excel
* Structured output for further analysis
* Reusable query results

## Project Structure

```text
readsum/
├── main.py              # Application entry point
├── database.py          # Database access layer
├── epub_reader.py       # EPUB extraction and parsing
├── analysis.py          # NLP and statistical functions
├── queries.py           # Available analysis queries
├── exporter.py          # CSV export functionality
├── requirements.txt
├── .env.example
└── .gitignore
```

## Technologies

* Python 3.10+
* MariaDB / MySQL
* BeautifulSoup4
* EbookLib
* mysql-connector-python

## Installation

Clone the repository:

```bash
git clone https://github.com/AnorienI/readsum.git
cd readsum
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create an environment file:

```bash
cp .env.example .env
```

Configure database credentials in `.env`.

## Usage

Run the application:

```bash
python main.py
```

Select one of the available analyses from the menu.

Example analyses:

1. Top 20 most common nouns
2. Top 20 most common verbs
3. Top 20 most common adjectives
4. Longest words
5. Longest sentences
6. Hapax legomena
7. Lexical density

Results can be exported directly to CSV files.

## Future Development

Planned improvements include:

* Additional corpus statistics
* Named entity analysis
* Comparative author studies
* Word frequency analysis by author
* Visualization and chart generation
* Summarization workflows using language models

## Author

Anestis M.

