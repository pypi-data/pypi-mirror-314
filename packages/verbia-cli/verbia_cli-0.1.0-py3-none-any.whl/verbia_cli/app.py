import sys

import typer
from loguru import logger

from verbia_cli.sub_commands import word_commands, config_commands, vocabulary_commands

logger.remove()
logger.add(sys.stdout, level="INFO")

__version__ = "0.1.0"
# Typer CLI app instance
app = typer.Typer(
    name="verbia",
    help="A command-line tool for learning and practicing vocabulary.",
    no_args_is_help=True,
)
# Subcommands manage vocabularies
app.add_typer(vocabulary_commands)
app.add_typer(word_commands)
app.add_typer(config_commands)


def version_callback(value: bool):
    if value:
        typer.echo(f"verbia {__version__}")
        raise typer.Exit()


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version.",
    ),
):
    pass


if __name__ == "__main__":
    app()
