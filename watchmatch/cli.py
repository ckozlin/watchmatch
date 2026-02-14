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
    for m in movies:
        client.enrich_movie(m)
        avail = client.get_watch_providers(m)
        typer.echo(f"{m.title} ({m.year})")
        if avail.flatrate:
            typer.echo(f"  Flatrate: {', '.join([p.provider_name for p in avail.flatrate])}")
        if avail.rent:
            typer.echo(f"  Rent: {', '.join([p.provider_name for p in avail.rent])}")
        if avail.buy:
            typer.echo(f"  Buy: {', '.join([p.provider_name for p in avail.buy])}")
        typer.echo("")