import typer
from rich.console import Console
from rich.table import Table
import json
import csv
from pathlib import Path

from watchmatch.ingest.letterboxd import parse_letterboxd_csv
from watchmatch.normalize import canonicalize_raw_movies
from watchmatch.providers.tmdb import TMDbClient
from watchmatch.matching.ranking import rank_availability
from watchmatch.models import Availability

app = typer.Typer()
console = Console()


def export_results(movies, avail_map, output_path: str):
    """Export enriched movies with availability to JSON or CSV."""
    output_path = Path(output_path)
    if output_path.suffix.lower() == ".json":
        data = []
        for m in movies:
            avail: Availability = avail_map[m.title]
            data.append({
                "title": m.title,
                "year": m.year,
                "imdb_id": m.imdb_id,
                "tmdb_id": m.tmdb_id,
                "flatrate": [p.provider_name for p in avail.flatrate],
                "rent": [p.provider_name for p in avail.rent],
                "buy": [p.provider_name for p in avail.buy],
            })
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    elif output_path.suffix.lower() == ".csv":
        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title","year","imdb_id","tmdb_id","flatrate","rent","buy"])
            writer.writeheader()
            for m in movies:
                avail: Availability = avail_map[m.title]
                writer.writerow({
                    "title": m.title,
                    "year": m.year,
                    "imdb_id": m.imdb_id,
                    "tmdb_id": m.tmdb_id,
                    "flatrate": ";".join(p.provider_name for p in avail.flatrate),
                    "rent": ";".join(p.provider_name for p in avail.rent),
                    "buy": ";".join(p.provider_name for p in avail.buy),
                })
    else:
        console.print(f"[red]Unsupported export format: {output_path.suffix}[/red]")


@app.command()
def run(watchlist: str, output: str = typer.Option(None, help="Optional output file path (JSON or CSV)")):
    """Process a Letterboxd CSV watchlist, show streaming options, and optionally export results."""
    # 1️⃣ Parse CSV
    raw_movies = parse_letterboxd_csv(watchlist)
    movies = canonicalize_raw_movies(raw_movies)

    # 2️⃣ TMDb client
    client = TMDbClient()

    # 3️⃣ Store availability for export
    avail_map = {}

    # 4️⃣ Process each movie
    for m in movies:
        client.enrich_movie(m)
        avail = client.get_watch_providers(m)
        avail_map[m.title] = avail

        # 5️⃣ Build Rich table
        table = Table(title=f"{m.title} ({m.year})", show_lines=True)
        table.add_column("Type", style="bold cyan")
        table.add_column("Providers", style="magenta")

        table.add_row("Flatrate", ", ".join(p.provider_name for p in avail.flatrate) or "-")
        table.add_row("Rent", ", ".join(p.provider_name for p in avail.rent) or "-")
        table.add_row("Buy", ", ".join(p.provider_name for p in avail.buy) or "-")

        # 6️⃣ Compute best option
        best = rank_availability(avail)
        best_text = best.provider_name if best else "None"

        # 7️⃣ Print table and best option
        console.print(table)
        console.print(f"Best option: [bold green]{best_text}[/bold green]\n")

    # 8️⃣ Export if requested
    if output:
        export_results(movies, avail_map, output)
        console.print(f"\nExported results to [bold green]{output}[/bold green]")
