import typer
from rich.console import Console
from rich.table import Table

from watchmatch.ingest.letterboxd import parse_letterboxd_csv
from watchmatch.normalize import canonicalize_raw_movies
from watchmatch.providers.tmdb import TMDbClient
from watchmatch.matching.ranking import rank_availability

app = typer.Typer()
console = Console()

@app.command()
def run(watchlist: str):
    """Process a Letterboxd CSV watchlist and show streaming options."""
    # 1️⃣ Parse CSV
    raw_movies = parse_letterboxd_csv(watchlist)
    movies = canonicalize_raw_movies(raw_movies)

    # 2️⃣ TMDb client
    client = TMDbClient()

    # 3️⃣ Process each movie
    for m in movies:
        client.enrich_movie(m)
        avail = client.get_watch_providers(m)

        # 4️⃣ Build Rich table
        table = Table(title=f"{m.title} ({m.year})", show_lines=True)
        table.add_column("Type", style="bold cyan")
        table.add_column("Providers", style="magenta")

        table.add_row("Flatrate", ", ".join(p.provider_name for p in avail.flatrate) or "-")
        table.add_row("Rent", ", ".join(p.provider_name for p in avail.rent) or "-")
        table.add_row("Buy", ", ".join(p.provider_name for p in avail.buy) or "-")

        # 5️⃣ Compute best option
        best = rank_availability(avail)
        best_text = best.provider_name if best else "None"

        # 6️⃣ Print
        console.print(table)
        console.print(f"Best option: [bold green]{best_text}[/bold green]\n")
