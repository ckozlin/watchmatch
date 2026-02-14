from typing import List
from watchmatch.ingest.letterboxd import RawMovie
from watchmatch.models import Movie

def canonicalize_raw_movies(raw_movies: List[RawMovie]) -> List[Movie]:
    movies: List[Movie] = []
    for rm in raw_movies:
        movies.append(Movie(
            title=rm.title,
            year=rm.year,
            letterboxd_uri=getattr(rm, "letterboxd_uri", None),
            imdb_id=None,   # to be filled during TMDb enrichment
            tmdb_id=None,   # to be filled during TMDb enrichment
            runtime=None    # to be filled during TMDb enrichment
        ))
    return movies
