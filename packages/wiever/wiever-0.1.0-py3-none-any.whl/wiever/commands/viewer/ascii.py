import typer
from wiever.core.viewer.ascii_tree import AsciiTree
from typing_extensions import Annotated

app = typer.Typer(help="Display directory structure in ASCII format.")

@app.command()
def ascii(
        root_dir: Annotated[str, typer.Argument(..., help="The root directory to display the tree for.")], 
        # max_depth: Annotated[int, typer.Option(-1, help="Maximum depth to traverse. Default is -1 (no limit).")],
        # exclude: Annotated[str, typer.Option(None, help="Exclude files or directories matching the pattern.")],
        # include: Annotated[str, typer.Option(None, help="Include only files or directories matching the pattern.")],
        # pattern: Annotated[str, typer.Option(None, help="Pattern to match files or directories.")]
    ):
    tree = AsciiTree(root_dir=root_dir, max_depth=-1)
    tree.display()
