from functools import wraps

import typer

from verbia_core.error import VerbiaError

APP_NAME = "verbia"

states = {"verbose": False}


def set_states(verbose: bool = False):
    states["verbose"] = verbose


def handle_verbia_error():
    """Decorator for handling errors related to the vocabulary operations."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except VerbiaError as e:
                typer.echo(f"Error: {e}")
                raise typer.Exit(1)

        return wrapper

    return decorator
