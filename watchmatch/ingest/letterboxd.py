import csv
from typing import List
from pydantic import BaseModel

class RawMovie(BaseModel):
    title: str
    year: int | None = None
    letterboxd_uri: str | None = None

def parse_letterboxd_csv(file_path: str) -> List[RawMovie]:
    movies: List[RawMovie] = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row.get('Name')
            year_str = row.get('Year')
            uri = row.get('Letterboxd URI')
            year = int(year_str) if year_str and year_str.isdigit() else None
            if title:
                movies.append(RawMovie(title=title, year=year, letterboxd_uri=uri))
    return movies
