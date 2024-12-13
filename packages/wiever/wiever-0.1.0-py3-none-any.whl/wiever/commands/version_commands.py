import typer

app = typer.Typer(help="Get the current version of the Viewer CLI.")


@app.command()
def version():
    print("0.0.1")