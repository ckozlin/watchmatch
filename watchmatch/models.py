from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
    title: str
    year: Optional[int] = None
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
    runtime: Optional[int] = None  # in minutes
    letterboxd_uri: Optional[str] = None
