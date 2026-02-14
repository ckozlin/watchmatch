import typer

app = typer.Typer()

@app.command()
def run(watchlist: str):
    typer.echo(f"Processing watchlist: {watchlist}")

