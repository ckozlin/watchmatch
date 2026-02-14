import typer
from watchmatch.ingest.letterboxd import parse_letterboxd_csv

app = typer.Typer()

@app.command()
def run(watchlist: str):
    movies = parse_letterboxd_csv(watchlist)
    typer.echo(f"Found {len(movies)} movies in your watchlist:")
    for m in movies:
        typer.echo(f"- {m.title} ({m.year}) URI: {m.letterboxd_uri}")
