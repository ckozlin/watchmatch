from dotenv import load_dotenv
import os
import requests
from watchmatch.models import Movie, Availability, ProviderPrice
from typing import Optional

# Load the .env in the repo root
load_dotenv()  

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

class TMDbClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or TMDB_API_KEY
        if not self.api_key:
            raise ValueError(
                "TMDb API key not set. Put it in your .env as TMDB_API_KEY."
            )

    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[dict]:
        params = {"api_key": self.api_key, "query": title}
        if year:
            params["year"] = year
        response = requests.get(f"{BASE_URL}/search/movie", params=params)
        if response.status_code != 200:
            return None
        data = response.json()
        results = data.get("results")
        if results:
            return results[0]  # top result for now
        return None

    def enrich_movie(self, movie: Movie) -> Movie:
        result = self.search_movie(movie.title, movie.year)
        if not result:
            return movie
        movie.tmdb_id = result.get("id")
        movie.imdb_id = result.get("imdb_id")  # might be None
        movie.runtime = result.get("runtime")  # search result often null; full fetch later
        return movie

    def get_watch_providers(self, movie: Movie, region: str = "US") -> Availability:
        if not movie.tmdb_id:
            return Availability()

        url = f"{BASE_URL}/movie/{movie.tmdb_id}/watch/providers"
        params = {"api_key": self.api_key}
        resp = requests.get(url, params=params)
        if resp.status_code != 200:
            return Availability()

        data = resp.json()
        country_data = data.get("results", {}).get(region, {})
        availability = Availability()

        for category in ["flatrate", "rent", "buy"]:
            for entry in country_data.get(category, []):
                availability_item = ProviderPrice(
                    provider_name=entry.get("provider_name"),
                    logo_path=entry.get("logo_path"),
                    display_priority=entry.get("display_priority")
                )
                getattr(availability, category).append(availability_item)

        return availability