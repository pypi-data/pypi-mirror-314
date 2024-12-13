import typer
from wiever.commands import version_commands
from wiever.commands.viewer import ascii


class Cli:
    def __init__(self) -> None:
        self.typer = typer.Typer(
            help="Viewer CLI." + "\n" + "https://github.com/alirezaaraby/wiever", pretty_exceptions_enable=False
        )
        self.load_commands()

    def load_commands(self):
        self.typer.command()(version_commands.version)
        self.typer.command()(ascii.ascii)

    def run(self):
        self.typer()

