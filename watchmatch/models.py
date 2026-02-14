from pydantic import BaseModel
from typing import Optional, List

class Movie(BaseModel):
    title: str
    year: Optional[int] = None
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
    runtime: Optional[int] = None  # in minutes
    letterboxd_uri: Optional[str] = None

class ProviderPrice(BaseModel):
    provider_name: str
    logo_path: str | None = None
    display_priority: int | None = None

class Availability(BaseModel):
    flatrate: List[ProviderPrice] = []
    rent: List[ProviderPrice] = []
    buy: List[ProviderPrice] = []
