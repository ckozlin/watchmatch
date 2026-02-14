import typer
from watchmatch.ingest.letterboxd import parse_letterboxd_csv
from watchmatch.normalize import canonicalize_raw_movies

app = typer.Typer()

@app.command()
def run(watchlist: str):
    raw_movies = parse_letterboxd_csv(watchlist)
    movies = canonicalize_raw_movies(raw_movies)
    typer.echo(f"Canonicalized {len(movies)} movies:")
    for m in movies:
        typer.echo(f"- {m.title} ({m.year}) imdb: {m.imdb_id} tmdb: {m.tmdb_id}")
