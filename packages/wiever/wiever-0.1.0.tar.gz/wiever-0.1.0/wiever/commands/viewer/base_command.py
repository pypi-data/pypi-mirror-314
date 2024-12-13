from abc import ABC, abstractmethod
import typer

class BaseViewerCommand(ABC):
    """
    Abstract base class for CLI viewer commands.
    Defines the common structure for all viewer commands.
    """
    def __init__(self):
        self.app = typer.Typer(help=self.get_help())

    @abstractmethod
    def get_help(self) -> str:
        """Return the help text for the command."""
        pass

    @abstractmethod
    def execute(self, root_dir: str, max_depth: int):
        """Execute the specific viewer command."""
        pass

    def register_command(self):
        """Register the CLI command with Typer."""
        @self.app.command()
        def command(root_dir: str = ".", max_depth: int = -1):
            """
            CLI command handler for the viewer.
            Args:
                root_dir (str): The root directory to display.
                max_depth (int): Maximum depth to display. Default is -1 (no limit).
            """
            self.execute(root_dir, max_depth)
