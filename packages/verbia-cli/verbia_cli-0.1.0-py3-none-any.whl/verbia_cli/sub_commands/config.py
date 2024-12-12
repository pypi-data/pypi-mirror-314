from typing import Annotated

import typer
from loguru import logger

from verbia_cli import config
from verbia_cli.common import handle_verbia_error

app = typer.Typer(
    name="config",
    help="Manage configuration settings.",
    no_args_is_help=True,
)


@app.command(name="list")
@handle_verbia_error()
def list_config():
    """
    List all available configuration settings.
    If a setting is not set, it will display "N/A".
    """
    all_config = config.get_user_available_config()
    for key, value in all_config.items():
        typer.echo(f"{key}: {value}")


@app.command(name="set", no_args_is_help=True)
@handle_verbia_error()
def set_config(
    key: str,
    value: Annotated[
        str, typer.Option(help="Value of the key, if not provided, will be prompted.")
    ] = None,
):
    """
    Set a configuration setting.
    """
    logger.debug(f"Setting config key: {key}")

    key = key.lower()
    if key not in config.user_available_config_keys:
        typer.echo(f"Invalid config key: {key}")
        raise typer.Exit(1)
    if not value:
        value = typer.prompt(f"Enter value for {key}: ", type=str)

    config.set_config(key, value)
    typer.echo(f"Set {key} to {value}.")
