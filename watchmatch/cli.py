import typer
from watchmatch.ingest.letterboxd import parse_letterboxd_csv
from watchmatch.normalize import canonicalize_raw_movies
from watchmatch.providers.tmdb import TMDbClient

app = typer.Typer()

@app.command()
def run(watchlist: str):
    raw_movies = parse_letterboxd_csv(watchlist)
    movies = canonicalize_raw_movies(raw_movies)

    client = TMDbClient()
    enriched = [client.enrich_movie(m) for m in movies]

    typer.echo(f"Enriched {len(enriched)} movies with TMDb IDs:")
    for m in enriched:
        typer.echo(f"- {m.title} ({m.year}) imdb: {m.imdb_id} tmdb: {m.tmdb_id}")
