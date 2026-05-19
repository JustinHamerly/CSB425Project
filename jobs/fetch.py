import json
from pathlib import Path
import pandas as pd
import requests

SUBJECT_LIST = ["science", "history", "technology"]

API_ENDPOINT = "https://openlibrary.org/search.json"

RAW_DATA_DIR = Path("data/raw")

RAW_JSON_PATH = RAW_DATA_DIR / "raw_data.json"
RAW_CSV_PATH = RAW_DATA_DIR / "raw_data.csv"

def fetch_books(subject: str, limit=100) -> json:
    req_params = {
        "subject": subject,
        "limit": limit
    }

    res = requests.get(API_ENDPOINT, params=req_params)
    res.raise_for_status()

    return res.json()

def return_first_item(value, default=None):
    if isinstance(value, list) and len(value) > 0:
        return value[0]
    return default

def main():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    raw_results = {}

    book_rows = []
    
    for subject in SUBJECT_LIST:
        data = fetch_books(subject)
        raw_results[subject] = data
        
        books = data.get("docs", [])
        
        for book in books:
            book_row = {
                "subject": subject,
                "title": book.get("title", None),
                "author": return_first_item(book.get("author_name")),
                "first_publish_year": book.get("first_publish_year", None),
                "edition_count": book.get("edition_count", None),
                "language": return_first_item(book.get("language"))
            }

            book_rows.append(book_row)

    with open(RAW_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(raw_results, f, indent=2)

    books_df = pd.DataFrame(book_rows)
    books_df.to_csv(RAW_CSV_PATH, index=False)

    print(f"Total Book Row Count: {len(books_df)}")
    print("\nDataframe Schema:")
    print(books_df.dtypes)
    print("\nRow Samples:")
    print(books_df.head())

if __name__ == "__main__":
    main()
